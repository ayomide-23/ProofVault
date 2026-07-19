from typing import Optional
from app.domain.repositories import UserRepository
from app.domain.entities import User
from app.infrastructure.securtiy.encryption import encrypt_key
from eth_account import Account
class CreateUserUseCase: 
    def __init__(self, user_repository: UserRepository): #getting the repository it needs to use to save the user to the database
        self.user_repository = user_repository
        
    async def execute(self, phone_number: str, name: Optional[str] = None) -> User:
        existing_user = await self.user_repository.get_by_phone(phone_number) #getting the existing user phone number from the db to check if they exist
        if existing_user: 
            raise existing_user
         
        account = Account.create() #creating a new ethereum account
        encrypted_key = encrypt_key(account.key.hex()) #encrypting the user's private key
        
        user = User(
            phone_number = phone_number,
            wallet_address = account.address,
            enctypted_private_key = encrypted_key,
            name = name
        )
        return await self.user_repository.save(user)