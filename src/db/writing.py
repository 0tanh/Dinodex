"""
Writing to db functions. 

"""
import io
import os
import sqlite3

import ascii_magic
import requests
from dotenv import load_dotenv
from PIL import UnidentifiedImageError
from PIL import Image

from rich.console import Console

from assets.no_dino import (
    NO_DINO_ASCII, 
    NO_DINO_IMG_PATH)

from config.config import (
    Config,
    PATH_TO_CONFIG,
    load_config
)

from db.dino_classes import Dinosaur

full_path = os.path.expanduser("~/Dinodex")
if not os.path.exists(full_path):
    os.mkdir(full_path)

p = "~/Dinodex/dinodex.db"
WORKING_DB = os.path.expanduser(p)

class DBWriteError(Exception):
    """Custom exception for failing to write a database"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def write_permission_check(path_to_db):
    """Diagnostic test to check if this place has write permissions

    Args:
        path_to_db (str): path to the database we are testing
    """
    with sqlite3.connect(path_to_db) as conn:
        curr = conn.cursor()
        try:
            curr.execute("CREATE TABLE permission_check ('check' BOOL)")
            curr.execute(
                "SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='permission_check')"
            )

            r = curr.fetchall()
            if r[0][0] == 1:
                curr.execute("DROP TABLE permission_check")
                return True
            else:
                return False
        except sqlite3.OperationalError as e:
            print(f"Error {e} occurred")
        curr.close()
        return False


def image_write(img_path: str, img_url: str) -> int:
    """Image Writing function

    Args:
        img_path: str -> where you want to write the image to
        img_url: str -> url of the image you want to write
    Returns:
        int -> status code of the request for the URL"""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    pic_res = requests.get(img_url, headers=headers)
    match pic_res.status_code:
        case 200:
            with open(img_path, "wb") as f:
                f.write(pic_res.content)
        case 404:
            print("Image not found")
        case 403:
            print("Not allowed to access this image with the headers provided")
    return pic_res.status_code


def which_path_to_db(config:Config) -> str:
    """Where the database is!! should change in binary vs development"""
    load_dotenv()
    path_env = os.getenv("PATH_TO_DB")
    if path_env:
        print("Testing environment database")
        path_to_db = path_env
    else:
        path_to_db = config.dinodex_path
    return path_to_db

def which_path_to_config()->str:
    load_dotenv()
    path_env = os.getenv("PATH_TO_CONFIG")
    if path_env:
        print("Testing environment config")
        path_to_config = path_env
    else:
        path_to_config = PATH_TO_CONFIG
    return path_to_config

def which_path_to_images(img_url: str, config: Config) -> str:
    """Where Images are being written to! should be different for binary vs dev"""
    load_dotenv()
    config = load_config()
    name = os.path.basename(img_url)
    path_env = os.getenv("PATH_TO_IMG")
    if path_env:
        print("Testing environment images")
        path_to_img = f"{path_env}/{name}"
        return path_to_img
    else:
        path_to_img = f"{config.images_path}/{name}"
        
    return path_to_img


def db_build(path_to_db: str, path_to_schema: str):
    """builds database"""
    if os.path.exists(path_to_db):
        print("Db already exists")
        return
    with open(path_to_schema, "r") as f:
        schema = f.read()

    with sqlite3.connect(path_to_db) as conn:
        curr = conn.cursor()
        print("Building database...")
        curr.executescript(schema)
        curr.execute(
            "SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='requests')"
        )
        # requests_check = curr.fetchall()

        #curr.execute(
        #     "SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='myDinos')"
        # )
        #myDinos_check = curr.fetchall()

        # if myDinos_check[0][0] == 1:
        #     print("My Dinos table made successfully")
        # if requests_check[0][0] == 1:
        #     print("requests table made successfully")

        curr.close()


def log_req(request, response, status, url, elapsed, collected_date, path_to_db):
    """log a dino request"""
    with sqlite3.connect(path_to_db) as conn:
        curr = conn.cursor()
        params = (request, response, status, url, elapsed, collected_date)
        curr.execute("INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?)", params)
        curr.close()


def new_dino(dino: Dinosaur, path_to_db:str, img_path:str, img_response, config:Config):
    load_dotenv()
    match img_response:
        case 200:
            with open(img_path, "rb") as img:
                image_bytes = img.read()
        case _:
            with open(NO_DINO_IMG_PATH) as img:
                image_bytes = img.read()

    with sqlite3.connect(path_to_db) as conn:
        curr = conn.cursor()

        myDino_params = (
            dino.name,
            dino.species,
            image_bytes,
            dino.imageURL,
            dino.description,
            dino.collected_date,
        )

        try:
            curr.execute("INSERT INTO myDinos VALUES (?, ?, ?, ?, ?, ?)", myDino_params)
            allDino_params = (dino.species, 1, True, dino.collected_date)
            curr.execute("INSERT INTO allDinos VALUES (?, ?, ?, ?)", allDino_params)
        except sqlite3.IntegrityError:
            allDino_params = (False, dino.species)
            curr.execute(
                "UPDATE allDinos SET rare = ?, copies = copies + 1 WHERE species = ?",
                allDino_params,
            )

        curr.close()
    if not config.image_save:
        remove_image(img_path)


def remove_image(img_path) -> None:
    """deletes an image

    Args:
        img_path (str): path to image to remove 
    """
    os.remove(img_path)


def last_dino():
    """get the last dino added to the database"""


def ascii_dino_from_url(img_path: str, img_url: str):
    """
    Ascii art of a dinosaur

    Args:
        img_path (str) : path that image will write to
        img_url (str) : url of image
    Return
        AsciiArt : ascii art of a dino
    """
    img_response = image_write(img_path, img_url)
    match img_response:
        case 200:
            try:
                ascii_dino = ascii_magic.from_image(img_path)
                return ascii_dino
            except UnidentifiedImageError:
                return NO_DINO_ASCII
        case 404:
            return NO_DINO_ASCII
        case _:
            return NO_DINO_ASCII

def ascii_dino_from_db(blob):
    workable =io.BytesIO(blob)
    dino_pil = Image.open(workable)
    ascii_dino = ascii_magic.from_pillow_image(dino_pil)
    return ascii_dino

def print_no_dino():
    """prints when no dino is available"""
    # config = load_config()
    console = Console()
    # dino_obj = NO_DINO
    # img_path = which_path_to_images(dino_obj.imageURL, config)
    # ascii_dino = ascii_dino_from_url(img_path=img_path, img_url=dino_obj.imageURL)
    console.print(NO_DINO_ASCII.to_ascii())

if __name__ == "__main__":
    path_to_db = "../dinodex.db"
    path_to_schema = "../db/schema.sql"
    db_build(path_to_db, path_to_schema)
    os.remove(path_to_db)
