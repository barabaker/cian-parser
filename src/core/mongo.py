import motor.motor_asyncio
from core.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo.dsn)
database = client[settings.mongo.db_name]