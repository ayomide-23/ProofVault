from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone
from .enums import AgreementStatus 

#user entity
@dataclass
class User: 
    id: Optional[str] = None
    name: Optional[str] = None
    phone_number: str
    wallet_address: str
    enctypted_private_key: str
    created_at: datetime = field(default_factory = lambda: datetime.now(timezone.utc))

#agreement entity
@dataclass
class Agreement: 
    id: Optional[str] = None
    title: str
    terms: str
    creator_id: str
    counterparty_id: str
    price: Optional[float] = None
    creator_signed: bool = True
    counterparty_signed: bool = False 
    fingerprint_hash: str #hashed fingerprint being sent to monad
    tx_hash: Optional[str] = None #transaction hash being returned from monad 
    status: AgreementStatus = AgreementStatus.PENDING
    created_at: datetime = field(default_factory = lambda: datetime.now(timezone.utc))
    confirmed_at: Optional[datetime] = None
