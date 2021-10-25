from pathlib import Path

import requests

import filename_operations
import images_operations


def fetch_nasa_images(nasa_token, root_img_dir, number_of_images=15):
    nasa_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": nasa_token,
        "thumbs": "True",
        "count": number_of_images,
    }
    nasa_response = requests.get(nasa_url, params=params)
    nasa_response.raise_for_status()
    nasa_images = nasa_response.json()

    directory = f"{root_img_dir}/{filename_operations.define_filename_prefix(nasa_url)}"
    Path(directory).mkdir(parents=True, exist_ok=True)

    for image in nasa_images:
        if image["hdurl"]:
            image_url = image["hdurl"]
            filename = filename_operations.pars_filename(image_url)
            file_path = f"{directory}/{filename}"
            images_operations.save_image(image_url, file_path)


def fetch_nasa_earth_images(nasa_token, root_img_dir):
    nasa_epic_url = "https://api.nasa.gov/EPIC/api/natural/images"
    payload = {
        "api_key": nasa_token,
    }
    nasa_response = requests.get(nasa_epic_url, params=payload)
    nasa_response.raise_for_status()
    nasa_epic_images = nasa_response.json()

    directory = f"{root_img_dir}/{filename_operations.define_filename_prefix(nasa_epic_url)}"
    Path(directory).mkdir(parents=True, exist_ok=True)

    for image in nasa_epic_images:
        if image["image"]:
            image_name = image["image"]
            date = image["date"].split()[0].replace("-", "/")
            image_url = (
                "https://api.nasa.gov/EPIC/archive/natural/"
                f"{date}/png/{image_name}.png"
            )
            filename = filename_operations.pars_filename(image_url)
            file_path = f"{directory}/{filename}"
            images_operations.save_image(image_url, file_path, params=payload)


def fetch_nasa(nasa_token, root_img_dir):
    fetch_nasa_earth_images(nasa_token, root_img_dir)
    fetch_nasa_images(nasa_token, root_img_dir)
