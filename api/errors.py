from typing import Any

import falcon

class RFC7807Error(falcon.HTTPError):
    status_code: int
    type: str | None = None
    title: str | None = None
    detail: str | None = None
    extra: dict[str, Any] | None = None

    def __init__(
        self,
        *,
        status_code: int | None = None,
        type: str | None = None,
        title: str | None = None,
        detail: str | None = None,
        extra: dict[str, Any] = {}
    ):
        # Get the class-defined status_code if none was provided
        if status_code is None:
            status_code = getattr(self, "status_code", None)
        
        if status_code is None:
            raise ValueError("status_code must be provided.")
        
        self.status_code = status_code  # Always set the instance attribute
        self.type = type
        self.extra = extra

        status = getattr(falcon, f"HTTP_{status_code}")
        super().__init__(status=status, title=title, description=detail)
    
    def to_dict(self, obj_type=dict):
        obj = obj_type()

        obj["status"] = self.status_code

        if self.title is not None:
            obj["title"] = self.title
        
        if self.type is not None:
            obj["type"] = self.type
        
        if self.description is not None:
            obj["detail"] = self.description
        
        if self.extra is not None:
            obj.update(self.extra)
        
        return obj


class NotFound(RFC7807Error):
    status_code = 404
    title = "Not found."


class ValidationError(RFC7807Error):
    status_code = 400
    title = "The request body was not valid."
