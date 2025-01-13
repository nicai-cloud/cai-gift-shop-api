from uuid import UUID
from falcon import HTTPBadRequest, HTTP_OK, HTTPNotFound

from api.base import RequestHandler, route
from features.shipment_feature import ShipmentAlreadyExistsException, ShipmentFeature
from features.email_feature import EmailFeature
from infrastructure.work_management import WorkManager


class ShipmentRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.shipment_feature = ShipmentFeature(work_manager)
        self.email_feature = EmailFeature()

    @route.get("/all", auth_exempt=True)
    async def get_shipments(self, req, resp):
        resp.media = await self.shipment_feature.get_shipments()
        resp.status = HTTP_OK

    @route.get("/", auth_exempt=True)
    async def get_shipment_by_order_id(self, req, resp):
        order_id = req.params.get('orderId')
        shipment = await self.shipment_feature.get_shipment_by_order_id(UUID(order_id))
        if shipment is None:
            raise HTTPNotFound(description="Shipment not found")
        
        resp.media = shipment
        resp.status = HTTP_OK

    @route.post("/", auth_exempt=True)
    async def create_shipment(self, req, resp):
        request_body = await req.get_media()

        volume = request_body.get("volume", None)
        weight = request_body["weight"]
        delivery_fee = request_body["delivery_fee"]
        tracking_number = request_body["tracking_number"]
        order_id = request_body["order_id"]

        try:
            # TODO: maybe change check on order_number instead of order_id?
            shipment_id = await self.shipment_feature.create_shipment(volume, weight, delivery_fee, tracking_number, order_id)
        except ShipmentAlreadyExistsException:
            raise HTTPBadRequest(
                title="Duplicate shipment for order_id",
                description="A shipment has already been created for the provided order_id."
            )

        if shipment_id is None:
            raise HTTPBadRequest(
                title="Unknown order_id",
                description="The provided order_id is not recognised."
            )
        
        # Get customer from order_id
        customer = await self.shipment_feature.get_customer(order_id)
        if customer is None:
            raise HTTPBadRequest(
                title="Unknown customer",
                description="The customer associated with the provided order_id is not found."
            )
        
        # Send customer delivery email
        await self.email_feature.send_delivery_email_to_customer(customer, tracking_number)

        resp.media = {"shipment_id": shipment_id}
        resp.status = HTTP_OK
