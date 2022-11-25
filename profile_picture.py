from typing import List
import wget
import pandas as pd
from settings import PROFILE_PICTURE_OUTPUT_DIR, INPUT_DIR
from user import UserInputColumns

BASE_URL = "https://eleves.mines-paris.eu/static//img/trombi"
IMAGE_EXTENSION = ".jpg"

user_df = pd.read_csv(INPUT_DIR + "/user.csv")

usernames: List[str] = user_df.loc[:, UserInputColumns.USERNAME.value].to_list()


def download_profile_picture(username: str):
    image_filename = username + IMAGE_EXTENSION

    print(f"Downloading... {image_filename}")

    try:
        wget.download(
            BASE_URL + "/" + image_filename,
            out=PROFILE_PICTURE_OUTPUT_DIR + "/" + image_filename,
        )

        print(" Downloaded!")
    except Exception as e:
        print(" Failure")


if __name__ == "__main__":
    for username in usernames:
        download_profile_picture(username)
