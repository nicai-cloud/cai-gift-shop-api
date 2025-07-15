from falcon import HTTPBadRequest, HTTP_OK

from api.base import RequestHandler, route
from api.errors import NotFound
from api.response_types import GetBagsResponse, GetBagResponse
from features.bag_feature import BagFeature
from infrastructure.async_work_management import AsyncWorkManager


class BagRequestHandler(RequestHandler):
    def __init__(self, work_manager: AsyncWorkManager):
        super().__init__()
        self.bag_feature = BagFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_bags(self, req, resp):
        bags = await self.bag_feature.get_bags()
        resp.media = GetBagsResponse(bags=bags)
        resp.status = HTTP_OK

    @route.get("/{bag_id}", auth_exempt=True)
    async def get_bag(self, req, resp, bag_id):
        try:
            bag_id = int(bag_id)
        except ValueError:
            raise HTTPBadRequest(
                title="Invalid parameter",
                description="The 'bag_id' must be a valid integer."
            )

        bag = await self.bag_feature.get_bag_by_id(bag_id)
        if bag is None:
            raise NotFound(detail=f"Bag with bag_id {bag_id} not found.")

        resp.media = GetBagResponse(bag=bag)
        resp.status = HTTP_OK
