import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from environs import Env

import services


def fetch_spacex_images(root_img_dir):
    spacex_url = "https://api.spacexdata.com/v4/launches"
    spacex_response = requests.get(spacex_url)
    all_spacex_launches = spacex_response.json()
    sorted_spacex_launches = reversed(all_spacex_launches)
    directory = f"{root_img_dir}/{services.fetch_file_name_prefix(spacex_url)}"
    Path(directory).mkdir(parents=True, exist_ok=True)

    for launch in sorted_spacex_launches:
        if launch["links"]["flickr"]["original"]:
            for image_number, image_url in enumerate(launch["links"]["flickr"]["original"]):
                extension = services.fetch_extension(image_url)
                filename = f"{directory}/spacex{image_number}{extension}"         
                services.save_images(image_url, filename)
            break
