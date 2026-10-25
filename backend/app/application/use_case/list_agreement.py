from app.domain.repositories import AgreementRepository, UserRepository

class ListAgreementUseCase:
    def __init__(self, agreement_repository: AgreementRepository, user_repository: UserRepository):
        self.agreement_repository = agreement_repository
        self.user_repository = user_repository
        
    async def execute(self, user_id: str):
        agreements = await self.agreement_repository.get_by_user(user_id)
        
        def other_id(a):
            return a.counterparty_id if a.creator_id == user_id else a.creator_id
        others = {}
        for oid in {other_id(a) for a in agreements}:
            others[oid] = await self.user_repository.get_by_id(oid)
        return [(a, others[other_id(a)]) for a in agreements]