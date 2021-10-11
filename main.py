import requests

from tldextract import extract
import os
from urllib.parse import urlparse
from pprint import pprint


def fetch_file_name_prefix(url):
    extracted = extract(url)
    return extracted.domain


def save_images(servise_url, image_url, filename):
    response = requests.get(image_url)
    response.raise_for_status()

    directory = fetch_file_name_prefix(servise_url)

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"{directory}/{filename}"

    with open (filename, "wb") as file:
        file.write(response.content)


def fetch_spacex_last_launch_images():
    spacex_url = "https://api.spacexdata.com/v4/launches"
    spacex_response = requests.get(spacex_url)
    all_spacex_launches = spacex_response.json()
    sorted_spacex_launches = list(reversed(all_spacex_launches))

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
    nasa_request = nasa_response.json()

    for image_number, image in enumerate(nasa_request):
        try:
            image_url = image["hdurl"]
            extension = fetch_extension(image_url)
            filename = f"nasa{image_number}{extension}"           
            save_images(nasa_url, image_url, filename)
        except:
            print("Изображение не найдено")


def fetch_extension(url):
    __, extension = os.path.splitext(url)
    return extension

# https://api.nasa.gov/planetary/apod?api_key=C0PVRDummK18vJxbYfuAERTd6CccdT7toxBgYzal

if __name__ == "__main__":
    # filename = "hubble.jpeg"
    url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"

    # fetch_spacex_last_launch_images()
    fetch_nasa_images()
