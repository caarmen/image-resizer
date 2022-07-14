"""
Api tests
"""
import io
import os
from pathlib import Path

import pytest
from PIL import Image
from fastapi.testclient import TestClient
from requests import Response

from imageresizer.main import app, setup
from imageresizer.service.types import Size


def _get_test_image_uri(test_image_filename: str) -> str:
    test_image_path = (
        Path(os.path.abspath(__file__)).parent / "data" / test_image_filename
    )
    return test_image_path.absolute().as_uri()


test_image_png_uri = _get_test_image_uri("150x100.png")
test_image_gif_uri = _get_test_image_uri("animated.gif")
setup()
client = TestClient(app)


def test_missing_image_url():
    """
    When I don't specify an image url, I get a 422 error code.
    """
    response = client.get("/resize")
    assert response.status_code == 422


@pytest.mark.parametrize("test_image_uri", [test_image_png_uri, test_image_gif_uri])
def test_zero_width(test_image_uri):
    """
    When I don't specify a zero width, I get a 422 error code
    """
    response = client.get(f"/resize?image_url={test_image_uri}&width=0")
    assert response.status_code == 422


@pytest.mark.parametrize("test_image_uri", [test_image_png_uri, test_image_gif_uri])
def test_negative_width(test_image_uri):
    """
    When I don't specify a negative width, I get a 422 error code
    """
    response = client.get(f"/resize?image_url={test_image_uri}&width=-1")
    assert response.status_code == 422


@pytest.mark.parametrize("test_image_uri", [test_image_png_uri, test_image_gif_uri])
def test_zero_height(test_image_uri):
    """
    When I don't specify a zero height, I get a 422 error code
    """
    response = client.get(f"/resize?image_url={test_image_uri}&height=0")
    assert response.status_code == 422


@pytest.mark.parametrize("test_image_uri", [test_image_png_uri, test_image_gif_uri])
def test_negative_height(test_image_uri):
    """
    When I don't specify a negative height, I get a 422 error code
    """
    response = client.get(f"/resize?image_url={test_image_uri}&height=-1")
    assert response.status_code == 422


def _assert_expected_size(response: Response, expected_size: Size):
    assert response.status_code == 200
    with Image.open(io.BytesIO(response.content)) as image:
        assert image.width == expected_size[0]
        assert image.height == expected_size[1]


@pytest.mark.parametrize("test_image_uri", [test_image_png_uri, test_image_gif_uri])
def test_no_resize(test_image_uri):
    """
    When I don't provide a width or height, I get the original image size
    """
    response = client.get(f"/resize?image_url={test_image_uri}")
    _assert_expected_size(response, expected_size=(150, 100))


@pytest.mark.parametrize("test_image_uri", [test_image_png_uri, test_image_gif_uri])
def test_resize_width_and_height(test_image_uri):
    """
    When I provide both width and height, I get an image with that provided size
    """
    response = client.get(f"/resize?image_url={test_image_uri}&width=75&height=25")
    _assert_expected_size(response, expected_size=(75, 25))


@pytest.mark.parametrize("test_image_uri", [test_image_png_uri, test_image_gif_uri])
def test_resize_provided_width(test_image_uri):
    """
    When I provide only width, I get an image with the height calculated
    based on the original aspect ratio
    """
    response = client.get(f"/resize?image_url={test_image_uri}&width=75")
    _assert_expected_size(response, expected_size=(75, 50))


@pytest.mark.parametrize("test_image_uri", [test_image_png_uri, test_image_gif_uri])
def test_resize_provided_height(test_image_uri):
    """
    When I provide only height, I get an image with the width calculated
    based on the original aspect ratio
    """
    response = client.get(f"/resize?image_url={test_image_uri}&height=50")
    _assert_expected_size(response, expected_size=(75, 50))


def test_recursive_request_fails():
    """
    When the server receives a request with the x-image-resizer header, it returns an error response
    """
    response = client.get(
        f"/resize?image_url={test_image_png_uri}", headers={"x-image-resizer": "foo"}
    )
    assert response.status_code == 400
