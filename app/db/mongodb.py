from motor.motor_asyncio import AsyncIOMotorClient

from app.core.settings import settings

mongo_client = AsyncIOMotorClient(settings.mongodb_url)

database = mongo_client[settings.database_name]