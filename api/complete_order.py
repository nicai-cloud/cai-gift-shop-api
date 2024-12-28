from api.base import RequestHandler, route
from api.types import PublishableKeyResponse
from features.payment_method_feature import PaymentMethodFeature
from features.customer_feature import CustomerFeature
from features.email_feature import EmailFeature
from features.order_feature import OrderFeature
from features.order_item_feature import OrderItemFeature
from features.preselection_feature import PreselectionFeature
from features.inventory_feature import InventoryFeature
from infrastructure.work_management import WorkManager
from utils.config import get


class CompleteOrderRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.customer_feature = CustomerFeature(work_manager)
        self.order_item_feature = OrderItemFeature(work_manager)
        self.order_feature = OrderFeature(work_manager)
        self.preselection_feature = PreselectionFeature(work_manager)
        self.inventory_feature = InventoryFeature(work_manager)
        self.payment_method_feature = PaymentMethodFeature()
        self.email_feature = EmailFeature()

    @route.post("/calculate-total-cost", auth_exempt=True)
    async def calculate_total_cost(self, req, resp):
        request_body = await req.get_media()
        print('request_body', request_body)

        order_items = request_body["order_items"]
        resp.media = await self.order_feature.calculate_total_cost(order_items=order_items)
    
    @route.get("/publishable-key", auth_exempt=True)
    async def get_publishable_key(self, req, resp):
        resp.media = PublishableKeyResponse(
            publishable_key=get("STRIPE_PUBLISHABLE_KEY"),
        )

    async def _check_stock_availability(self, order_items):
        bag_quantities = {}
        item_quantities = {}
        for order_item in order_items:
            quantity = order_item["quantity"]
            bag_id = order_item.get("bag_id", None)
            item_ids = order_item.get("item_ids", None)
            if bag_id and item_ids:
                bag_quantities[bag_id] = bag_quantities.get(bag_id, 0) + quantity
                for item_id in item_ids:
                    item_quantities[item_id] = item_quantities.get(item_id, 0) + quantity

            preselection_id = order_item.get("preselection_id", None)
            if preselection_id:
                preselection = await self.preselection_feature.get_preselection_by_id(preselection_id)
                preselection_bag_id = preselection.bag_id
                preselection_item_ids = preselection.item_ids
                bag_quantities[preselection_bag_id] = bag_quantities.get(preselection_bag_id, 0) + quantity
                for preselection_item_id in preselection_item_ids:
                    item_quantities[preselection_item_id] = item_quantities.get(preselection_item_id, 0) + quantity

        inventories = await self.inventory_feature.get_inventories()
        print('!!inventories', inventories)

        print('!!bag_quantities', bag_quantities)
        
        print('!!item_quantities', item_quantities)
        # bag_inventory = inventories["bag"]
        # items_inventory = inventories["item"]


    @route.post("/", auth_exempt=True)
    async def complete_order(self, req, resp):
        request_body = await req.get_media()
        # print('request_body', request_body)

        customer_info = request_body["customer_info"]
        order_items = request_body["order_items"]
        payment_method_id = request_body["payment_method_id"]

        first_name = customer_info["first_name"]
        last_name = customer_info["last_name"]
        # TODO: sanitisation on email and mobile
        email = customer_info["email"]
        mobile = customer_info["mobile"]
        address = customer_info["address"]

        # Check there is enough stock
        await self._check_stock_availability(order_items)
        
        # total_cost = await self.order_feature.calculate_total_cost(order_items)

        # # Make the payment
        # await self.payment_method_feature.create_payment_intent(payment_method_id, total_cost)

        # # Create customer
        # customer_id = await self.customer_feature.create_customer(first_name, last_name, email, mobile, address)
        # print('!! created customer id: ', customer_id)

        # # Create an order against the customer
        # order_id = await self.order_feature.create_order(customer_id=customer_id, amount=total_cost)
        # print('!! created order id: ', order_id)

        # # Create each of the order items
        # order_item_ids = []
        # for order_item in order_items:
        #     quantity = order_item["quantity"]
        #     preselection_id = order_item.get("preselection_id", None)
        #     bag_id = order_item.get("bag_id", None)
        #     item_ids = order_item.get("item_ids", None)

        #     order_item_id = await self.order_item_feature.create_order_item(quantity, preselection_id, bag_id, item_ids, order_id)
        #     order_item_ids.append(order_item_id)
        #     print('!! created order item id: ', order_item_id)

        # # Send the successful order email
        # await self.email_feature.send_email(email, order_id)
