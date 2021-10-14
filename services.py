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


def save_images(servise_url, image_url, filename, params=None):
    env = Env()
    env.read_env()
    response = requests.get(image_url, params=params)
    response.raise_for_status()

    root_img_dir = env.str("ROOT_IMG_DIR")

    directory = f"{root_img_dir}/{fetch_file_name_prefix(servise_url)}"
    Path(directory).mkdir(parents=True, exist_ok=True)
    file_path = f"{directory}/{filename}"
    with open (file_path, "wb") as file:
        file.write(response.content)
