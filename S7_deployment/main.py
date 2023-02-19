# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Small aplication as per the description in M22
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Created by Felix Bo Caspersen, s183319 on Tue Jan 17 2023

import re
from enum import Enum
from http import HTTPStatus

from fastapi import FastAPI

app = FastAPI()

# Standard GET function that.. prints "Hello World"..?
@app.get("/")
def read_root():
    return {"Hello": "World"}


# GET function that does something?
@app.get("/")
def root():
    """Health check."""
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
    }
    return response


# GET function
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


class ItemEnum(Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/restrict_items/{item_id}")
def read_item(item_id: ItemEnum):
    return {"item_id": item_id}


@app.get("/query_items")
def read_item(item_id: int):
    return {"item_id": item_id}


database = {"username": [], "password": []}


@app.post("/login/")
def login(username: str, password: str):
    username_db = database["username"]
    password_db = database["password"]
    if username not in username_db and password not in password_db:
        with open("database.csv", "a") as file:
            file.write(f"{username}, {password} \n")
        username_db.append(username)
        password_db.append(password)
    return "login saved"


@app.get("/text_model/")
def contains_email(data: str):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    response = {
        "input": data,
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "is_email": re.fullmatch(regex, data) is not None,
    }
    return response
