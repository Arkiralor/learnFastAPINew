from fastapi import APIRouter

from helpers.auth import UserModelHelpers
from schema.auth import UserRegisterSchema, UserRegisterOutputSchema

from controllers import logger

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@auth_router.get("/user", response_model=UserRegisterOutputSchema)
async def get_user(user_id: str) -> UserRegisterOutputSchema:
    """
    Get user by ID.
    """
    logger.info(f"{user_id=}")
    user = UserModelHelpers.get_one(user_id)
    return UserRegisterOutputSchema(**user.model_dump())

@auth_router.post("/register/", response_model=UserRegisterOutputSchema, status_code=201)
async def register_user(user: UserRegisterSchema) -> UserRegisterOutputSchema:
    """
    Register a new user.
    """
    user = await UserModelHelpers.create_user(user)
    return user