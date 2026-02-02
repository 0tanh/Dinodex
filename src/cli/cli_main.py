import os
import httpx
from dotenv import load_dotenv
import datetime
import faker
import typer
import nest_asyncio

from PIL import UnidentifiedImageError

from typing import Annotated

from async_typer import AsyncTyper

from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from rich.live import Live 
from rich.spinner import Spinner

import ascii_magic

from src.gui.gui_collect import Dinodex_Collect

from ..db.writing import (db_build, 
    log_req, 
    which_path_to_db, 
    which_path_to_images,
    image_write,
    new_dino,
    ascii_dino_from_url,
    write_permission_check,
    DBWriteError
    )

from ..db.dino_classes import Dinosaur

from ..assets.no_dino import NO_DINO

load_dotenv()
nest_asyncio.apply()
cli = AsyncTyper()
console = Console()
fake = faker.Faker()

timeout = httpx.Timeout(30.0, connect=30.0)


@cli.command(name="init", help="Start Your Dino Journey!")
def initialise():
    """Rebuilds Database from scratch and initialises your user"""
    
    load_dotenv()
    #TODO customise location of db_path
    
    path_to_db = os.getenv("PATH_TO_DB")
    if path_to_db:
        print("Test Env..")
        if os.path.exists(path_to_db):
            print("removing old Db")
            os.remove(path_to_db)
        db_build(path_to_db, path_to_schema="src/assets/schema.sql")
        
        if write_permission_check(path_to_db):
            return
        else:
            raise DBWriteError("Unable to write to this database on initialisation")
    else:
        p = "~/Dinodex/dinodex.db"
        path_to_db = os.path.expanduser(p)
        db_build(path_to_db, path_to_schema="src/assets/schema.sql")
        if write_permission_check(path_to_db):
           return
        else:
            raise DBWriteError("Unable to write to this database on initialisation")

@cli.async_command(name="collect", help="Collect a new Dinosaur!")
async def collect(gui:Annotated[bool, typer.Option(help="Explore collection with a GUI")]= False):
    """Collect a dinosaur!"""
    # spin = Spinner(name="Looking for dinos...", style="dots")
    
    path_to_db = which_path_to_db()
    if gui:
        try:
            async with httpx.AsyncClient() as client:
                x = await client.get(url="https://restasaurus.onrender.com/api/v1/dinosaurs/random/1")
                
                request = x.request.read()
                response = x.content
                response_status = x.status_code
                url = x.url.path
                elapsed = x.elapsed
            collected_date = datetime.datetime.now().isoformat()
            name = f"{fake.first_name_female()} from {fake.company()}"
            
            log_req(request, response, response_status, url, 
                str(elapsed),collected_date,path_to_db)
            dino_son =  x.json()
            dino_obj = Dinosaur(dino_son, name, collected_date)
            img_path = which_path_to_images(dino_obj.imageURL)
            
            img_response = image_write(img_path, dino_obj.imageURL)
            if write_permission_check(path_to_db):
                new_dino(dino_obj, path_to_db, img_path, img_response)
            else:
                      
                raise DBWriteError("Unable to log new dino")
            dino_ascii = ascii_dino_from_url(img_path=img_path, img_url=dino_obj.imageURL)
            os.remove(img_path)
            gui_collect = Dinodex_Collect(dino_obj, dino_ascii)
            gui_collect.run()
            return dino_obj
        
        except httpx.ReadTimeout:
            print("Search unsuccessful...")
            dino_obj = NO_DINO
            img_path = which_path_to_images(dino_obj.imageURL)
            dino_ascii = ascii_dino_from_url(img_path=img_path, img_url=dino_obj.imageURL)
            gui_collect = Dinodex_Collect(dino_obj, dino_ascii)
            
            gui_collect.run()
    else:
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
                    
                    name = f"{fake.first_name_female()} from {fake.company()}"
                    
                    log_req(request, response, response_status, url, 
                        str(elapsed),collected_date,path_to_db)
                    
                    
                    dino_son =  x.json()
                    dino_obj = Dinosaur(dino_son, name, collected_date)
            img_path = which_path_to_images(dino_obj.imageURL)
            
            print(dino_obj.name)
            print(dino_obj.description)
            
            with console.status("Photographing dino ..."):
                img_response = image_write(img_path, dino_obj.imageURL)
                match img_response:
                    case 200:
                        try:
                            ascii_dino = ascii_magic.from_image(img_path)
                        except UnidentifiedImageError:
                            ascii_dino = ascii_magic.from_image("src/assets/missing_dino.png")
                        with Live(console=console, refresh_per_second=0.5):
                            console.print(ascii_dino.to_ascii(enhance_image=True))
                    case 404:
                        print("We couldn't find a picture of this dino...")
            if write_permission_check(path_to_db):
                new_dino(dino_obj, path_to_db, img_path, img_response)
            else:
                raise DBWriteError("Unable to log new dino")
             
            return dino_obj
                
        except httpx.ReadTimeout:
            print("Search unsuccessful...")
            return NO_DINO


@cli.command(name="config", help="Configure your Dino collection")
def config():
    ...

@cli.command(name="gallery", help="All your dino pics!")
def gallery():
    ...

@cli.command(name="mydino", help="View your dinos")
def view():
    ...

@cli.command(name="dinofight!", help="Fight!")
def dinofight():
    ...

@cli.command(name="export", help="Export your dinodex!")
def exportDinodex():
    ...

@cli.command(name="import", help="Import a dinodex!")
def importDinodex():
    ...
