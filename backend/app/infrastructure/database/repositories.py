from typing import Optional
from beanie import PydanticObjectId
from app.domain.repositories import UserRepository, AgreementRepository
from .models import UserDocument, AgreementDocument
from app.domain.entities import User, Agreement

def _user_doc_to_entity(doc: UserDocument) -> User: #translates the userdocument to entity user
    return User(
        id=str(doc.id),
        phone_number=doc.phone_number,
        wallet_address=doc.wallet_address,
        enctypted_private_key=doc.enctypted_private_key,
        name=doc.name,
        created_at=doc.created_at
    )
    
class MongoUserRepository(UserRepository):
    async def save(self, user: User) -> User: #saves a user to the database and returns the saved user
        doc = UserDocument(
            phone_number=user.phone_number,
            wallet_address=user.wallet_address,
            enctypted_private_key=user.enctypted_private_key,
            name=user.name
        )
        await doc.insert()
        return _user_doc_to_entity(doc)
    async def get_by_id(self, user_id: str) -> Optional[User]: #retrieves a user from the database by their ID
        doc = await UserDocument.get(PydanticObjectId(user_id))
        return _user_doc_to_entity(doc) if doc else None
    async def get_by_phone(self, phone_number: str) -> Optional[User]: #retrieves a user from the database by their phone number
        doc = await UserDocument.find_one(UserDocument.phone_number == phone_number)
        return _user_doc_to_entity(doc) if doc else None
    
def _agreement_doc_to_entity(doc: AgreementDocument) -> Agreement:
    return Agreement(
        id=str(doc.id),
        title=doc.title,
        terms=doc.terms,
        creator_id=doc.creator_id,
        counterparty_id=doc.counterparty_id,
        price=doc.price,
        creator_signed=doc.creator_signed,
        counterparty_signed=doc.counterparty_signed,
        fingerprint_hash=doc.fingerprint_hash,
        tx_hash=doc.tx_hash,
        status=doc.status,
        created_at=doc.created_at,
        confirmed_at=doc.confirmed_at
    )
    
class MongoAgreementRepository(AgreementRepository):
    async def save(self, agreement: Agreement) -> Agreement:
        doc = AgreementDocument(
            title=agreement.title,
            terms=agreement.terms,
            creator_id=agreement.creator_id,
            counterparty_id=agreement.counterparty_id,
            price=agreement.price,
            creator_signed=agreement.creator_signed,
            counterparty_signed=agreement.counterparty_signed,
            fingerprint_hash=agreement.fingerprint_hash,
            tx_hash=agreement.tx_hash,
            status=agreement.status
        )
        await doc.insert()
        return _agreement_doc_to_entity(doc)
    async def get_by_id(self, agreement_id: str) -> Optional[Agreement]:
        doc = await AgreementDocument.get(PydanticObjectId(agreement_id))
        return _agreement_doc_to_entity(doc) if doc else None
    async def update(self, agreement: Agreement) -> Agreement:
        doc = await AgreementDocument.get(PydanticObjectId(agreement.id))
        if not doc:
            raise ValueError("Agreement not found")
        doc.title = agreement.title
        doc.terms = agreement.terms
        doc.creator_id = agreement.creator_id
        doc.counterparty_id = agreement.counterparty_id
        doc.price = agreement.price
        doc.creator_signed = agreement.creator_signed
        doc.counterparty_signed = agreement.counterparty_signed
        doc.fingerprint_hash = agreement.fingerprint_hash
        doc.tx_hash = agreement.tx_hash
        doc.status = agreement.status
        doc.confirmed_at = agreement.confirmed_at
        await doc.save()
        return _agreement_doc_to_entity(doc)