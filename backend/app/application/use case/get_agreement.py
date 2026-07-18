from app.domain.repositories import AgreementRepository
from app.domain.entities import Agreement

class GetAgreementUseCase:
    def __init__(self, agreement_repository: AgreementRepository):
        self.agreement_repository = agreement_repository

    async def execute(self, agreement_id: str) -> Agreement:
        agreement = await self.agreement_repository.get_by_id(agreement_id)
        if not agreement: 
            raise ValueError("Agreement not found")
        return agreement