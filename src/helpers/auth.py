from fastapi import status
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from schema.auth import UserRegisterSchema, UserRegisterOutputSchema, UserPasswordLoginSchema, AuthTokenSchema, UserGenericInfoSchema,\
TokenBlacklistSchema
from models.auth import User
from database.collections import DatabaseCollections
from database.methods import AsynchronousMethods, SynchronousMethods
import hmac
from hashlib import sha256
from config.globals import settings
import re
from constants import FormatRegex
from helpers import logger
from exceptions import NotFoundException
from bson import ObjectId
from utils.json_web_token import create_access_token, create_refresh_token, blacklist_token, get_token_from_header, get_user_from_access_token \
    , get_user_from_refresh_token


class UserModelHelpers:

    @classmethod
    def get_one(cls, user_id: str) -> User:
        """
        Get a user by ID.
        """
        if not user_id:
            raise ValueError("User ID is required")

        user = SynchronousMethods.find_one(
            _id=ObjectId(user_id),
            collection=DatabaseCollections.USERS
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found")
        return User(**user) if user else None

    @classmethod
    def hash_password(cls, entered_password: str) -> str:
        """
        Hash the password using HMAC with SHA256.
        """
        return hmac.new(
            key=settings.SECRET_KEY.encode(),
            msg=entered_password.encode(),
            digestmod=sha256
        ).hexdigest()

    @classmethod
    def verify_password(cls, entered_password: str, user: User) -> bool:
        """
        Verify the entered password against the stored hashed password.
        """
        return hmac.compare_digest(
            cls.hash_password(entered_password),
            user.password
        )

    @classmethod
    async def user_exists(cls, username: str, email: str) -> bool:
        """
        Check if a user with the given username or email already exists.
        """
        if not username and not email:
            raise ValueError("Either username or email must be provided")

        filter_dict = {}
        if username:
            filter_dict = {
                "username": username
            }
        if email:
            filter_dict = {
                "email": email
            }
        if username and email:
            filter_dict = {
                "$or": [
                    {"username": username},
                    {"email": email}
                ]
            }

        return SynchronousMethods.exists(
            filter_dict=filter_dict,
            collection=DatabaseCollections.USERS
        )

    @classmethod
    async def create_user(cls, data: UserRegisterSchema) -> UserRegisterOutputSchema:
        """
        Create a new user in the database.
        """
        if not data.username or not data.email or not data.password:
            raise ValueError("Username, email, and password are required")

        if await cls.user_exists(username=data.username, email=data.email):
            raise ValueError("User with this username or email already exists")

        if settings.DEBUG:
            print(
                f"Creating user with username: {data.username}, password: {data.password} and email: {data.email}")
        data.password = cls.hash_password(data.password)
        if not re.match(FormatRegex.EMAIL_REGEX, data.email):
            raise ValueError("Invalid email format")
        user = User(**data.model_dump())
        user: User = SynchronousMethods.insert_one(
            collection=DatabaseCollections.USERS,
            data=user.model_dump(by_alias=True)
        )
        return UserRegisterOutputSchema(**user)

    @classmethod
    def create_auth_tokens(cls, user: User) -> AuthTokenSchema:
        """
        Create authentication tokens for the user.
        """
        access = create_access_token(user)
        refresh = create_refresh_token(user)

        return {"access": access, "refresh": refresh}

    @classmethod
    def login_user_password(cls, data: UserPasswordLoginSchema) -> AuthTokenSchema:
        user: User = SynchronousMethods.find(
            filter_dict={"email": data.email},
            collection=DatabaseCollections.USERS
        )

        if not user:
            raise ValueError("User not found")

        tokens = cls.create_auth_tokens(user)

        if not cls.verify_password(data.password, user):
            user.login_attempts += 1
            SynchronousMethods.insert_one(
                collection=DatabaseCollections.USERS,
                data=user.model_dump()
            )
            raise ValueError("Invalid password")

        # Update last login and login attempts

        auth_object = AuthTokenSchema(
            user=UserGenericInfoSchema(**user.model_dump()),
            access=tokens.get("access"),
            refresh=tokens.get("refresh")
        )

        return auth_object

    @classmethod
    def logout_user(cls, access: str, refresh:str) -> TokenBlacklistSchema:
        """
        Log out the user by blacklisting the token.
        """
        if not access or not refresh:
            raise ValueError("Access or refresh token is required")

        if not isinstance(access, str) or not isinstance(refresh, str):
            raise ValueError("Access and refresh tokens must be strings")
        
        if SynchronousMethods.exists(
            filter_dict={"token": access},
            collection=DatabaseCollections.TOKEN_BLACKLIST
        ):
            raise ValueError("Token is already blacklisted")        
        
        if SynchronousMethods.exists(
            filter_dict={"token": refresh},
            collection=DatabaseCollections.TOKEN_BLACKLIST
        ):
            raise ValueError("Token is already blacklisted")
        
        access_blacklisted = blacklist_token(access)
        refresh_blacklisted = blacklist_token(refresh)


        if not access_blacklisted or not refresh_blacklisted:
            raise ValueError("Failed to blacklist token")
        
        return TokenBlacklistSchema(
            token=access_blacklisted.token,
            created_at=access_blacklisted.created_at,
            expires_at=access_blacklisted.expires_at
        )
        

    @classmethod
    def get_user_from_request(cls, request: Request) -> UserGenericInfoSchema:
        """
        Get the user from the request using the access token.
        """
        token = get_token_from_header(request)
        if not token:
            raise ValueError("Token is required")

        user = get_user_from_access_token(token)
        if not user:
            raise ValueError("Invalid token")

        return user