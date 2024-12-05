import functools
import logging
import re
from decimal import Decimal
from utils.config import get

import simplejson
from falcon import MEDIA_JSON, asgi, CORSMiddleware, media

from core.api.health_check import HealthCheckRequestHandler
from core.api.address import AddressRequestHandler
from core.api.complete_order import CompleteOrderRequestHandler
from core.api.payment_method import PaymentMethodRequestHandler
from utils.json_dumps_default import json_dumps_default

from infrastructure.postgres import PostgresTransactable
from infrastructure.user import UserRepo, construct_postgres_user_repo
from infrastructure.work_management import WorkManager


# Add in falcon setup here
def create_api():
    logging.basicConfig(level=logging.INFO)

    database_url = get("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is not set")

    work_manager = WorkManager(PostgresTransactable(database_url))
    work_manager.register(UserRepo, construct_postgres_user_repo)
    
    cors_allowed_origins = get("signup_cors_allowed_origins").split(";")

    app = asgi.App(
        middleware=[
            CORSMiddleware(
                allow_origins=cors_allowed_origins,
                allow_credentials=cors_allowed_origins,
            )
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

    return app
