from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from config.globals import settings
import logging

logger = logging.getLogger(__name__)

client = MongoClient(settings.MONGO_URI, tz_aware=True)
sync_database = client[settings.MONGO_DB]
client = AsyncIOMotorClient(settings.MONGO_URI, tz_aware=True)
async_database = client.get_database(settings.MONGO_DB)