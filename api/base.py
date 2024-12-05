import inspect
import logging

from falcon import HTTP_200, HTTPMethodNotAllowed, HTTPNotFound, HTTPUnauthorized
from falcon.routing import CompiledRouter

LOG = logging.getLogger(__name__)


class RequestRouter(CompiledRouter):
    def map_http_methods(self, resource, **kwargs):
        return super().map_http_methods(resource, **kwargs)


class RequestHandler:
    def __init__(self, *args, **kwargs):
        self.__routes__: dict[str, dict[str, str]] = {}
        self.router = CompiledRouter()

        for _, m in inspect.getmembers(self, inspect.ismethod):
            if hasattr(m, "__methods__"):
                for http_method, route_map in m.__methods__.items():
                    for route, _ in route_map.items():
                        method_map = self.__routes__.setdefault(route, {})
                        method_map[http_method] = m.__name__

                        self.router.add_route(route, self, _asgi=True)

    async def on_get(self, req, resp, uri_template, params):
        await self.handle_request("GET", req, resp, uri_template, params)

    async def on_post(self, req, resp, uri_template, params):
        await self.handle_request("POST", req, resp, uri_template, params)

    async def on_patch(self, req, resp, uri_template, params):
        await self.handle_request("PATCH", req, resp, uri_template, params)

    async def on_delete(self, req, resp, uri_template, params):
        await self.handle_request("DELETE", req, resp, uri_template, params)

    async def on_options(self, req, resp, uri_template, params):
        await self.handle_request("OPTIONS", req, resp, uri_template, params)

    async def __call__(self, req, resp, path="", **kwargs):
        # NOTE(michael): We must have this here for now because Falcon
        # middleware does not call process_resource for sinks, which means
        # that we are unable to exempt routes from authentication without
        # checking locally. The alternative is to avoid using sinks,
        # however I believe that the development convenience is significant
        # enough to warrant the tradeoff.
        #
        # Falcon is currently working on a feature to have
        # a path converter as part of the URL matching. This will solve a large
        # part of the problem for us.
        #
        # Note that Falcon's default responses to OPTIONS requests are not enabled
        # using sinks because they cannot infer the allowed request methods for a
        # particular resource. OPTIONS requests are by default unauthorized so we
        # can safely process the request as long as we don't call the handler method.
        result = self.router.find(path)

        if result is None:
            LOG.error("Could not find route for path.")
            raise HTTPNotFound()

        _, method_map, params, uri_template = result

        await method_map[req.method](req, resp, uri_template, params)

    async def handle_request(self, method, req, resp, uri_template, params):
        http_method_handlers = self.__routes__.get(uri_template)

        if not http_method_handlers:
            raise HTTPNotFound()

        # This code is taken directly from the default responder found in
        # falcon.responders.create_default_options.
        if method == "OPTIONS" and "OPTIONS" not in http_method_handlers:
            resp.status = HTTP_200
            resp.set_header("Allow", ", ".join(http_method_handlers.keys()))
            resp.set_header("Content-Length", "0")
            return

        handler = http_method_handlers.get(method)

        if not handler:
            raise HTTPMethodNotAllowed(allowed_methods=http_method_handlers.keys())

        try:
            handler_method = getattr(self, handler)
        except AttributeError:
            raise RuntimeError(f"Handler method {handler} does not exist on {self.__class__}")

        if handler_method.__methods__[method][uri_template]["auth_exempt"]:
            await handler_method(req, resp, **params)
            return

        if not req.context or not req.context.authorized:
            LOG.error("Request context is not authorized")
            raise HTTPUnauthorized()

        await handler_method(req, resp, **params)


class AlreadyRegistered(Exception):
    pass


class route:
    """A decorator which allows methods of resource classes to be used as view functions
    for specific routes. By default, all of the routes are authenticated.

    This decorator will only work for classes which inherit from RequestHandler.

    For example:

    class ExampleRequestHandler(RequestHandler):
        @route.get('/example')
        async def example_route(self, req, resp):
            resp.media = {"status": "ok"}

        @route.post('/example')
        async def example_route_post(self, req, resp):
            body = await req.get_media()

            await do_something_important(body)

            resp.media = {"status": "ok"}

        @route.get('/example_unauthenticated', auth_exempt=True)
        async def example_route_unauthenticated(self, req, resp):
            resp.media = {"status": "unauthenticated"}
    """

    @staticmethod
    def _annotate_method(
        method: str,
        r: str,
        allowed_access_levels: list[int] = [],
        minimum_level_required: int = 2,
        auth_exempt: bool = False,
    ):
        def _dec(f):
            if not hasattr(f, "__methods__"):
                # A mapping of method -> (route -> is authenticated)
                f.__methods__ = {}

            method_routes = f.__methods__.setdefault(method, {})

            method_routes[r] = {"auth_exempt": auth_exempt}
            return f

        return _dec

    @staticmethod
    def get(
        r: str, auth_exempt: bool = False, minimum_level_required: int = 2, allowed_access_levels: list[int] = []
    ):
        return route._annotate_method(
            "GET",
            r,
            auth_exempt=auth_exempt,
            minimum_level_required=minimum_level_required,
            allowed_access_levels=allowed_access_levels,
        )

    @staticmethod
    def post(
        r: str, auth_exempt: bool = False, minimum_level_required: int = 2, allowed_access_levels: list[int] = []
    ):
        return route._annotate_method(
            "POST",
            r,
            auth_exempt=auth_exempt,
            minimum_level_required=minimum_level_required,
            allowed_access_levels=allowed_access_levels,
        )

    @staticmethod
    def patch(
        r: str, auth_exempt: bool = False, minimum_level_required: int = 2, allowed_access_levels: list[int] = []
    ):
        return route._annotate_method(
            "PATCH",
            r,
            auth_exempt=auth_exempt,
            minimum_level_required=minimum_level_required,
            allowed_access_levels=allowed_access_levels,
        )

    @staticmethod
    def delete(
        r: str, auth_exempt: bool = False, minimum_level_required: int = 2, allowed_access_levels: list[int] = []
    ):
        return route._annotate_method(
            "DELETE",
            r,
            auth_exempt=auth_exempt,
            minimum_level_required=minimum_level_required,
            allowed_access_levels=allowed_access_levels,
        )
