from uuid import UUID
from falcon import HTTPBadRequest, HTTP_OK

from api.base import RequestHandler, route
from api.errors import NotFound
from api.response_types import GetCustomerResponse, GetCustomersResponse
from features.customer_feature import CustomerFeature
from infrastructure.work_management import WorkManager


class CustomerRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.customer_feature = CustomerFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_customers(self, req, resp):
        customers = await self.customer_feature.get_customers()
        resp.media = GetCustomersResponse(customers=customers)
        resp.status = HTTP_OK

    @route.get("/{customer_id}", auth_exempt=True)
    async def get_customer(self, req, resp, customer_id):
        try:
            customer_id = UUID(customer_id)
        except ValueError:
            raise HTTPBadRequest(
                title="Invalid parameter",
                description="The 'customer_id' must be a valid UUID."
            )

        customer = await self.customer_feature.get_customer_by_id(customer_id)
        if customer is None:
            raise NotFound(detail=f"Customer with customer_id {customer_id} not found.")

        resp.media = GetCustomerResponse(customer=customer)
        resp.status = HTTP_OK
