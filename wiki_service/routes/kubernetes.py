from fastapi.routing import APIRouter
from loguru import logger
from starlette import status

router = APIRouter()

@router.get('/health', status_code=status.HTTP_200_OK)
async def health():
    logger.debug('Received health check request')   
