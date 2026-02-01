import sqlite3
import os
from dotenv import load_dotenv
import requests

def image_write(img_path:str, img_url:str)->int:
    """Image Writing function
    
    Args:
        img_path: str -> where you want to write the image to
        img_url: str -> url of the image you want to write
    Returns:
        int -> status code of the request for the URL"""
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    pic_res = requests.get(img_url, headers= headers)
    match pic_res.status_code:
        case 200:
            with open(img_path, "wb") as f:
                f.write(pic_res.content)
        case 404:
            print("Image not found")
        case 403:
            print("Not allowed to access this image with the headers provided")
    return pic_res.status_code

def which_path_to_db()->str:
    load_dotenv()
    path_env = os.getenv("PATH_TO_DB")
    if path_env:
        path_to_db = path_env
        return path_to_db
    else:
        p = "~/Dinodex/dinodex.db"
        path_to_db = os.path.expanduser(p)
        return path_to_db

def db_build(path_to_db:str, path_to_schema:str):
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
        curr.execute("SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='requests')")
        requests_check = curr.fetchall()
       
        curr.execute("SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='myDinos')")
        myDinos_check = curr.fetchall()
        
        if myDinos_check[0][0] == 1:
            print("My Dinos table made successfully")
        if requests_check[0][0] == 1:
            print("requests table made successfully")
        
        curr.close()

def log_req(request, response, status, url, elapsed, collected_date, path_to_db):
    """log a dino request"""
    with sqlite3.connect(path_to_db) as conn:
        curr = conn.cursor()
        params = (request, response, status, url, elapsed, collected_date)
        curr.execute("INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?)", params)
        curr.close()

def new_dino()

def last_dino():
    """get the last dino added to the database"""


if __name__ == "__main__":
    path_to_db = "../dinodex.db"
    path_to_schema ="../db/schema.sql"
    db_build(path_to_db,path_to_schema)
    os.remove(path_to_db)