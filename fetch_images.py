import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from tldextract import extract


def fetch_file_name_prefix(url):
    extracted_url = extract(url)
    return extracted_url.domain


def fetch_extension(url):
    __, extension = os.path.splitext(url)
    return extension


def save_images(servise_url, image_url, filename, params=None):
    response = requests.get(image_url, params=params)
    response.raise_for_status()

    root_img_dir = os.getenv("ROOT_IMG_DIR")

    directory = f"{root_img_dir}/{fetch_file_name_prefix(servise_url)}"
    Path(directory).mkdir(parents=True, exist_ok=True)
    file_path = f"{directory}/{filename}"
    with open (file_path, "wb") as file:
        file.write(response.content)


def fetch_spacex_last_launch_images():
    spacex_url = "https://api.spacexdata.com/v4/launches"
    spacex_response = requests.get(spacex_url)
    all_spacex_launches = spacex_response.json()
    sorted_spacex_launches = reversed(all_spacex_launches)

    for flight in sorted_spacex_launches:
        if flight["links"]["flickr"]["original"]:
            for image_number, image_url in enumerate(flight["links"]["flickr"]["original"]):
                extension = fetch_extension(image_url)
                filename = f"spacex{image_number}{extension}"           
                save_images(spacex_url, image_url, filename)
            break


def fetch_nasa_images(nubder_of_images=10):
    nasa_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": os.getenv("NASA_TOKEN"),
        "thumbs": "True",
        "count": nubder_of_images,
        }
    nasa_response = requests.get(nasa_url, params=params)
    nasa_images = nasa_response.json()


    for image_number, image in enumerate(nasa_images):
        try:
            image_url = image["hdurl"]
            extension = fetch_extension(image_url)
            filename = f"nasa{image_number}{extension}"           
            save_images(nasa_url, image_url, filename)
        except:
            print("В NASA изображение не найдено")


def fetch_nasa_earth_images():
    nasa_url = "https://api.nasa.gov/EPIC/api/natural/images"
    payload = {
        "api_key": os.getenv("NASA_TOKEN"),
        }
    nasa_response = requests.get(nasa_url, params=payload)
    nasa_earth_images = nasa_response.json()

    for image_number, image in enumerate(nasa_earth_images):
        try:
            image_name = image["image"]
            date = image["date"].split()[0].replace("-", "/")
            image_url = f"https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image_name}.png"
            extension = fetch_extension(image_url)
            filename = f"nasa_earth{image_number}{extension}"           
            save_images(nasa_url, image_url, filename, params=payload)
        except:
            print("В NASA_Eerth Изображение не найдено")


def fetch_images():
    fetch_spacex_last_launch_images()
    fetch_nasa_images()
    fetch_nasa_earth_images()


if __name__ == "__main__":
    load_dotenv()
    fetch_images()
