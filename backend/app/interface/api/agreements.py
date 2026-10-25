from fastapi import APIRouter, HTTPException, Request
from app.interface.api.schemas import CreateAgreementRequest, SignAgreementRequest, AgreementResponse, AgreementListItem

def __to_response(agreement) -> AgreementResponse:
    return AgreementResponse(
        id =agreement.id,
        title =agreement.title,
        terms =agreement.terms,
        creator_id =agreement.creator_id,
        counterparty_id =agreement.counterparty_id,
        price =agreement.price,
        creator_signed =agreement.creator_signed,
        counterparty_signed =agreement.counterparty_signed,
        fingerprint_hash =agreement.fingerprint_hash,
        tx_hash = agreement.tx_hash,
        status = agreement.status,
        created_at = agreement.created_at,
        confirmed_at = agreement.confirmed_at,
    )

#route to create a new agreement in the database and return the created agreement as a response
router = APIRouter(prefix="/agreements",tags=["agreements"])
@router.post("/", response_model=AgreementResponse)
async def create_agreement(request: Request, agreement_request: CreateAgreementRequest):
    use_case = request.app.state.create_agreement_use_case
    try: 
        agreement = await use_case.execute(
            title= agreement_request.title,
            terms = agreement_request.terms,
            creator_id = agreement_request.creator_id,
            counterparty_phone = agreement_request.counterparty_phone,
            price = agreement_request.price
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return __to_response(agreement)
@router.get("/", response_model=list[AgreementListItem])
async def list_agreements(user_id: str, request: Request):
    use_case = request.app.state.list_agreement_use_case
    results = await use_case.execute(user_id)
    return[
        AgreementListItem(
            **__to_response(agreement).model_dump(),
            other_party_name=other.name if other else None,
            other_party_phone_number=other.phone_number if other else None
        )
        for agreement, other in results
    ]
#route to sign an existing agreement in the database and return the updated agreement as a response
@router.post("/{agreement_id}/sign", response_model=AgreementResponse)
async def sign_agreement(request: Request, agreement_id: str, sign_request: SignAgreementRequest):
    use_case = request.app.state.sign_agreement_use_case
    try:
        agreement = await use_case.execute(agreement_id=agreement_id, signer_id=sign_request.signer_id)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return __to_response(agreement)

@router.get("/{agreement_id}", response_model=AgreementResponse)
async def get_agreement(agreement_id: str, request: Request):
    use_case = request.app.state.get_agreement_use_case
    try:
        agreement = await use_case.execute(agreement_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return __to_response(agreement)