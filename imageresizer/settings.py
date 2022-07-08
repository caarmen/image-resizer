"""
Settings module
"""
from pathlib import Path

from pydantic import BaseSettings


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """
    Settings for the app
    """

    worker_count: int = 1
    cache_dir: str = None

    @property
    def cache_image_dir(self) -> str:
        """
        :return: the path where image files will be stored
        """
        return str(Path(self.cache_dir) / "images") if self.cache_dir else None


settings = Settings()
if settings.cache_image_dir:
    Path(settings.cache_image_dir).mkdir(parents=True, exist_ok=True)
