import asyncio
import logging
from contextvars import ContextVar
from typing import Any
from collections.abc import Callable, MutableMapping
from contextlib import contextmanager
from typing import Generic, Protocol, TypeVar

from falcon.asgi import Request, Response


LOG = logging.getLogger(__name__)

current_request_task = ContextVar("current_request_task", default=None)


class Transactable(Protocol):
    """Something which implements two-phase commit semantics.
    It is important that the transactable is thread-safe. It should ensure that all of the work performed in one thread
    is isolated from the work performed in another thread."""

    # Global transactions.
    async def begin(self): ...

    async def commit(self): ...

    async def rollback(self): ...

    async def close(self): ...

    # Sub transactions.
    def begin_nested(self): ...

    def commit_nested(self): ...

    def rollback_nested(self): ...


T = TypeVar("T", bound=Transactable)
S = TypeVar("S")


class UnitOfWork(Generic[T]):
    """Represents the scope of a single unit of work."""

    def __init__(self, transactable: T):
        self.transactable = transactable
        self.closed = False

        self.transactable.begin_nested()

    def cancel(self) -> None:
        """Cancel the current unit of work and reverse any changes which have already been made by rolling back the
        transactable."""

        self.transactable.rollback_nested()
        self.closed = True

    def complete(self) -> None:
        """Complete a unit of work by committing the transactable."""

        if not self.closed:
            self.transactable.commit_nested()
            self.closed = True

    def close(self) -> None:
        """Close a unit of work. This method is intended to be called at the very end of the scope, for situations where
        complete or cancel may or may not have been called.
        If one of those methods has been called first, close will do nothing.
        If a unit of work has not been cancelled or completed when close is called, it will be cancelled by default.
        """

        if not self.closed:
            self.cancel()


class NotRegistered(Exception):
    """Raised if an interface is not registered with a work manager."""


ConstructorRegistry = MutableMapping[type[S], Callable[[T], S]]
ImplementationCache = MutableMapping[type[S], S]


class WorkManager(Generic[T]):
    """A work manager coordinates the transactions of some Transactable. It allows the transactable to be shared
    across multiple classes in order to coordinate a unit of work across all of them.
    The assumption here is that in regular usage, the transactable will manage the highest-level scope outside of the
    work manager. The work manager exists for coordinating the transactable between different objects.
    """

    def __init__(self, transactable: T | None = None):
        super().__init__()

        self.transactable = transactable

        # This registry maps types to the callables which return instances of them.
        self.registry: ConstructorRegistry = {}

        # Keep a cache of the instantiated implementations.
        self.cache: ImplementationCache = {}

    def set_transactable(self, transactable: T):
        if self.transactable:
            raise RuntimeError("Cannot set a transactable twice.")

        if self.cache:
            raise RuntimeError("Cannot set a transactable because an instance has already been created.")

        self.transactable = transactable

    def get(self, interface: type[S]) -> S:
        """Retrieve an instance of an interface registered with the work manager."""

        try:
            instance = self.cache[interface]
        except KeyError:
            # We don't have a cached version of the instance. Attempt to construct it.
            #  This is technically not thread-safe if two things are trying to get something from the work manager
            #  at the same time. Because we're using IO-based greenlets, it's not an issue at the moment
            try:
                construct_instance = self.registry[interface]
            except KeyError:
                raise NotRegistered
            else:
                instance = construct_instance(self.transactable)
                self.cache[interface] = instance

        return instance

    def register(self, interface: type[S], constructor: Callable[[T], S]):
        self.registry[interface] = constructor

    def begin(self) -> UnitOfWork:
        """Begin a unit of work."""

        return UnitOfWork(self.transactable)

    @contextmanager
    def scope(self):
        unit = self.begin()

        try:
            yield unit
            unit.complete()
        except Exception:
            unit.cancel()
            raise
        finally:
            unit.close()


class WorkManagementMiddleware:
    """Middleware which manages database transactions against the lifecycle of a request."""

    def __init__(self, work_manager: WorkManager):
        self.transactable = work_manager.transactable

    async def process_request(self, request: Request, response: Response):
        current_request_task.set(asyncio.current_task())  # type: ignore
        await self.transactable.begin()

    async def process_response(
        self,
        request: Request,
        response: Response,
        resource: Any,
        request_succeeded: bool,
    ):
        if request_succeeded:
            LOG.debug("Committing transactable.")
            await self.transactable.commit()
        else:
            LOG.debug("Rolling back transactable.")
            await self.transactable.rollback()

        await self.transactable.close()
