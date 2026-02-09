"""All cli logic lives here"""
import os
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

from rich.errors import MarkupError
from rich.panel import Panel
from rich.console import Console
from rich.live import Live 

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from InquirerPy.base.control import Choice

from PIL import UnidentifiedImageError

from typing import Annotated

from async_typer import AsyncTyper

import ascii_magic

from gui.gui_collect import Dinodex_Collect

from config.config import (
    PATH_TO_CONFIG,
    PATH_TO_SCHEMA,
    config_to_dict,
    name_config,
    images_path_config,
    dinodex_path_config,
    config_write,
    load_config,
    all_config
)

from db.writing import (db_build, 
    log_req, 
    which_path_to_db, 
    which_path_to_images,
    which_path_to_config,
    image_write,
    new_dino,
    ascii_dino_from_url,
    write_permission_check,
    ascii_dino_from_db,
    print_no_dino,
    DBWriteError
    )

from db.dino_classes import Dinosaur

from assets.no_dino import (
    # NO_DINO, 
    NO_DINO_IMG_PATH)

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
    path_to_config = which_path_to_config()
    all_config(path_to_config)
    
    config = load_config()
    #TODO readd the b here to fix
    path_to_db = which_path_to_db(config)
    if path_to_db:
        if os.path.exists(path_to_db):
            print("removing old Db")
            os.remove(path_to_db)
        db_build(path_to_db, path_to_schema=PATH_TO_SCHEMA)
        
        if write_permission_check(path_to_db):
            pass
        else:
            raise DBWriteError("Unable to write to this database on initialisation")
    else:
        path_to_db = f"{config.dinodex_path}"
        db_build(path_to_db, path_to_schema="src/assets/schema.sql")
        if not write_permission_check(path_to_db):
            raise DBWriteError("Unable to write to this database on initialisation")
    
    console.print(f"Welcome to the dinodex [bold]{config.name}[/bold]! \n")
    console.print("Run [italics bold] dinodex collect [/italics bold] to start collecting dinos\n")
    console.print("Dinos can be very shy, so sometimes you have to look around for a bit before you see a dino...")

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
            # dino_obj = NO_DINO
            # img_path = which_path_to_images(dino_obj.imageURL, config)
            # dino_ascii = ascii_dino_from_url(img_path=img_path, img_url=dino_obj.imageURL)
            # gui_collect = Dinodex_Collect(dino_obj, dino_ascii)
            
            # gui_collect.run()
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
            
            print("You have met...", end="")
            
            # time.sleep(3)
            # print(".",end="")
            # time.sleep(3)
            # print(".",end="")
            # time.sleep(3)
            # print(".",end="")
            # time.sleep(3)
            
            name = f"[bold green]{dino_obj.name}[/bold green]"
            
            console.print(f"{name}\n")
            
            console.print(f"{name} is a {dino_obj.species} from the {dino_obj.period} \n")
            
            desc_copy = f"[italics]{dino_obj.description}[/italics]"
            
            # print(name_copy)
            with Live(Panel(""),console=console, refresh_per_second=2) as live:
                dino_str = ""
                for c in desc_copy:
                    dino_str += c
                    live.update(Panel(dino_str, 
                        # title=dino_obj.name, 
                        subtitle=dino_obj.species,
                        padding=(1,1),
                        safe_box=True),refresh=True)
                    
            
            with console.status("Photographing dino ..."):
                img_response = image_write(img_path, dino_obj.imageURL)
                match img_response:
                    case 200:
                        try:
                            ascii_dino = ascii_magic.from_image(img_path)
                        except UnidentifiedImageError:
                            ascii_dino = ascii_magic.from_image(NO_DINO_IMG_PATH)
                        try:
                            
                            with Live(Panel(""),console=console, refresh_per_second=0.05) as live:
                                stringy_dino = ascii_dino.to_ascii(enhance_image=True)
                                dino_str = ""
                                for c in stringy_dino:
                                    dino_str += c
                                    live.update(Panel(dino_str, 
                                        title=dino_obj.name, 
                                        subtitle=dino_obj.species,
                                        padding=(1,1),
                                        safe_box=True),refresh=True)
                                    time.sleep(0.00001)
                            console.print(f"[bold blue][link={dino_obj.imageURL}]View here[/link][/bold blue]")
                        except MarkupError:
                            print("There was an error making this dino ascii!")
                            print_no_dino()
                            new_dino(dino_obj, path_to_db, NO_DINO_IMG_PATH, img_response, config)
                            return
                    case 404:
                        print("We couldn't find a picture of this dino...")
            if write_permission_check(path_to_db):
                new_dino(dino_obj, path_to_db, img_path, img_response, config)
            else:
                raise DBWriteError("Unable to log new dino")
             
            return dino_obj
                
        except httpx.ReadTimeout:
            print("Search unsuccessful...")
            print_no_dino()
            # return NO_DINO


@cli.command(name="gallery", help="All your dino pics!")
def gallery():
    console = Console()
    config = load_config()
    path_to_db = which_path_to_db(config)
    with sqlite3.connect(path_to_db) as conn:
        curr = conn.cursor()
        curr.execute("SELECT image, name, imageURL, collected_date FROM myDinos",)
        r = curr.fetchall()
        curr.close()
    
    if len(r) == 0:
        print("You have no photographed dinos!")
        print_no_dino()
        return
    i = 0    
    while i < 2 * len(r):
        for dino in r:
            ascii_dino = ascii_dino_from_db(dino[0])
            name = dino[1]
            
            with Live(Panel(""),console=console, refresh_per_second=4) as live:
                stringy_dino = ascii_dino.to_ascii(enhance_image=True)
                dino_str = ""
                for c in stringy_dino:
                    dino_str += c
                    live.update(Panel(dino_str, 
                        title=name, 
                        subtitle=dino[3],
                        padding=(1,1),
                        safe_box=True),refresh=True)
                    # time.sleep(0.00001)
            # print(name)
            console.print(f"[bold blue][link={dino[2]}]View an HD version here[/link][/bold blue]")
            print("\n")
            time.sleep(3)
            i += 1

@cli.command(name="mydinos", help="Look through your dinos!")
def my_dino_cli():
    console = Console()
    config = load_config()
    path_to_db = which_path_to_db(config)
    while True:
        print(f"{config.name}'s dinodex")
        with sqlite3.connect(path_to_db) as conn:
            curr = conn.cursor()
            curr.execute("SELECT name, species, description FROM mydinos")
            r = curr.fetchall()
            choices = [f[0] for f in r]
            if len(choices) == 0:
                print("You have caught no dinos!")
                print_no_dino()
                return
            
            choices.append("Quit")
            
            which_dino = inquirer.select(qmarkan HD version ="🦖",amark= "🦕",message="Your Dinos!",choices=choices).execute()
            print(which_dino)
            if which_dino == "Quit3:
                curr.close()
                return
            else:
                curr.execute(f"SELECT image, imageURL FROM myDinos WHERE name = '{which_dino}'",)
                r = curr.fetchone()
                ascii_dino = ascii_dino_from_db(r[0])
                console.print(ascii_dino.to_ascii(enhance_image=True))
                console.print(f"[bold blue][link={r[1]}]View here[/link][/bold blue]")
                time.sleep(5)
                curr.close()
        

@cli.command(name="dinofight! #TODO", help="Fight!")
def dinofight():
    print("TODO")
    ...

@cli.command(name="sanity", 
    help="Sanity check info about the current config",
    hidden=True)
def sanity():
    print("Config is currently arranged as such:")
    
    print(f"path to config is {PATH_TO_CONFIG}")
    config = load_config()
    
    config_dict = config_to_dict(config)
    
    for k, v in config_dict.items():
        print(k, v)
    

@cli.command(name="config", help="Configure your Dinodex")
def dino_config():
    path_to_config = which_path_to_config()
    if os.path.exists(path_to_config):
        print("Reconfiguring...")
        config = load_config()
        choices = [
            Choice(name="All", value=0),
            Choice(name="Username", value=1),
            Choice(name="Dinodex path", value=2),
            Choice(name="Images", value=3),
            Choice(name="Exit", value=-1)
        ]
        
        to_config = inquirer.select(qmark="🦖",
            amark= "🦕",
            message="Select what you would like to configure",
            choices=choices).execute()
        match to_config:
            case -1:
                print("Configuration unchanged")
                return
            case 0:
                all_config(path_to_config)
                return
            case 1:
                name = name_config()
                config.name = name
                data = config_to_dict(config)
                config_write(path_to_config, data)
                
            case 2:
                dinodex_path = dinodex_path_config(config)
                config.dinodex_path = dinodex_path
                data = config_to_dict(config)
                config_write(path_to_config, data)
                
            case 3:
                image_save, images_path=images_path_config(config)
                config.image_save, config.images_path = image_save, images_path
                data = config_to_dict(config)
                config_write(path_to_config, data)
    else:
       all_config(path_to_config) 

@cli.command(name="exportdino",help="Export a single dino")
def exportSingle():
    console = Console()
    config = load_config()
    path_to_db = which_path_to_db(config)
    
    
    
    while True:
        print(f"{config.name}'s dinodex")
        with sqlite3.connect(path_to_db) as conn:
            curr = conn.cursor()
            curr.execute("SELECT name, species, description FROM mydinos")
            r = curr.fetchall()
            choices = [f[0] for f in r]
            if len(choices) == 0:
                print("You have caught no dinos!")
                print_no_dino()
                return
            
            choices.append("Quit")
            
            which_dino = inquirer.select(qmarkan HD version ="🦖",amark= "🦕",message="Your Dinos!",choices=choices).execute()
            print(which_dino)
            if which_dino == "Quit":
                curr.close()
                return
            else:
                curr.execute(f"CREATE TABLE SELECT name, species, image, imageURL, description, collected_date FROM myDinos WHERE name = '{which_dino}'",)
                r = curr.fetchone()
                
                curr.close()
    ...

@cli.command(name="export", help="Export your dinodex!")
def exportDinodex():
    """Export your dino dex collection"""
    config = load_config()
    collection_name = inquirer.text(
        qmark="🦖",
        amark="🦕",
        message="What's the name of this collection?"
    ).execute()
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
    dinodex_suff = ".dex"
    db_change = os.path.expanduser(f"{where_to}/{user_name}_{collection_name}{dinodex_suff}")
    my_baselocation.touch()
    shutil.copy2(my_baselocation, db_change)
    console.print("You have exported a [green]dinodex[/green]!")

@cli.command(name="import", help="Import a dinodex!")
def importDinodex():
    config = load_config()
    where_from = inquirer.filepath(
        qmark="🦖",
        amark="🦕",
        instruction="Please select a .dex file!",
        message="Where from?",
        validate=PathValidator(is_file=True, 
            message="Please select a file")
    ).execute()
    
    full_path = os.path.expanduser(where_from)
    
    shutil.copy2(full_path, config.dinodex_path)
    print("You have imported a new dinodex!")

@cli.command(name="unint", help="uninstalls the dinodex", hidden=True)
def uninstall():
    ...    
    