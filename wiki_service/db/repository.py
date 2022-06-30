from abc import ABC, abstractmethod
from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection
)

class Repository(ABC):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.col: AsyncIOMotorCollection = db[self.collection]

    @property
    @abstractmethod
    def collection(self):
        pass
