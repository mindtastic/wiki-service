from typing import Union

from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

async def http_request_validation_error_handler(
    _: Request, 
    exc: Union[ValidationError, RequestValidationError]
) -> JSONResponse:
    return JSONResponse(
        {"error": exc.errors()},
        status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )
