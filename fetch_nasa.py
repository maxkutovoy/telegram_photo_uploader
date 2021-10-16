import requests
from environs import Env

import services


def fetch_nasa_images(nasa_token, root_img_dir, number_of_images=15):
    env = Env()
    env.read_env()
    nasa_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": nasa_token,
        "thumbs": "True",
        "count": number_of_images,
        }
    nasa_response = requests.get(nasa_url, params=params)
    nasa_images = nasa_response.json()

    for image_number, image in enumerate(nasa_images):
        try:
            image_url = image["hdurl"]
            extension = services.fetch_extension(image_url)
            filename = f"nasa{image_number}{extension}"           
            services.save_images(root_img_dir, nasa_url, image_url, filename)
        except:
            print("В NASA изображение не найдено")


def fetch_nasa_earth_images(nasa_token, root_img_dir):
    nasa_url = "https://api.nasa.gov/EPIC/api/natural/images"
    payload = {
        "api_key": nasa_token,
        }
    nasa_response = requests.get(nasa_url, params=payload)
    nasa_earth_images = nasa_response.json()

    for image_number, image in enumerate(nasa_earth_images):
        try:
            image_name = image["image"]
            date = image["date"].split()[0].replace("-", "/")
            image_url = f"https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image_name}.png"
            extension = services.fetch_extension(image_url)
            filename = f"nasa_earth{image_number}{extension}"           
            services.save_images(root_img_dir, nasa_url, image_url, filename, params=payload)
        except:
            print("В NASA_Eerth Изображение не найдено")


def fetch_nasa(nasa_token, root_img_dir):
    fetch_nasa_earth_images(nasa_token, root_img_dir)
    fetch_nasa_images(nasa_token, root_img_dir)
