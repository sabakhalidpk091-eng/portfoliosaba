import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

async def test():
    uri = "mongodb+srv://portfolio:q6bcEVLl57qUb812@cluster0.zvhw8ay.mongodb.net/portfolio_db?retryWrites=true&w=majority&appName=Cluster0"
    print(f"Connecting to: {uri}")
    client = AsyncIOMotorClient(uri)
    try:
        # The ismaster command is cheap and does not require auth.
        await client.admin.command('ismaster')
        print("MongoDB Connection Successful!")
    except Exception as e:
        print(f"MongoDB Connection Failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test())
