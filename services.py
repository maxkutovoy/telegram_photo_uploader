import os
import random
import shutil
from urllib.parse import unquote, urlsplit

import requests
from tldextract import extract


def fetch_file_name_prefix(url):
    extracted_url = extract(url)
    return extracted_url.domain


def fetch_filename(url):
    parsed_url = urlsplit(url)
    filename = os.path.split(unquote(parsed_url.path))[1]
    return filename


def fetch_random_image(root_img_dir):
        random_image_dir = random.choice(os.listdir(root_img_dir))
        random_image = random.choice((os.listdir(f"{root_img_dir}/{random_image_dir}")))
        random_image_path = f"{root_img_dir}/{random_image_dir}/{random_image}"
        return random_image_path


def remove_used_images(root_img_dir):
        dirs_for_remove = os.listdir(root_img_dir)
        for dir in dirs_for_remove:
            shutil.rmtree(f"{root_img_dir}/{dir}")


def save_images(image_url, file_path, params=None):
    response = requests.get(image_url, params=params)
    response.raise_for_status()
    with open (file_path, "wb") as file:
        file.write(response.content)
