from abc import ABC, abstractmethod
from typing import Optional
from .entities import Agreement, User
#abc stands for abstract base class
#other classes will inherit from this class and implement its abstract methods
#every blockchain service  being sent to the onchain should implement this class and its methods
class BlockChainService(ABC):
    #implement this function if using a blockchain service
    @abstractmethod #every blockchain method should have a record management
    async def record_agreement(
        self,
        signer_private_Key: str, #private key of the signer which authorizes the signing of the agreement that will be sent to monad i.e it doesnt get sent to monad
        fingerprint_hash: str, #unique hash of the agreement being sent to the blockchain
        counterparty_wallet_address: str, #wallet address of the counterparty
        creator_wallet_address: str, #wallet address of the creator
        ) -> str:
        """Signs and sends the agreement confirmation onchain. Returns the returned_fingerprint_hash."""
        
class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        """Saves a user to the database and returns the saved user."""
        
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Retrieves a user from the database by their ID. Returns None if not found."""
        
    @abstractmethod
    async def get_by_phone(self, phone_number: str) -> Optional[User]:
        """Retrieves a user from the database by their phone number. Returns None if not found."""

class AgreementRepository(ABC):
    @abstractmethod
    async def save(self, agreement: Agreement) -> Agreement:
        """Saves an agreement to the database and returns the saved agreement."""
        
    @abstractmethod
    async def get_by_id(self, agreement_id: str) -> Optional[Agreement]:
        """Retrieves an agreement from the database by its ID. Returns None if not found."""
        
    @abstractmethod
    async def update(self, agreement: Agreement) -> Agreement:
        """Updates an existing agreement in the database and returns the updated agreement."""