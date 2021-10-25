import time

import telegram
from environs import Env

import images_operations
from fetch_nasa import fetch_nasa
from fetch_spacex import fetch_spacex_images


def main():
    env = Env()
    env.read_env()
    root_img_dir = env.str("ROOT_IMG_DIR", "images")
    nasa_token = env.str("NASA_TOKEN")
    telegram_token = env.str("TELEGRAM_TOKEN")
    telegram_channel_id = env.str("CHANNEL_ID")
    bot = telegram.Bot(token=telegram_token)

    while True:
        fetch_nasa(nasa_token, root_img_dir)
        fetch_spacex_images(root_img_dir)
        random_image_path = images_operations.choose_random_image(root_img_dir)
        with open(random_image_path, 'rb') as file:
            bot.send_photo(chat_id=telegram_channel_id, photo=file)
        images_operations.remove_image_dirs(root_img_dir)

        time.sleep(env.int("TIME_INTERVAL", 86400))


if __name__ == "__main__":
    main()
