from pathlib import Path
from urllib.parse import urlparse

import requests
from environs import Env

import services


def fetch_spacex_images(root_img_dir):
    spacex_url = "https://api.spacexdata.com/v4/launches"
    spacex_response = requests.get(spacex_url)
    spacex_response.raise_for_status()
    all_spacex_launches = spacex_response.json()
    sorted_spacex_launches = reversed(all_spacex_launches)
    directory = f"{root_img_dir}/{services.fetch_file_name_prefix(spacex_url)}"
    Path(directory).mkdir(parents=True, exist_ok=True)

    for launch in sorted_spacex_launches:
        if launch["links"]["flickr"]["original"]:
            for image_number, image_url in enumerate(launch["links"]["flickr"]["original"]):
                filename = services.fetch_filename(image_url)
                file_path = f"{directory}/{filename}"
                print(file_path)  
                services.save_images(image_url, file_path)
            break
