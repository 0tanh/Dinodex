import requests
import os
import sqlite3
import aiohttp
import httpx
import asyncio 
from dotenv import load_dotenv
import pathlib
import datetime

from typing import Annotated

from async_typer import AsyncTyper

from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from rich.live import Live 
from rich.spinner import Spinner

import ascii_magic

from ..db.db_writing import db_build, log_req, path_to_db

load_dotenv()

cli = AsyncTyper()
console = Console()

timeout = httpx.Timeout(30.0, connect=30.0)

class Dinosaur:
    def __init__(self, response):
        self.name = response["data"][0]["name"]
        self.description = response["data"][0]["description"]
        self.imageURL = response["data"][0]["image"]["imageURL"]
        self.period = response["data"][0]["temporalRange"]
        self.movement = response["data"][0]["locomotionType"]
    # {
    #   "count": 5,
    #   "data": [
    #     {
    #       "id": 1118,
    #       "name": "Zephyrosaurus",
    #       "temporalRange": "Early Cretaceous, ~113 Ma",
    #       "diet": "herbivore",
    #       "locomotionType": "biped",
    #       "description": "...",
    #       "classificationInfo": {...},
    #       "image": {...},
    #       "source": {...}
    #     }
    #   ]
    # }
def which_path()->str:
    load_dotenv()
    path_to_db = os.getenv("PATH_TO_DB")
    if path_to_db:
        return path_to
    return path_to_db

@cli.command(name="init", help="Start Your Dino Journey!")
def initialise():
    load_dotenv()
    #TODO customise location of db_path
    path_to_db = os.getenv("PATH_TO_DB")
    if path_to_db:
        print("Test Env..")
        if os.path.exists(path_to_db):
            print("removing old Db")
            os.remove(path_to_db)
        db_build(path_to_db, path_to_schema="src/db/schema.sql")
        return
    else:
        p = "~/Dinodex/dinodex.db"
        path_to_db = os.path.expanduser(p)
        db_build(path_to_db, path_to_schema="../db/schema.sql")
        return

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

@cli.async_command(name="collect", help="Collect a new Dinosaur!")
async def collect(count=1):
    # spin = Spinner(name="Looking for dinos...", style="dots")
    load_dotenv()
    
    try:
        async with httpx.AsyncClient() as client:
            with console.status("Looking for dinos...", spinner_style="bouncing ball"):
                x = await client.get(url="https://restasaurus.onrender.com/api/v1/dinosaurs/random/1")
                
                request = x.request
                response = x.content
                response_status = x.status_code
                url = x.url
                elapsed = x.elapsed
                collected_date = datetime.datetime.now().isoformat()
                
                log_req(request, 
                    response,
                    response_status,
                    url,
                    str(elapsed),
                    collected_date,
                    )
                
                dino_son =  x.json()
                
                dino_obj = Dinosaur(dino_son)
        
        print(dino_obj.name)
        print(dino_obj.description)
        
        name = os.path.basename(dino_obj.imageURL)
        path = f"src/images/{name}"
        
        img_response = image_write(path, dino_obj.imageURL)
        
        match img_response:
            case 200:
                ascii_dino = ascii_magic.from_image(path)
                with Live(console=console, refresh_per_second=3):
                    console.print(ascii_dino.to_ascii(enhance_image=True))
                return dino_obj
            case 404:
                print("We couldn't find a picture of this dino...")
                
    except httpx.ReadTimeout:
        print("hunt unsuccesful...")

@cli.command(name="config", help="Configure your Dino collection")
def config():
    ...

@cli.command(name="gallery", help="All your dino pics!")
def gallery():
    ...

@cli.command(name="view", help="View your dinos")
def view():
    ...

@cli.command(name="dinofight!", help="Fight!")
def dinofight():
    ...

