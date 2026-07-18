from enum import Enum

#agreement status enum 
class AgreementStatus(str, Enum):
    PENDING= "pending"
    CONFIRMED = "confirmed"
    DISPUTED = "disputed"