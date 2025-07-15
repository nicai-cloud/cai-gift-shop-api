import asyncio
import logging
from contextvars import ContextVar
from typing import Callable, Generic, Protocol, Type, TypeVar, Any
from falcon.asgi import Request, Response

LOG = logging.getLogger(__name__)

current_request_task = ContextVar("current_request_task", default=None)


class AsyncTransactable(Protocol):
    """Something which implements two-phase commit semantics."""

    # Global transactions.
    async def commit(self): ...

    async def rollback(self): ...

    # Sub transactions.
    async def begin_nested(self): ...

    # Cleanup
    async def close(self): ...


T = TypeVar("T", bound=AsyncTransactable)
S = TypeVar("S")


class AsyncUnitOfWork(Generic[T]):
    """Represents the scope of a single unit of work.

    The unit of work can be used as a context manager:

    with UnitOfWork(Session):
        # A transaction has started.
        do_something_in_the_db()
    # The transaction is committed in the DB.

    The AsyncWorkManager handles the creation of units of work for you,
    so you just need to call the `scope()` function:

    with work_manager.scope():
        do_something_in_the_db()

    """

    def __init__(self, transactable: T):
        self.transactable = transactable
        self.closed = False

    # Context manager implementation.
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            await self.complete()
        else:
            await self.cancel()

        return False  # Raise the exception if there was one.

    async def begin_nested(self):
        """Start a transaction in this unit of work."""

        await self.transactable.begin_nested()

    async def cancel(self) -> None:
        """Cancel the current unit of work and reverse any changes which have already been made by rolling back the
        transactable."""

        await self.transactable.rollback()
        self.closed = True

    async def complete(self) -> None:
        """Complete a unit of work by committing the transactable."""

        if not self.closed:
            await self.transactable.commit()
            self.closed = True


class NotRegistered(Exception):
    """Raised if an interface is not registered with a work manager."""

    pass


Constructor = Callable[[T], S]
ConstructorRegistry = dict[Type[S], Constructor[T, S]]
ImplementationCache = dict[Type[S], S]


class AsyncWorkManager(Generic[T]):
    """A work manager provides a consistent interface for managing units of work
    across different repositories.

    It consists of two main features:
    * a registry of services that can be retrieved by their interface.
    * functions to manage a unit of work.

    A work manager takes as its only argument a transactable, which is an object
    that supports transactions. The registry contains singleton instances of objects
    that perform work via the transactable.

    """

    def __init__(self, transactable: T | None = None):
        self.transactable = transactable

        # This registry maps types to the callables which return instances of them.
        self.registry: ConstructorRegistry[S, T] = {}

        # Keep a cache of the instantiated implementations.
        self.cache: ImplementationCache[S] = {}

    def set_transactable(self, transactable: T):
        if self.transactable:
            raise RuntimeError("Cannot set a transactable twice.")

        if self.cache:
            raise RuntimeError(
                "Cannot set a transactable because an instance has already been created."
            )

        self.transactable = transactable

    def get(self, interface: Type[S]) -> S:
        """Retrieve an instance of an interface registered with the work manager.

        Takes one argument:
        * interface: The interface for which to retrieve an instance. Must already have been registered.

        Returns an instance of the interface.

        """

        try:
            instance = self.cache[interface]
        except KeyError:
            try:
                construct_instance = self.registry[interface]
            except KeyError as e:
                raise NotRegistered(
                    f"No registry entry found for interface {interface}."
                )
            else:
                instance = construct_instance(self.transactable)
                self.cache[interface] = instance

        return instance

    def register(self, interface: Type[S], constructor: Callable[[T], S]):
        """Register an interface alongside a concrete constructor that will return an instance
        of that interface.

        Takes two arguments:
        * interface: the interface to be constructed.
        * constructor: a function that takes an instance of the transactable and returns an instance of the interface.

        """
        self.registry[interface] = constructor

    def scope(self) -> AsyncUnitOfWork[T]:
        """Construct a unit of work.

        This can be used manually or with a context manager:

        with work_manager.scope():
            do_something_db_related()

        scope = work_manager.scope()
        do_something_db_related()
        scope.commit()
        scope.close()

        """

        return AsyncUnitOfWork(self.transactable)

    async def close(self):
        """Call this method to clean up resources at the end of a particular process, for example,
        a request or a task.

        """
        await self.transactable.close()


class AsyncWorkManagementMiddleware:
    """Middleware which manages database transactions against the lifecycle of a request."""

    def __init__(self, work_manager: AsyncWorkManager):
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