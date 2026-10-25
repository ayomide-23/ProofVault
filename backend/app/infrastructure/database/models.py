from beanie import Document
from datetime import datetime, timezone
from pydantic import Field
from typing import Optional 
from pymongo import IndexModel, ASCENDING
from app.domain.enums import AgreementStatus

class UserDocument(Document):
    phone_number: str
    name: Optional[str] = None
    wallet_address: str
    enctypted_private_key: str
    created_at: datetime =  Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "users" #name of the collection in the database
        indexes = [IndexModel([("phone_number", ASCENDING)], unique = True)]
        
class AgreementDocument(Document):
    title: str
    terms: str
    creator_id: str
    counterparty_id: str
    price: Optional[float] = None
    creator_signed: bool = True
    counterparty_signed: bool = False 
    fingerprint_hash: str 
    tx_hash: Optional[str] = None 
    status: AgreementStatus = AgreementStatus.PENDING
    created_at: datetime =  Field(default_factory=lambda: datetime.now(timezone.utc))
    confirmed_at: Optional[datetime] = None
    
    class Settings: 
        name = "agreements" #name of the collection in the database
