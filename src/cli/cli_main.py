import typer
import requests
import os
import sqlite3

from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from rich.live import Live, live_table
from rich.spinner import Spinner
cli = typer.Typer()

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

@cli.command()

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

@cli.command(name="collect", help="Collect a new Dinosaur!")
def collect(count=1):
    spin = Spinner(name="Looking for dinos...", style=)
    with :
        x = requests.get(url="https://restasaurus.onrender.com/api/v1/dinosaurs/random/1")
        dino_son =  x.json()
        dino_obj = Dinosaur(dino_son)
    
    print(dino_obj.name)
    print(dino_obj.description)
    print(dino_obj.imageURL)
    
    name = os.path.basename(dino_obj.imageURL)
    path = f"src/images/{name}"
    r = image_write(path, dino_obj.imageURL)

        
        
    # return dino_obj