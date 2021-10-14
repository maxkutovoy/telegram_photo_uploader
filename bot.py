import os
import random
import time

import telegram
from dotenv import load_dotenv

import fetch_images as fi

load_dotenv()

def main():
    while True:
        bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
        space_photos_channel_id = os.getenv("CHANNEL_ID")

        fi.fetch_images()
        root_img_dir = os.getenv("ROOT_IMG_DIR")
        random_image_dir = random.choice(os.listdir(root_img_dir))
        random_image = random.choice((os.listdir(f"{root_img_dir}/{random_image_dir}")))
        random_image_path = f"{root_img_dir}/{random_image_dir}/{random_image}"

        bot.send_photo(chat_id=space_photos_channel_id, photo=open(random_image_path, 'rb'))

        time.sleep(10)


if __name__ == "__main__":
    main()
