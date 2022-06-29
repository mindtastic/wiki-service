from abc import ABC, abstractmethod
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

class Migration(ABC):
    @property 
    @abstractmethod
    def timestamp(self) -> datetime:
        pass
        
    @property
    def name(self) -> str:
        type(self).__name__

    @abstractmethod
    async def migrate(self, db: AsyncIOMotorDatabase) -> None:
        pass

    @classmethod
    def is_abstract(cls) -> bool:
        return bool(getattr(cls, "__abstractmethods__", False))
