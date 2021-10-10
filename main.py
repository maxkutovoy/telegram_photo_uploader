import requests

import os


def fetch_images(url, filename):
    response = requests.get(url)
    response.raise_for_status()

    directory = "images"
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"{directory}/{filename}"

    with open (filename, "wb") as file:
        file.write(response.content)


if __name__ == "__main__":
    filename = "hubble.jpeg"
    url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"

    fetch_images(url, filename)
