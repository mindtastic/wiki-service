from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from wiki_service.db.mongo import connect_to_mongo, close_mongo_connection
from wiki_service.errors.http_error import http_error_handler
from wiki_service.errors.validation_error import http_request_validation_error_handler

from wiki_service.core.settings import Settings

def create_wiki_service() -> FastAPI:
    settings = Settings()
    settings.configure_logging()
    
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowedHost,
        allow_credential=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    app.add_event_handler('startup', connect_to_mongo)
    app.add_event_handler('shutdown', close_mongo_connection)

    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http_request_validation_error_handler)

    return app

wiki_service = create_wiki_service()
