import os
import httpx
from dotenv import load_dotenv
import datetime
import faker

from PIL import UnidentifiedImageError

from typing import Annotated

from async_typer import AsyncTyper

from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from rich.live import Live 
from rich.spinner import Spinner

import ascii_magic

from ..db.writing import (db_build, 
    log_req, 
    which_path_to_db, 
    which_path_to_images,
    image_write,
    new_dino
    )

from ..db.dino_classes import Dinosaur

load_dotenv()

cli = AsyncTyper()
console = Console()
fake = faker.Faker()

timeout = httpx.Timeout(30.0, connect=30.0)


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
        db_build(path_to_db, path_to_schema="src/db/schema.sql")
        return


@cli.async_command(name="collect", help="Collect a new Dinosaur!")
async def collect(gui:Annotated()):
    """Collect a dinosaur!"""
    # spin = Spinner(name="Looking for dinos...", style="dots")
    path_to_db = which_path_to_db()
    
    try:
        async with httpx.AsyncClient() as client:
            with console.status("Looking for dinos...", spinner_style="bouncing ball"):
                x = await client.get(url="https://restasaurus.onrender.com/api/v1/dinosaurs/random/1")
                
                request = x.request.read()
                response = x.content
                response_status = x.status_code
                url = x.url.path
                elapsed = x.elapsed
                collected_date = datetime.datetime.now().isoformat()
                
                name = f"{fake.first_name_female()} from {fake.company}"
                
                log_req(request, response, response_status, url, 
                    str(elapsed),collected_date,path_to_db)
                
                
                dino_son =  x.json()
                dino_obj = Dinosaur(dino_son, name, collected_date)
        img_path = which_path_to_images(dino_obj.imageURL)
                
        img_response = image_write(img_path, dino_obj.imageURL)
        
        new_dino(dino_obj, path_to_db, img_path, img_response)
        
        print(dino_obj.name)
        print(dino_obj.description)
        
        match img_response:
            case 200:
                try:
                    ascii_dino = ascii_magic.from_image(img_path)
                except UnidentifiedImageError:
                    ascii_dino = ascii_magic.from_image("src/assets/missing_dino.png")
                with Live(console=console, refresh_per_second=0.5):
                    console.print(ascii_dino.to_ascii(enhance_image=True))
                return dino_obj
            case 404:
                print("We couldn't find a picture of this dino...")
        
        return dino_obj
               
    except httpx.ReadTimeout:
        print("Search unsuccessful...")
        return "Search unsuccessful"

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

