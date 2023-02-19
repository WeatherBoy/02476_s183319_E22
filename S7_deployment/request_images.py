# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Gotta be totally honest, don't entirely know what the logic for doing this in another script was..
# I just thought it was adequately different that another script for a better overview, might be nice.
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Created by Felix Bo Caspersen, s183319 on Tue Jan 17 2023

import os

import requests

response_im = requests.get("https://imgs.xkcd.com/comics/making_progress.png")

# Trying to call .json() on this png fails :/
try:
    print(response_im.json())
except requests.JSONDecodeError:
    print("We can't convert this image into a json-file...")


def saveRequestAsIm(
    response_im: requests.Response, filename: str, path_to_dir: str = "./S7_deployment/saved_ims"
) -> None:
    """
    Super dumb function!
    More os shenaniganz
    """
    if not os.path.isdir(path_to_dir):
        os.makedirs(path_to_dir)
    if response_im.status_code == 200:
        # Valid response status_code, so we can save the contents as a json

        while os.path.exists(path_to_dir + "/" + filename + ".png"):
            # Checking whether the filename exists and creates a new filename
            # in the case it does.

            if filename[-2:].isnumeric():
                temp_num = int(filename[-2:])
                temp_num += 1
                if temp_num < 10:
                    filename = filename[:-2] + "0" + str(temp_num)
                else:
                    filename = filename[:-2] + str(temp_num)
            else:
                filename = filename + "01"

        with open(path_to_dir + "/" + filename + ".png", "wb") as f:
            f.write(response_im.content)

        print("File was succesfully saved to the path: ", path_to_dir + "/" + filename + ".png", sep="\n")

    else:
        print(
            f"Encountered status code: {response_im.status_code}. You might want to check it at: https://restfulapi.net/http-status-codes/"
        )


saveRequestAsIm(response_im, "request_im")
