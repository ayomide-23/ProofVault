from fastapi import APIRouter, Request
from app.interface.api.schemas import CreateUserRequest, UserResponse

router = APIRouter(prefix="/users", tags=["users"])
#route to create a new user in the database and return the created user as a response
@router.post("/", response_model=UserResponse)
async def create_user(request: Request, user_request: CreateUserRequest):
    use_case = request.app.state.create_user_use_case
    user = await use_case.execute(user_request.phone_number, user_request.name)
    return UserResponse(
        id=user.id,
        phone_number = user.phone_number,
        name=user.name,
        wallet_address= user.wallet_address
    )