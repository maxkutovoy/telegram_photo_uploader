import os
import random
import shutil
import time

import telegram
from environs import Env

from fetch_nasa import fetch_nasa
from fetch_spacex import fetch_spacex_images


def main():
    while True:
        env = Env()
        env.read_env()

        bot = telegram.Bot(token=env.str("TELEGRAM_TOKEN"))
        space_photos_channel_id = env.str("CHANNEL_ID")

        fetch_nasa()
        fetch_spacex_images()
        root_img_dir = env.str("ROOT_IMG_DIR", "images")
        random_image_dir = random.choice(os.listdir(root_img_dir))
        random_image = random.choice((os.listdir(f"{root_img_dir}/{random_image_dir}")))
        random_image_path = f"{root_img_dir}/{random_image_dir}/{random_image}"

        bot.send_photo(chat_id=space_photos_channel_id, photo=open(random_image_path, 'rb'))

        dirs_for_remove = os.listdir(root_img_dir)
        for dir in dirs_for_remove:
            shutil.rmtree(f"{root_img_dir}/{dir}")

        time.sleep(env.int("TIME_INTERVAL", 86400))


if __name__ == "__main__":
    main()
