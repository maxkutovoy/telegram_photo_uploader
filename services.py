import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from environs import Env
from tldextract import extract


def fetch_file_name_prefix(url):
    extracted_url = extract(url)
    return extracted_url.domain


def fetch_extension(url):
    __, extension = os.path.splitext(url)
    return extension


def save_images(root_img_dir, servise_url, image_url, filename, params=None):

    response = requests.get(image_url, params=params)
    response.raise_for_status()

    directory = f"{root_img_dir}/{fetch_file_name_prefix(servise_url)}"
    Path(directory).mkdir(parents=True, exist_ok=True)
    file_path = f"{directory}/{filename}"
    with open (file_path, "wb") as file:
        file.write(response.content)
