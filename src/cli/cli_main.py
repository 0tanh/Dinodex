import os
import json
import shutil
from pathlib import Path
import time
import sqlite3
import httpx
from dotenv import load_dotenv
import datetime
import faker
import typer
import nest_asyncio
from rich.prompt import Prompt
from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from PIL import UnidentifiedImageError

from typing import Annotated

from async_typer import AsyncTyper

from rich.console import Console
from rich.live import Live 

import ascii_magic

from src.gui.gui_collect import Dinodex_Collect

from ..config.config import (
    name_config,
    images_path_config,
    dinodex_path_config,
    config_write,
    load_config,
    Config,
    PATH_TO_CONFIG,
    all_config
)

from ..db.writing import (db_build, 
    log_req, 
    which_path_to_db, 
    which_path_to_images,
    which_path_to_config,
    image_write,
    new_dino,
    ascii_dino_from_url,
    write_permission_check,
    ascii_dino_from_db,
    WORKING_DB,
    DBWriteError,
    )

from ..db.dino_classes import Dinosaur

from ..assets.no_dino import NO_DINO, NO_DINO_IMG_PATH

STYLE = {}
KEYBINDINGS = {}


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
    dino_config()
    
    config = load_config()
    #TODO readd the b here to fix
    path_to_db = os.getenv("PATH_TO_D") 
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
        path_to_db = f"{config.dinodex_path}"
        db_build(path_to_db, path_to_schema="src/assets/schema.sql")
        if write_permission_check(path_to_db):
           return
        else:
            raise DBWriteError("Unable to write to this database on initialisation")

@cli.async_command(name="collect", help="Collect a new Dinosaur!")
async def collect(gui:Annotated[bool, typer.Option(help="Explore collection with a GUI")]= False):
    """Collect a dinosaur!"""
    # spin = Spinner(name="Looking for dinos...", style="dots")
    config = load_config()
    
    path_to_db = which_path_to_db(config)
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
            img_path = which_path_to_images(dino_obj.imageURL, config)
            
            img_response = image_write(img_path, dino_obj.imageURL)
            if write_permission_check(path_to_db):
                new_dino(dino_obj, path_to_db, img_path, img_response, config)
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
            img_path = which_path_to_images(dino_obj.imageURL, config)
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
            img_path = which_path_to_images(dino_obj.imageURL, config)
            
            print(dino_obj.name)
            print(dino_obj.description)
            
            with console.status("Photographing dino ..."):
                img_response = image_write(img_path, dino_obj.imageURL)
                match img_response:
                    case 200:
                        try:
                            ascii_dino = ascii_magic.from_image(img_path)
                        except UnidentifiedImageError:
                            ascii_dino = ascii_magic.from_image(NO_DINO_IMG_PATH)
                        with Live(console=console, refresh_per_second=0.5):
                            console.print(ascii_dino.to_ascii(enhance_image=True))
                    case 404:
                        print("We couldn't find a picture of this dino...")
            if write_permission_check(path_to_db):
                new_dino(dino_obj, path_to_db, img_path, img_response, config)
            else:
                raise DBWriteError("Unable to log new dino")
             
            return dino_obj
                
        except httpx.ReadTimeout:
            print("Search unsuccessful...")
            return NO_DINO


@cli.command(name="gallery", help="All your dino pics!")
def gallery():
    console = Console()
    config = load_config()
    path_to_db = which_path_to_db(config)
    while True:
        with sqlite3.connect(path_to_db) as conn:
            curr = conn.cursor()
            curr.execute("SELECT image, name FROM myDinos",)
            r = curr.fetchall()
            if len(r) == 0:
                print("You have no photographed dinos!")
                break
            for dino in r:
                ascii_dino = ascii_dino_from_db(dino[0])
                name = dino[1]
                console.print(ascii_dino.to_ascii(enhance_image=True))
                print(name)
                time.sleep(5)
            curr.close()

@cli.command(name="mydinos", help="mydinos <3")
def my_dino_cli():
    console = Console()
    config = load_config()
    path_to_db = which_path_to_db(config)
    while True:
        with sqlite3.connect(path_to_db) as conn:
            curr = conn.cursor()
            curr.execute("SELECT name, species, description FROM mydinos")
            r = curr.fetchall()
            choices = [f[0] for f in r]
            if len(choices) == 0:
                print("You have caught no dinos!")
                return
            which_dino = inquirer.select(qmark="🦖",amark= "🦕",message="Your Dinos!",choices=choices).execute()
            print(which_dino)
            curr.execute(f"SELECT image FROM myDinos WHERE name = '{which_dino}'",)
            r = curr.fetchone()
            ascii_dino = ascii_dino_from_db(r[0])
            console.print(ascii_dino.to_ascii(enhance_image=True))
            time.sleep(5)
            curr.close()
    

@cli.command(name="dinofight!", help="Fight!")
def dinofight():
    
    ...

@cli.command(name="config", help="Configure your Dinodex")
def dino_config():
    old_db_path = ""
    old_images_path = ""
    path_to_config = which_path_to_config()
    if os.path.exists(path_to_config):
        print("Reconfiguring...")
        config = load_config()
        old_db_path = config.dinodex_path
        old_images_path = config.images_path
        
    else:
        all_config(path_to_config)
        


@cli.command(name="export", help="Export your dinodex!")
def exportDinodex():
    """Export your dino dex collection"""
    config = load_config()
    
    where_to = inquirer.filepath(
        qmark="🦖",
        amark="🦕",
        message="Where to?",
        validate=PathValidator(is_dir=True, 
            message="Please select a directory")
    ).execute()
    p = "src/dinodex.db"
    my_baselocation = Path(p)
    
    user_name = config.name
    dinodex_suff = ".dino"
    db_change = os.path.expanduser(f"{where_to}/{user_name}_dex{dinodex_suff}")
    my_baselocation.touch()
    shutil.copy2(my_baselocation, db_change)
    print("You have exported a [green]dinodex[/green]!")

@cli.command(name="import", help="Import a dinodex!")
def importDinodex():
    config = load_config()
    where_from = inquirer.filepath(
        qmark="🦖",
        amark="🦕",
        instruction="Please select a .dino file!",
        message="Where from?",
        validate=PathValidator(is_file=True, 
            message="Please select a file")
    ).execute()
    full_path = os.path.expanduser(where_from)
    p = config.dinodex_path
    shutil.copy2(full_path, p)
    print("You have imported a new dinodex!")
    
    