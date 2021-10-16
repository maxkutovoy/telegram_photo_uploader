import os
import time

import telegram
from environs import Env

import services
from fetch_nasa import fetch_nasa
from fetch_spacex import fetch_spacex_images


def main():
    env = Env()
    env.read_env()
    root_img_dir = env.str("ROOT_IMG_DIR", "images")
    nasa_toket = env.str("NASA_TOKEN")
    telegram_token = env.str("TELEGRAM_TOKEN")
    telegram_channel_id = env.str("CHANNEL_ID")
    bot = telegram.Bot(token=telegram_token)

    while True:
        fetch_nasa(nasa_toket, root_img_dir)
        fetch_spacex_images(root_img_dir)
        random_image_path = services.fetch_random_image(root_img_dir)
        with open(random_image_path, 'rb') as file:
            bot.send_photo(chat_id=telegram_channel_id, photo=file)
        services.remove_used_images(root_img_dir)

        time.sleep(env.int("TIME_INTERVAL", 86400))


if __name__ == "__main__":
    main()
