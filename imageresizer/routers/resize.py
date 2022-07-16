"""
Resize router
"""
from urllib.error import HTTPError
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.params import Query, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from imageresizer.routers.dependencies import (
    get_session,
    validate_not_recursive,
    client_headers,
)
from imageresizer.service import service
from imageresizer.service.types import ImageFormat, ScaleType, ResizedImageLookup

router = APIRouter(
    dependencies=[Depends(validate_not_recursive)],
)


# pylint: disable=too-many-arguments
@router.get(
    "/resize",
    responses={
        HTTPStatus.OK: {
            "content": {
                "image/png": {},
                "image/gif": {},
                "image/jpeg": {},
                "image/tiff": {},
                "image/webp": {},
                "application/pdf": {},
            },
        },
        HTTPStatus.BAD_REQUEST: {
            "description": "Invalid request parameters",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "image not found",
        },
    },
)
async def resize(
    image_url: str,
    width: int | None = Query(default=None, gt=0, lt=1024),
    height: int | None = Query(default=None, gt=0, lt=1024),
    image_format: ImageFormat | None = Query(default=None),
    scale_type: ScaleType | None = Query(default=ScaleType.FIT_XY),
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

    :return: a Response containing the new image
    """
    try:
        resized_image = service.resize(
            db_session,
            headers=headers,
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
        raise HTTPException(status_code=error.status, detail=error.reason) from error
