# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# A very smol script to test the requests library
# Oh no... I get error code 403!?
# Shouldn't it be 404???
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Created by Felix Bo Caspersen, s183319 on Tue Jan 17 2023

import requests
import os
import json


def checkValidResponse(response: requests.Response) -> None:
    """
    What is an overkill?

    The course wanted us to be aware that you could have conditions,
    based on the status codes of requests.

    This function exemplifies this functionality.
    """
    if response.status_code == 200:
        print(f"Response connected with valid status code: {response.status_code}")
        print(f"Response contents: \n{response.content}\n")
    elif response.status_code == 403:
        print(f"Restricted acces at the moment. Found status code: {response.status_code}")
    elif response.status_code == 404:
        print(f"A classic! Response status code: {response.status_code}")
    else:
        print(f"Responded with unkown status code: {response.status_code}")
        print("You could try and check: https://restfulapi.net/http-status-codes/")


response_1 = requests.get("https://api.github.com/this-api-should-not-exist")
checkValidResponse(response_1)

response_2 = requests.get("https://api.github.com")
checkValidResponse(response_2)

response_3 = requests.get("https://api.github.com/repos/SkafteNicki/dtu_mlops")
checkValidResponse(response_3)

# If Github didn't time me out I could call:
# repsonse_3.json()
# To convert the response to a "human-readable" json file, rather than the
# standard byte output.


#%% QUERY SEARCH **********************************************************************************
# Additionally we can add queries to our requests.
# Here, I think, we request all the URLs of all the repositories
# containing Python code.
response_4 = requests.get(
    "https://api.github.com/search/repositories",
    params={"q": "requests+language:python"},
)


def saveResponseAsJson(
    response: requests.Response, filename: str, path_to_dir: str = "./S7_deployment/request_jsons"
) -> None:
    """
    Super dumb function, but I just wanted to play a little bit with os and saving a file.
    """
    if not os.path.isdir(path_to_dir):
        os.makedirs(path_to_dir)
    if response.status_code == 200:
        # Valid response status_code, so we can save the contents as a json

        while os.path.exists(path_to_dir + "/" + filename + ".json"):
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

        with open(path_to_dir + "/" + filename + ".json", "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)

        print("File was succesfully saved to the path: ", path_to_dir + "/" + filename + ".json", sep="\n")

    else:
        print(
            f"Encountered status code: {response.status_code}. You might want to check it at: https://restfulapi.net/http-status-codes/"
        )


saveResponseAsJson(response_4, filename="github_python_request")


#%% IMAGES IN REQUESTS ****************************************************************************
# Here we get an image:
import requests

response_im = requests.get("https://imgs.xkcd.com/comics/making_progress.png")
print(response_im.json())

# %%
