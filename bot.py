import os
import random
import shutil
import time

import telegram
from dotenv import load_dotenv

import fetch_images as fi

load_dotenv()

def main():
    while True:
        bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
        space_photos_channel_id = os.getenv("CHANNEL_ID")

        # fi.fetch_images()
        root_img_dir = os.getenv("ROOT_IMG_DIR")
        random_image_dir = random.choice(os.listdir(root_img_dir))
        random_image = random.choice((os.listdir(f"{root_img_dir}/{random_image_dir}")))
        random_image_path = f"{root_img_dir}/{random_image_dir}/{random_image}"

        bot.send_photo(chat_id=space_photos_channel_id, photo=open(random_image_path, 'rb'))

        dirs_for_remove = os.listdir(root_img_dir)
        print(dirs_for_remove)
        for dir in dirs_for_remove:
            shutil.rmtree(f"{root_img_dir}/{dir}")

        time.sleep(10)


if __name__ == "__main__":
    main()
