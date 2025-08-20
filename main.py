import functools
import logging
import re
from decimal import Decimal
from utils.config import get

import simplejson
from falcon import MEDIA_JSON, asgi, CORSMiddleware, media

from api.health_check import HealthCheckRequestHandler
from api.address import AddressRequestHandler
from api.bag import BagRequestHandler
from api.complete_order import CompleteOrderRequestHandler
from api.complete_pickup_order import CompletePickupOrderRequestHandler
from api.item import ItemRequestHandler
from api.payment import PaymentRequestHandler
from api.preselection import PreselectionRequestHandler
from api.inventory import InventoryRequestHandler
from api.inventory_transaction import InventoryTransactionRequestHandler
from api.customer import CustomerRequestHandler
from api.order import OrderRequestHandler
from api.order_item import OrderItemRequestHandler
from api.shipment import ShipmentRequestHandler
from api.fulfillment_method import FulfillmentMethodRequestHandler
from api.coupon import CouponRequestHandler
from api.image import ImageRequestHandler
from utils.json_dumps_default import json_dumps_default

from infrastructure.postgres import PostgresTransactable
from infrastructure.customer_repo import CustomerRepo, construct_postgres_customer_repo
from infrastructure.order_repo import OrderRepo, construct_postgres_order_repo
from infrastructure.order_item_repo import OrderItemRepo, construct_postgres_order_item_repo
from infrastructure.preselection_repo import PreselectionRepo, construct_postgres_preselection_repo
from infrastructure.preselection_bag_items_repo import PreselectionBagItemsRepo, construct_postgres_preselection_bag_items_repo
from infrastructure.bag_repo import BagRepo, construct_postgres_bag_repo
from infrastructure.item_repo import ItemRepo, construct_postgres_item_repo
from infrastructure.inventory_repo import InventoryRepo, construct_postgres_inventory_repo
from infrastructure.inventory_transaction_repo import InventoryTransactionRepo, construct_postgres_inventory_transaction_repo
from infrastructure.shipment_repo import ShipmentRepo, construct_postgres_shipment_repo
from infrastructure.fulfillment_method_repo import FulfillmentMethodRepo, construct_postgres_fulfillment_method_repo
from infrastructure.coupon_repo import CouponRepo, construct_postgres_coupon_repo
from infrastructure.async_work_management import AsyncWorkManager, AsyncWorkManagementMiddleware


# Add in falcon setup here
def create_api():
    logging.basicConfig(level=logging.INFO)

    database_url = get("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is not set")

    work_manager = AsyncWorkManager(PostgresTransactable(database_url))
    work_manager.register(CustomerRepo, construct_postgres_customer_repo)
    work_manager.register(OrderItemRepo, construct_postgres_order_item_repo)
    work_manager.register(OrderRepo, construct_postgres_order_repo)
    work_manager.register(PreselectionRepo, construct_postgres_preselection_repo)
    work_manager.register(PreselectionBagItemsRepo, construct_postgres_preselection_bag_items_repo)
    work_manager.register(BagRepo, construct_postgres_bag_repo)
    work_manager.register(ItemRepo, construct_postgres_item_repo)
    work_manager.register(InventoryRepo, construct_postgres_inventory_repo)
    work_manager.register(InventoryTransactionRepo, construct_postgres_inventory_transaction_repo)
    work_manager.register(ShipmentRepo, construct_postgres_shipment_repo)
    work_manager.register(FulfillmentMethodRepo, construct_postgres_fulfillment_method_repo)
    work_manager.register(CouponRepo, construct_postgres_coupon_repo)
    
    cors_allowed_origins = get("CORS_ALLOWED_ORIGINS").split(";")

    app = asgi.App(
        middleware=[
            CORSMiddleware(
                allow_origins=cors_allowed_origins,
                allow_credentials=cors_allowed_origins,
            ),
            AsyncWorkManagementMiddleware(work_manager)
        ]
    )

    json_handler = media.JSONHandler(
        dumps=functools.partial(simplejson.dumps, default=json_dumps_default),
        loads=functools.partial(simplejson.loads, parse_float=Decimal),
    )

    extra_handlers = {
        MEDIA_JSON: json_handler,
    }

    app.req_options.media_handlers.update(extra_handlers)
    app.resp_options.media_handlers.update(extra_handlers)

    app.add_sink(
        HealthCheckRequestHandler(),
        prefix=re.compile("^/health-check(?P<path>/?.*)$"),
    )

    app.add_sink(
        AddressRequestHandler(),
        prefix=re.compile("^/address(?P<path>/?.*)$"),
    )

    app.add_sink(
        CompleteOrderRequestHandler(work_manager),
        prefix=re.compile("^/complete-order(?P<path>/?.*)$"),
    )

    app.add_sink(
        CompletePickupOrderRequestHandler(work_manager),
        prefix=re.compile("^/complete-pickup-order(?P<path>/?.*)$"),
    )

    app.add_sink(
        PaymentRequestHandler(work_manager),
        prefix=re.compile("^/payment(?P<path>/?.*)$"),
    )

    app.add_sink(
        PreselectionRequestHandler(work_manager),
        prefix=re.compile("^/preselections(?P<path>/?.*)$"),
    )

    app.add_sink(
        BagRequestHandler(work_manager),
        prefix=re.compile("^/bags(?P<path>/?.*)$"),
    )

    app.add_sink(
        ItemRequestHandler(work_manager),
        prefix=re.compile("^/items(?P<path>/?.*)$"),
    )

    app.add_sink(
        InventoryRequestHandler(work_manager),
        prefix=re.compile("^/inventories(?P<path>/?.*)$"),
    )

    app.add_sink(
        InventoryTransactionRequestHandler(work_manager),
        prefix=re.compile("^/inventory-transactions(?P<path>/?.*)$"),
    )

    app.add_sink(
        CustomerRequestHandler(work_manager),
        prefix=re.compile("^/customers(?P<path>/?.*)$"),
    )

    app.add_sink(
        OrderRequestHandler(work_manager),
        prefix=re.compile("^/orders(?P<path>/?.*)$"),
    )

    app.add_sink(
        OrderItemRequestHandler(work_manager),
        prefix=re.compile("^/order-items(?P<path>/?.*)$"),
    )

    app.add_sink(
        ShipmentRequestHandler(work_manager),
        prefix=re.compile("^/shipments(?P<path>/?.*)$"),
    )

    app.add_sink(
        FulfillmentMethodRequestHandler(work_manager),
        prefix=re.compile("^/fulfillment-methods(?P<path>/?.*)$"),
    )

    app.add_sink(
        CouponRequestHandler(work_manager),
        prefix=re.compile("^/coupons(?P<path>/?.*)$"),
    )

    app.add_sink(
        ImageRequestHandler(work_manager),
        prefix=re.compile("^/images(?P<path>/?.*)$"),
    )

    return app
