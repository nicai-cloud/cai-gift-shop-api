import falcon.asgi

# Resource class for handling requests
class HelloWorldResource:
    async def on_get(self, req, resp):
        """Handles GET requests"""
        resp.media = {"message": "Hello, World!"}
        resp.status = falcon.HTTP_200


class CORSMiddleware:
    async def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header("Access-Control-Allow-Origin", "*")  # Allow all origins
        resp.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")  # Allowed methods
        resp.set_header("Access-Control-Allow-Headers", "Content-Type")  # Allowed headers

# Create Falcon app and add a route
app = falcon.asgi.App(middleware=[CORSMiddleware()])
app.add_route('/hello', HelloWorldResource())
