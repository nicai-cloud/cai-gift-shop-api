import falcon.asgi

# Resource class for handling requests
class HelloWorldResource:
    async def on_get(self, req, resp):
        """Handles GET requests"""
        resp.media = {"message": "Hello, World!"}
        resp.status = falcon.HTTP_200

# Create Falcon app and add a route
app = falcon.asgi.App()
app.add_route('/hello', HelloWorldResource())
