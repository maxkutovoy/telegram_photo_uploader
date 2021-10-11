import requests

import os
from pprint import pprint


def save_images(url, filename):
    response = requests.get(url)
    response.raise_for_status()

    directory = "images"
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"{directory}/{filename}"

    with open (filename, "wb") as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    spacex_url = "https://api.spacexdata.com/v4/launches"
    spacex_response = requests.get(spacex_url)
    all_spacex_launches = spacex_response.json()
    sorted_spacex_launches = list(reversed(all_spacex_launches))

    for flight in sorted_spacex_launches:
        if flight["links"]["flickr"]["original"]:
            for image_numder, image_url in enumerate(flight["links"]["flickr"]["original"]):
                filename = f"spacex{image_numder}.jpg"
                save_images(image_url, filename)
            break


if __name__ == "__main__":
    filename = "hubble.jpeg"
    url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"

    fetch_spacex_last_launch()

    # fetch_images(url, filename)
