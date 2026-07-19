from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from .models import UserDocument, AgreementDocument
from dotenv import load_dotenv
import os

load_dotenv()
async def init_db():
    mongo_url = os.getenv("MONGO_URL")
    if not mongo_url:
        raise ValueError("Cannot establish databse connection")
    
    client = AsyncIOMotorClient(mongo_url)
    
    await init_db(
        database = client.get_default_database(),
        document_models = [UserDocument, AgreementDocument]
    )