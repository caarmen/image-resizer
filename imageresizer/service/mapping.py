"""
Image resizing service types
"""

from imageresizer.repository import crud
from imageresizer.service.types import ResizedImageLookup

Size = tuple[int, int]


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
    )
