import typer
import requests
import os
import sqlite3


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

@cli.command(name="hw", help="simple hello world")
def hello_world():
    print("Hello World!")
    return "Hello World"

@cli.command(name="config", help="Configure your Dino collection")

@cli.command(name="dinosaur", help="Get a random Dinosaur")
def dinosaur(count=1):
    x = requests.get(url="https://restasaurus.onrender.com/api/v1/dinosaurs/random/1")
    dino_son =  x.json()
    dino_obj = Dinosaur(dino_son)
    
    print(dino_obj.name)
    print(dino_obj.description)
    print(dino_obj.imageURL)
    
    dino_pic = requests.get(dino_obj.imageURL)
    if dino_pic.status_code == 200:
        #TODO change this
        name = os.path.basename(dino_obj.imageURL)
        
        with open(f"src/images/{name}", "wb") as f:
            f.write(dino_pic.content)
        
        
        
    # return dino_obj