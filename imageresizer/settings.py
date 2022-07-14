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

    log_folder: str = "."
    cache_dir: str = None
    cache_validity_s = 86400

    def _create_log_folder(self):
        Path(self.log_folder).mkdir(parents=True, exist_ok=True)

    def get_log_absolute_path(self, filename) -> str:
        """
        :return: the path to the log file with the given name
        """
        self._create_log_folder()
        return str(Path(self.log_folder) / filename)

    @property
    def cache_image_dir(self) -> str:
        """
        :return: the path where image files will be stored
        """
        return str(Path(self.cache_dir) / "images") if self.cache_dir else None


settings = Settings()
if settings.cache_image_dir:
    Path(settings.cache_image_dir).mkdir(parents=True, exist_ok=True)
