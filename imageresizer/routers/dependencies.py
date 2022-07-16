"""
Provides dependencies for routers
"""
from http import HTTPStatus

from fastapi import HTTPException
from starlette.requests import Request

from imageresizer.repository.database import SessionLocal

CLIENT_HEADER = "x-image-resizer"


def get_session():
    """
    Provides a database session
    """
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


async def client_headers():
    """
    Provides headers we should use when we are doing a request to another server
    """
    return {
        CLIENT_HEADER: "true",
    }


async def validate_not_recursive(request: Request):
    """
    Validate that a request we received didn't come from our own server
    """
    if request.headers.get(CLIENT_HEADER):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid image url"
        )
