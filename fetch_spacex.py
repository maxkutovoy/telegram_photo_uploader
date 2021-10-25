from pathlib import Path

import requests

import filename_operations as fl
import images_operations as im


def fetch_spacex_images(root_img_dir):
    spacex_url = "https://api.spacexdata.com/v4/launches"
    spacex_response = requests.get(spacex_url)
    spacex_response.raise_for_status()
    all_spacex_launches = spacex_response.json()
    sorted_spacex_launches = reversed(all_spacex_launches)
    directory = f"{root_img_dir}/{fl.define_filename_prefix(spacex_url)}"
    Path(directory).mkdir(parents=True, exist_ok=True)

    for launch in sorted_spacex_launches:
        if launch["links"]["flickr"]["original"]:
            for image_url in launch["links"]["flickr"]["original"]:
                filename = fl.pars_filename(image_url)
                file_path = f"{directory}/{filename}"
                im.save_image(image_url, file_path)
            break
