from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone
from .enums import AgreementStatus 

#user entity
@dataclass
class User: 
    phone_number: str
    wallet_address: str
    enctypted_private_key: str
    id: Optional[str] = None
    name: Optional[str] = None
    created_at: datetime = field(default_factory = lambda: datetime.now(timezone.utc))

#agreement entity
@dataclass
class Agreement: 
    title: str
    terms: str
    creator_id: str
    counterparty_id: str
    fingerprint_hash: str #hashed fingerprint being sent to monad
    creator_signed: bool = True
    counterparty_signed: bool = False 
    tx_hash: Optional[str] = None #transaction hash being returned from monad 
    price: Optional[float] = None
    id: Optional[str] = None
    status: AgreementStatus = AgreementStatus.PENDING
    created_at: datetime = field(default_factory = lambda: datetime.now(timezone.utc))
    confirmed_at: Optional[datetime] = None
