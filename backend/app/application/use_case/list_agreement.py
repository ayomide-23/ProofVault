from app.domain.repositories import AgreementRepository

class ListAgreementUseCase:
    def __init__(self, agreement_repository: AgreementRepository):
        self.agreement_repository = agreement_repository
    async def execute(self, user_id: str):
        return await self.agreement_repository.get_by_user(user_id)