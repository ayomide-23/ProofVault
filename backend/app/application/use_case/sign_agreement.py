from datetime import datetime, timezone
from app.domain.entities import User , Agreement
from app.domain.repositories import UserRepository, AgreementRepository, BlockChainService
from app.domain.rules import can_sign
from app.domain.enums import AgreementStatus

class SignAgreementUseCase:
    def __init__(self, user_repository: UserRepository, agreement_repository: AgreementRepository, blockchain_service: BlockChainService):
        self.user_repository = user_repository,
        self.agreement_repository = agreement_repository,
        self.blockchain_service = blockchain_service
    #checking if the agreement exists
    async def execute(self, agreement_id: str, signer_id: str) -> Agreement:
        agreement = await self.agreement_repository.get_by_id(agreement_id)
        if not agreement:
            raise ValueError("Agreement not found")
        #checking if the counterparty is allowed to sign the agreement
        if not can_sign(agreement, signer_id):
            raise ValueError("User not allowed to sign agreement")
        #retrieving the signer's and creator's info from the database
        signer = await self.user_repository.get_by_id(signer_id) #fetching the signer's record via id
        creator = await self.user_repository.get_by_id(agreement.creator_id) #fetching the creator's record via id
        if signer is None or creator is None:
            raise ValueError("User not found")
        #recording the agreement on the blockchain
        tx_hash = await self.blockchain_service.record_agreement(
            signer_private_key= signer.enctypted_private_key, #the signer's private key is used to sign the agreement on the blockchain
            fingerprint_hash=agreement.fingerprint_hash, #the unique hash of the agreement being sent to the blockchain
            counterparty_wallet_address=signer.wallet_address, #the wallet address of the counterparty signing the agreement
            creator_wallet_address=creator.wallet_address #the wallet address of the creator of the agreement
        )
        agreement.counterparty_signed = True 
        agreement.tx_hash = tx_hash #the transaction hash returned from the blockchain after recording the agreement
        agreement.status = AgreementStatus.CONFIRMED #updating the status of the agreement to confirmed after it has been signed and recorded on the blockchain
        agreement.confirmed_at = datetime.now(timezone.utc) #recording the time when the agreement was confirmed
        return await self.agreement_repository.update(agreement) #updating the agreement in the database with the new status and transaction