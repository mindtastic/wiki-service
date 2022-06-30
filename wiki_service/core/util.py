import os
from typing import Dict
from loguru import logger
from pymongo.uri_parser import parse_uri
from pymongo.errors import InvalidURI
from urllib.parse import quote_plus
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse

def aliased_response(model: BaseModel) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(model, by_alias=True))

class MongoConnectionSettings:
    connection_str: str
    username: str
    password: str
    database: str

    def __init__(self, connection_str: str, user: str, password: str, db: str):
        self.connection_str = connection_str
        self.user = user
        self.password = password
        self.database = db

    def connection_string(self) -> str:
        return self.connection_str

    @classmethod
    def create_from_environment(cls):
        connection_string = os.getenv('CONNECTION_STRING', None)
        if connection_string is None:
            connection_string = cls.connection_string_from_env()
            logger.info('Build connection string {}', connection_string)
        
        parsed = cls.parse_connection_string(connection_string)
        return cls(
            connection_string,
            parsed['username'] or '',
            parsed['password'] or '',
            parsed['database'] or ''
        )

    @staticmethod
    def parse_connection_string(connection_string: str) -> Dict:
        try:
            return parse_uri(connection_string)
        except InvalidURI:
            # If the string is invalid, parse a definitly working url and drop the provided components.
            # So this method always returns a valid parse_dictionary
            parsed = parse_uri('mongodb://127.0.0.1')
            parsed['nodelist'] = []
            return parsed
    
    @staticmethod
    def connection_string_from_env() -> str:
        return "mongodb://%s:%s@%s/%s?authSource=%s" % (
                quote_plus(os.getenv('MONGODB_USER', 'admin')),
                quote_plus(os.getenv('MONGODB_PASSWORD', 'admin')),
                quote_plus(os.getenv('MONGODB_HOST', 'mongo_wiki')),
                quote_plus(os.getenv('MONGODB_DB', 'wiki')),
                quote_plus(os.getenv('MONGODB_AUTHSOURCE', 'admin'))
            )
