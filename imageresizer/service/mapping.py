"""
Image resizing service types
"""

from imageresizer.repository import crud
from imageresizer.service.types import ScaleType, ResizedImageLookup

Size = tuple[int, int]


def _map_scale_type(service_scale_type: ScaleType) -> crud.ScaleType:
    """
    Convert a service ScaleType to a repository ScaleType
    """
    if service_scale_type == ScaleType.FIT_XY:
        return crud.ScaleType.FIT_XY
    return crud.ScaleType.FIT_PRESERVE_ASPECT_RATIO


def map_lookup(service_lookup: ResizedImageLookup) -> crud.ResizedImageLookup:
    """
    Convert a service lookup to a repository lookup
    """
    return crud.ResizedImageLookup(
        url=service_lookup.url,
        width=service_lookup.width,
        height=service_lookup.height,
        image_format=service_lookup.image_format.name
        if service_lookup.image_format
        else None,
        scale_type=_map_scale_type(service_lookup.scale_type),
    )
