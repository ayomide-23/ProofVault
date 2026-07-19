import hashlib
from typing import Optional
from app.domain.repositories import AgreementRepository, UserRepository
from app.domain.entities import Agreement

class CreateAgreementUseCase:
    def __init__(self, agreement_repository: AgreementRepository, user_repository: UserRepository):  #getting the repositories needed for saving the agreement and other operations
        self.agreement_repository = agreement_repository
        self.user_repository = user_repository
        
    async def execute(self, title: str, terms: str, creator_id: str, phone_number: str, price: Optional[str] = None) -> Agreement: 
        #checking if the counterparty already exists in the database using their phone number
        counterparty = await self.user_repository.get_by_phone(phone_number)
        if counterparty is None:
            raise ValueError("CounterParty not found.")
        
        finger_print_hash = hashlib.sha256(terms.encode()).hexdigest()  #creating a unique fingerprint hash of the agreement terms using sha256 hashing algorithm
        agreement = Agreement(
            title=title,
            terms=terms,
            fingerprint_hash=finger_print_hash,
            creator_id=creator_id,
            counterparty_id=counterparty.id,
            price=price
        )
        return await self.agreement_repository.save(agreement)  #saving the agreement to the database and returning it