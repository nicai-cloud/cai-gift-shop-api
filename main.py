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
from api.item import ItemRequestHandler
from api.payment_method import PaymentMethodRequestHandler
from api.preselection import PreselectionRequestHandler
from api.inventory import InventoryRequestHandler
from api.customer import CustomerRequestHandler
from api.order import OrderRequestHandler
from api.order_item import OrderItemRequestHandler
from utils.json_dumps_default import json_dumps_default

from infrastructure.postgres import PostgresTransactable
from infrastructure.customer_repo import CustomerRepo, construct_postgres_customer_repo
from infrastructure.order_repo import OrderRepo, construct_postgres_order_repo
from infrastructure.order_item_repo import OrderItemRepo, construct_postgres_order_item_repo
from infrastructure.preselection_repo import PreselectionRepo, construct_postgres_preselection_repo
from infrastructure.bag_repo import BagRepo, construct_postgres_bag_repo
from infrastructure.item_repo import ItemRepo, construct_postgres_item_repo
from infrastructure.inventory_repo import InventoryRepo, construct_postgres_inventory_repo
from infrastructure.inventory_transaction_repo import InventoryTransactionRepo, construct_postgres_inventory_transaction_repo
from infrastructure.work_management import WorkManager, WorkManagementMiddleware


# Add in falcon setup here
def create_api():
    logging.basicConfig(level=logging.INFO)

    database_url = get("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is not set")

    work_manager = WorkManager(PostgresTransactable(database_url))
    work_manager.register(CustomerRepo, construct_postgres_customer_repo)
    work_manager.register(OrderItemRepo, construct_postgres_order_item_repo)
    work_manager.register(OrderRepo, construct_postgres_order_repo)
    work_manager.register(PreselectionRepo, construct_postgres_preselection_repo)
    work_manager.register(BagRepo, construct_postgres_bag_repo)
    work_manager.register(ItemRepo, construct_postgres_item_repo)
    work_manager.register(InventoryRepo, construct_postgres_inventory_repo)
    work_manager.register(InventoryTransactionRepo, construct_postgres_inventory_transaction_repo)
    
    cors_allowed_origins = get("fe_cors_allowed_origins").split(";")

    app = asgi.App(
        middleware=[
            CORSMiddleware(
                allow_origins=cors_allowed_origins,
                allow_credentials=cors_allowed_origins,
            ),
            WorkManagementMiddleware(work_manager)
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
        PaymentMethodRequestHandler(),
        prefix=re.compile("^/payment-method(?P<path>/?.*)$"),
    )

    app.add_sink(
        PreselectionRequestHandler(work_manager),
        prefix=re.compile("^/preselection(?P<path>/?.*)$"),
    )

    app.add_sink(
        BagRequestHandler(work_manager),
        prefix=re.compile("^/bag(?P<path>/?.*)$"),
    )

    app.add_sink(
        ItemRequestHandler(work_manager),
        prefix=re.compile("^/item(?P<path>/?.*)$"),
    )

    app.add_sink(
        InventoryRequestHandler(work_manager),
        prefix=re.compile("^/inventory(?P<path>/?.*)$"),
    )

    app.add_sink(
        CustomerRequestHandler(work_manager),
        prefix=re.compile("^/customer(?P<path>/?.*)$"),
    )

    app.add_sink(
        OrderRequestHandler(work_manager),
        prefix=re.compile("^/order(?P<path>/?.*)$"),
    )

    app.add_sink(
        OrderItemRequestHandler(work_manager),
        prefix=re.compile("^/order-item(?P<path>/?.*)$"),
    )

    return app
