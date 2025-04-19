from datetime import datetime, timedelta
import pytz
import jwt

from fastapi.requests import Request

from database.collections import DatabaseCollections
from database.methods import SynchronousMethods
from models.auth import User
from schema.auth import UserGenericInfoSchema
from config.globals import settings

from utils import logger


ACCESS_KEY: str = "access"
REFRESH_KEY: str = "refresh"
JWT_HEADER_KEY: str = "Authorization"
JWT_HEADER_PREFIX: str = "Brearer"


def get_token_from_header(request: Request) -> str:
    """
    Get the token from the Authorization header.
    """
    auth_header = request.headers.get(JWT_HEADER_KEY)
    if not auth_header:
        raise ValueError("Authorization header is missing")
    if not isinstance(auth_header, str):
        raise ValueError("Authorization header must be a string")
    token_parts = auth_header.split(" ")
    return token_parts[-1]


def create_access_token(user: User) -> str:
    data = {
        "sub": user.email,
        "id": user.id,
        "type": ACCESS_KEY,
        "exp": datetime.now(tz=pytz.UTC) + timedelta(seconds=settings.JWT_EXPIRATION_TIME)
    }
    logger.info(
        f"Creating access token for user: {user.email} with expiration time: {settings.JWT_EXPIRATION_TIME} seconds")
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user: User) -> str:
    data = {
        "sub": user.email,
        "id": user.id,
        "type": REFRESH_KEY,
        "exp": datetime.now(tz=pytz.UTC) + timedelta(seconds=settings.JWT_REFRESH_EXPIRATION_TIME)
    }
    logger.info(
        f"Creating refresh token for user: {user.email} with expiration time: {settings.JWT_REFRESH_EXPIRATION_TIME} seconds")
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    if not token:
        raise ValueError("Token is required")
    if not isinstance(token, str):
        raise ValueError("Token must be a string")
    token_parts = token.split(" ")
    if len(token_parts) != 2 or token_parts[0] != JWT_HEADER_PREFIX:
        raise ValueError("Invalid token format")
    token = token_parts[-1]
    if SynchronousMethods.exists(
        filter_dict={"token": token},
        collection=DatabaseCollections.TOKEN_BLACKLIST
    ):
        raise ValueError("Token is blacklisted")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def validate_access_token(token: str) -> bool:
    if not token:
        raise ValueError("Token is required")

    try:
        payload = decode_token(token)
        if payload["type"] != ACCESS_KEY:
            raise ValueError("Invalid token type")
        return payload
    except ValueError:
        return None


def validate_refresh_token(token: str) -> bool:
    try:
        payload = decode_token(token)
        if payload["type"] != REFRESH_KEY:
            raise ValueError("Invalid token type")
        return payload
    except ValueError:
        return None


def get_user_from_payload(payload: dict) -> UserGenericInfoSchema:
    _id = payload.get("id")
    if not _id:
        raise ValueError("Invalid payload: missing user ID")

    user = SynchronousMethods.get_user_by_id(_id)
    if not user:
        raise ValueError("User not found")
    return UserGenericInfoSchema(**user)


def get_user_from_access_token(token: str) -> UserGenericInfoSchema:
    payload = validate_access_token(token)
    if not payload:
        raise ValueError("Invalid token")

    return get_user_from_payload(payload)


def get_user_from_refresh_token(token: str) -> UserGenericInfoSchema:
    payload = validate_refresh_token(token)
    if not payload:
        raise ValueError("Invalid token")

    return get_user_from_payload(payload)


def blacklist_token(token: str):
    """
    Blacklist a token by adding it to the blacklist collection.
    """
    if not token:
        raise ValueError("Token is required")
    if not isinstance(token, str):
        raise ValueError("Token must be a string")
    if SynchronousMethods.exists(
        filter_dict={"token": token},
        collection=DatabaseCollections.TOKEN_BLACKLIST
    ):
        raise ValueError("Token is already blacklisted")

    res = SynchronousMethods.insert_one(
        data={
            "token": token,
            "created_at": datetime.now(tz=pytz.UTC),
            "expires_at": datetime.now(tz=pytz.UTC) + timedelta(seconds=settings.JWT_EXPIRATION_TIME)
        },
        collection=DatabaseCollections.TOKEN_BLACKLIST
    )

    return res
