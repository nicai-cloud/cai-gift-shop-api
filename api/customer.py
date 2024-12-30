import falcon

from api.base import RequestHandler, route
from features.customer_feature import CustomerFeature
from infrastructure.work_management import WorkManager


class CustomerRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.customer_feature = CustomerFeature(work_manager)

    @route.get("/all", auth_exempt=True)
    async def get_customers(self, req, resp):
        resp.media = await self.customer_feature.get_customers()
        resp.status = falcon.HTTP_OK

    @route.get("/{customer_id}", auth_exempt=True)
    async def get_customer(self, req, resp, customer_id):
        resp.media = await self.customer_feature.get_customer_by_id(customer_id)
        resp.status = falcon.HTTP_OK
