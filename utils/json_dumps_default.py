import dataclasses
import datetime
import enum
import uuid
from utils.camelize import camelize


def json_dumps_default(o):
    if dataclasses.is_dataclass(o):
        return camelize(dataclasses.asdict(o))

    if isinstance(o, datetime.date):
        return o.isoformat()

    if isinstance(o, uuid.UUID):
        return str(o)

    if isinstance(o, enum.Enum):
        return o.value

    raise TypeError("Object of type %s is not JSON serializable" % type(o))
