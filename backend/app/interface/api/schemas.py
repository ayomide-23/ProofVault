from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateUserRequest(BaseModel):
    phone_number: str
    name: Optional[str] = None
    
class UserResponse(BaseModel): 
    id: str
    phone_number: str
    name: Optional[str] = None
    wallet_address: str

class CreateAgreementRequest(BaseModel):
    title: str
    terms: str
    creator_id: str
    counterparty_phone: str
    price: Optional[float] = None

class SignAgreementRequest(BaseModel):
    signer_id: str   
    
class AgreementResponse(BaseModel):
    id: str
    title:str
    terms:str
    creator_id: str
    counterparty_id: str
    price: Optional[float] = None
    creator_signed: bool
    counterparty_signed: bool
    fingerprint_hash: str
    tx_hash: Optional[str] = None
    created_at: datetime
    status:str
    confirmed_at: Optional[datetime] = None