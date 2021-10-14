import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from environs import Env

import services


def fetch_spacex_images():
    spacex_url = "https://api.spacexdata.com/v4/launches"
    spacex_response = requests.get(spacex_url)
    all_spacex_launches = spacex_response.json()
    sorted_spacex_launches = reversed(all_spacex_launches)

    for flight in sorted_spacex_launches:
        if flight["links"]["flickr"]["original"]:
            for image_number, image_url in enumerate(flight["links"]["flickr"]["original"]):
                extension = services.fetch_extension(image_url)
                filename = f"spacex{image_number}{extension}"           
                services.save_images(spacex_url, image_url, filename)
            break
