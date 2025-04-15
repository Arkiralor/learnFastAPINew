from fastapi import status
from fastapi.exceptions import HTTPException, WebSocketException


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "not_found",
        }


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "bad_request",
        }


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "unauthorized",
        }


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Forbidden"):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "forbidden",
        }


class InternalServerErrorException(HTTPException):
    def __init__(self, detail: str = "Internal server error"):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "internal_server_error",
        }


class ConflictException(HTTPException):
    def __init__(self, detail: str = "Conflict"):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "conflict",
        }


class NotAcceptableException(HTTPException):
    def __init__(self, detail: str = "Not acceptable"):
        self.status_code = status.HTTP_406_NOT_ACCEPTABLE
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "not_acceptable",
        }
    
class NotFoundWSException(WebSocketException):
    def __init__(self, detail: str = "Resource not found"):
        self.status_code = status.WS_1003_UNSUPPORTED_DATA
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "not_found",
        }
    
class BadRequestWSException(WebSocketException):
    def __init__(self, detail: str = "Bad request"):
        self.status_code = status.WS_1003_UNSUPPORTED_DATA
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "bad_request",
        }
    
class UnauthorizedWSException(WebSocketException):
    def __init__(self, detail: str = "Unauthorized"):
        self.status_code = status.WS_1010_MANDATORY_EXT
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "unauthorized",
        }
    
class ForbiddenWSException(WebSocketException):
    def __init__(self, detail: str = "Forbidden"):
        self.status_code = status.WS_1008_POLICY_VIOLATION
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "forbidden",
        }
    
class InternalServerErrorWSException(WebSocketException):
    def __init__(self, detail: str = "Internal server error"):
        self.status_code = status.WS_1011_UNEXPECTED_CONDITION
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "internal_server_error",
        }
    
class ConflictWSException(WebSocketException):
    def __init__(self, detail: str = "Conflict"):
        self.status_code = status.WS_1008_POLICY_VIOLATION
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "conflict",
        }
    
class NotAcceptableWSException(WebSocketException):
    def __init__(self, detail: str = "Not acceptable"):
        self.status_code = status.WS_1003_UNSUPPORTED_DATA
        self.detail = detail

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": "not_acceptable",
        }
