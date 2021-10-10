import requests

import os

directory = "images"

if not os.path.exists(directory):
    os.makedirs(directory)

filename = f"{directory}/hubble.jpeg"
url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"

response = requests.get(url)
response.raise_for_status()

with open (filename, "wb") as file:
    file.write(response.content)