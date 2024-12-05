from api.base import RequestHandler, route
from features.user import User
from features.payment_method import PaymentMethod
from infrastructure.work_management import WorkManager
from infrastructure.user import UserRepo


class CompleteOrderRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        user_repo = work_manager.get(UserRepo)
        self.user_feature = User(user_repo)
        self.payment_method = PaymentMethod()

    @route.post("/", auth_exempt=True)
    async def complete_order(self, req, resp):
        request_body = await req.get_media()
        print('request_body', request_body)
        payment_method_id = request_body["payment_method_id"]
        amount = 1000

        await self.payment_method.create_payment_intent(payment_method_id, amount)
        