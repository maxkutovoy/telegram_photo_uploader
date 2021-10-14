import os
import random
import shutil
import time

import telegram
from environs import Env

import fetch_images as fi


def main():
    while True:
        env = Env()
        env.read_env()

        bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
        space_photos_channel_id = os.getenv("CHANNEL_ID")

        fi.fetch_images()
        root_img_dir = env.str("ROOT_IMG_DIR")
        random_image_dir = random.choice(os.listdir(root_img_dir))
        random_image = random.choice((os.listdir(f"{root_img_dir}/{random_image_dir}")))
        random_image_path = f"{root_img_dir}/{random_image_dir}/{random_image}"

        bot.send_photo(chat_id=space_photos_channel_id, photo=open(random_image_path, 'rb'))

        dirs_for_remove = os.listdir(root_img_dir)
        for dir in dirs_for_remove:
            shutil.rmtree(f"{root_img_dir}/{dir}")

        time.sleep(int(env.int("TIME_INTERVAL")))


if __name__ == "__main__":
    main()
