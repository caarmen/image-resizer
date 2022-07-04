"""
Animated image support
"""

from PIL import Image
from PIL.GifImagePlugin import GifImageFile

Size = tuple[int, int]


class AnimatedImage:
    """
    An image-like class with resize and save functions, for images containing image sequences
    """

    def __init__(self, source: GifImageFile):
        self._source = source
        self._frames = []

    def resize(self, size: Size):
        """
        Resize the frames of this image
        :param size: The requested size in pixels
        :return: this instance
        """
        for i in range(self._source.n_frames):
            self._source.seek(i)
            self._frames.append(
                self._source.resize(size, resample=Image.Resampling.BICUBIC)
            )
        return self

    def save(self, output_path: str, image_format: str):
        """
        Saves this image under the given filename and format.
        """
        self._frames[0].save(
            output_path,
            append_images=self._frames[1:],
            format=image_format,
            save_all=True,
        )
