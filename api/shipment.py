import falcon

from api.base import RequestHandler, route
from features.shipment_feature import ShipmentFeature
from infrastructure.work_management import WorkManager


class ShipmentRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.shipment_feature = ShipmentFeature(work_manager)

    @route.get("/all", auth_exempt=True)
    async def get_shipments(self, req, resp):
        resp.media = await self.shipment_feature.get_shipments()
        resp.status = falcon.HTTP_OK

    @route.get("/{order_id}", auth_exempt=True)
    async def get_shipment_by_order_id(self, req, resp, order_id):
        resp.media = await self.shipment_feature.get_shipment_by_order_id(order_id)
        resp.status = falcon.HTTP_OK

    @route.post("/", auth_exempt=True)
    async def create_shipment(self, req, resp):
        request_body = await req.get_media()

        volume = request_body.get("volume", None)
        weight = request_body["weight"]
        delivery_fee = request_body["delivery_fee"]
        tracking_number = request_body["tracking_number"]
        order_id = request_body["order_id"]

        resp.media = await self.shipment_feature.create_shipment(volume, weight, delivery_fee, tracking_number, order_id)
        resp.status = falcon.HTTP_OK
