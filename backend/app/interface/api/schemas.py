from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import re
from pydantic import field_validator

class CreateUserRequest(BaseModel):
    phone_number: str
    name: Optional[str] = None
    
    @field_validator("phone_number")
    @classmethod
    def check_method(cls, v):
        if not re.fullmatch(r"\+234[789]\d{9}", v):
            raise ValueError("Phone number must be in +234 format")
        return v
    
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
    
    @field_validator("counterparty_phone")
    @classmethod
    def check_method(cls, v):
        if not re.fullmatch(r"\+234[789]\d{9}", v):
            raise ValueError("Phone number must be in +234 format")
        return v

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

class AgreementListItem(AgreementResponse):
    other_party_name: Optional[str] = None
    other_party_phone_number: Optional[str] = None