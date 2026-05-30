from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_manager = Database()

def get_db():
    return db_manager.db

async def connect_to_mongo():
    db_manager.client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        tlsAllowInvalidCertificates=True
    )
    db_manager.db = db_manager.client["portfolio_db"]
    print("Connected to MongoDB Atlas! 🍃")

async def close_mongo_connection():
    db_manager.client.close()
    print("MongoDB connection closed.")
