import cv2
import itertools
import json
import numpy as np

from django.db import models
from django.utils.text import slugify

from rest_framework import status
from rest_framework.response import Response
from urllib import request as urlreq
from urllib.parse import urlencode, quote_plus


def create_error_response(message):
    print("API ERROR: " + message)
    return Response({
        'status': status.HTTP_400_BAD_REQUEST,
        'message': message,
    }, status=status.HTTP_400_BAD_REQUEST)


def download_image(image_url):
    response = urlreq.urlopen(image_url)
    img_array = np.array(bytearray(response.read()), dtype=np.uint8)  # nopep8
    image = cv2.imdecode(img_array, -1)

    return image


def get_image_descriptions(image_url):
    image = download_image(image_url)

    # Force a resize in case it's larger than 1000
    image = resize_image(image, 1000)

    # Change the image color to GRAY
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create()
    (keypoints, descriptors) = orb.detectAndCompute(image, None)  # nopep8

    return descriptors


def jsonfield_default_value():
    return {}


def resize_image(image, max_width):
    (height, width, channel) = image.shape

    while (width > max_width):
        new_width = int(width/2)
        new_height = int(height/2)

        image = cv2.resize(image, (new_width, new_height))
        (height, width, channel) = image.shape

    return image


def scryfall_api(params):
    return scryfall_fetch(
        "https://api.scryfall.com/cards/search?" + urlencode(params)
    )


def scryfall_fetch(url):
    response = urlreq.urlopen(url)

    content = response.read()
    encoding = response.info().get_content_charset('utf-8')

    data = json.loads(content.decode(encoding))

    cards = data['data']

    if data['has_more']:
        cards = cards + scryfall_fetch(data['next_page'])

    return cards


def slugify_model(model: models.Model, content: str) -> str:
    """
    Slugify a content and assume it's an unique slug in a model
    Parameters
    ----------
    model : django.db.models.Model, mandatory
            The model to check for uniqueness
    content : str, mandatory
            The content to slugify
    Returns
    -------
    slug : str
        the new unique slug for this model
    """
    slug_candidate = slug_original = slugify(content)

    for i in itertools.count(1):
        if not model.objects.filter(slug=slug_candidate).exists():
            break
        slug_candidate = '{}-{}'.format(slug_original, i)

    return slug_candidate
