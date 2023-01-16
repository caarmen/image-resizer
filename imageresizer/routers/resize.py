"""
Resize router
"""
from http import HTTPStatus
from urllib.error import HTTPError, URLError

from fastapi import APIRouter, HTTPException
from fastapi.params import Query, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from imageresizer.routers.dependencies import (
    get_session,
    validate_not_recursive,
    client_headers,
    validate_allowed_domain,
    validate_supported_schema,
)
from imageresizer.service import service
from imageresizer.service.types import ImageFormat, ScaleType, ResizedImageLookup

router = APIRouter(
    dependencies=[
        Depends(validate_not_recursive),
        Depends(validate_supported_schema),
        Depends(validate_allowed_domain),
    ],
)


# pylint: disable=too-many-arguments
@router.get(
    "/resize",
    responses={
        200: {
            "content": {
                "image/png": {},
                "image/gif": {},
                "image/jpeg": {},
                "image/tiff": {},
                "image/webp": {},
                "application/pdf": {},
            },
        },
        400: {
            "description": "Invalid request parameters",
        },
        422: {
            "description": "The request parameters were understood, but could not be processed",
        },
    },
)
async def resize(
    image_url: str,
    width: int | None = Query(default=None, gt=0, lt=1024),
    height: int | None = Query(default=None, gt=0, lt=1024),
    image_format: ImageFormat | None = Query(default=None),
    scale_type: ScaleType | None = Query(default=ScaleType.FIT_XY),
    user_agent: str | None = "image-resizer",
    db_session: Session = Depends(get_session),
    headers: dict = Depends(client_headers),
):
    """
    Endpoint to resize an image.

    :param image_url: the url of the image to resize

    :param width: the width of the new image

    :param height: the height of the new image

    :param image_format: the format of the resized image. Defaults to the format of the source image

    :param scale_type: controls how the image should be resized to match
    the requested width and height. Ignored if either width or height are not provided.

    :param user_agent: the User-Agent header value to pass to the request to get the image

    :return: a Response containing the new image
    """
    try:
        resized_image = service.resize(
            db_session,
            headers={**headers, "User-Agent": user_agent},
            lookup=ResizedImageLookup(
                url=image_url,
                width=width,
                height=height,
                image_format=image_format,
                scale_type=scale_type,
            ),
        )
        return FileResponse(resized_image.file, media_type=resized_image.mime_type)
    except HTTPError as error:
        raise HTTPException(
            status_code=error.status, detail="Error retrieving image"
        ) from error
    except URLError as error:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid image url"
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Didn't understand your request parameters",
        ) from error
