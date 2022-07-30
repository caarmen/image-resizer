"""
Settings module
"""
from pathlib import Path
from typing import Set

from pydantic import BaseSettings


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """
    Settings for the app
    """

    log_dir: str = "."
    cache_dir: str = "."
    cache_validity_s = 86400
    cache_clean_interval_s = 86400
    supported_image_url_schemas: Set[str] = {"https"}
    allowed_domains: Set[str] = set()
    denied_domains: Set[str] = set()
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    docs_url: str = "/docs"

    def _create_log_dir(self):
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)

    def get_log_absolute_path(self, filename) -> str:
        """
        :return: the path to the log file with the given name
        """
        self._create_log_dir()
        return str(Path(self.log_dir) / filename)

    @property
    def cache_image_dir(self) -> str:
        """
        :return: the path where image files will be stored
        """
        return str(Path(self.cache_dir) / "images")


settings = Settings()
if settings.cache_image_dir:
    Path(settings.cache_image_dir).mkdir(parents=True, exist_ok=True)
