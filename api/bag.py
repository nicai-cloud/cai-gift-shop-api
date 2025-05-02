from falcon import HTTP_OK

from api.base import RequestHandler, route
from api.errors import NotFound
from features.bag_feature import BagFeature
from infrastructure.work_management import WorkManager


class BagRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.bag_feature = BagFeature(work_manager)

    @route.get("/", auth_exempt=True)
    async def get_bags(self, req, resp):
        resp.media = await self.bag_feature.get_bags()
        resp.status = HTTP_OK

    @route.get("/{bag_id}", auth_exempt=True)
    async def get_bag(self, req, resp, bag_id):
        bag = await self.bag_feature.get_bag_by_id(int(bag_id))
        if bag is None:
            raise NotFound(detail=f"Bag with bag_id {bag_id} not found.")

        resp.media = bag
        resp.status = HTTP_OK
