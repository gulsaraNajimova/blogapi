from typing import Any, Dict, Optional

from fastapi import HTTPException, status


class AuthError(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None):
        super().__init__(status.HTTP_403_FORBIDDEN, detail, headers)


class DuplicatedError(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)


class NotFoundError(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None):
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)

