import shutil
import os
import json

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from InquirerPy.base.control import Choice

PATH_TO_CONFIG = os.path.expanduser("~/Dinodex/config.json")

class Config:
    """Config object
    """
    def __init__(self, data):
        self.name = data["name"]
        self.image_save = data["image_save"]
        self.images_path = data["images_path"]
        self.dinodex_path = data["dinodex_path"]

def config_to_dict(config:Config)->dict:
    config_dict = {
        "name":config.name,
        "image_save": config.image_save,
        "images_path":config.images_path,
        "dinodex_path":config.dinodex_path
    }
    return config_dict

def load_config()->Config:
    """loads to current config

    Returns:
        Config: current config 
    """
    with open(PATH_TO_CONFIG, "r") as con:
        f = json.load(con)
    
    config = Config(f)
    return config 

def name_config():
    """Configure your username"""
    name = inquirer.text(message="What's your name?", qmark="🦖", amark="🦕").execute()
    return name

def dinodex_path_config(config:Config|None=None)->str:
    """Configure where your dinodex is"""
    dinodex_path= inquirer.filepath(
        qmark="🦖",
        amark="🦕",
        message="Where would you like your dinodex?",
        validate=PathValidator(is_dir=True, 
            message="Please select a directory")
    ).execute()
    
    full_dino_path = f"{os.path.expanduser(dinodex_path)}/dinodex.db"
    
    if not os.path.exists(full_dino_path):
        os.mkdir(full_dino_path)
    if config:
        old_db_path = config.dinodex_path
        if old_db_path != dinodex_path:
            shutil.move(src=old_db_path, dst=dinodex_path)
        
    return full_dino_path

def images_path_config(config:Config|None=None)-> tuple:
    """Configure if you images get saved and where"""
    choices = [
            Choice(name="Yes",value =True),
            Choice(name="No",value =False)
        ]
    image_save = inquirer.select(qmark="🦖", amark="🦕",message="Would you like to save your dino photos seperately?", 
        choices = choices).execute()
    
    if image_save:
        stub_images_path = inquirer.filepath(
            qmark="🦖",
            amark="🦕",
            message="Where would you like to save your images?",
            validate=PathValidator(is_dir=True, 
                message="Please select a directory")
        ).execute()
        
        images_path = f"{os.path.expanduser(stub_images_path)}/dino_pics"
        if not os.path.exists(images_path):
            os.mkdir(images_path)
        
        if config:
            print("Moving images")
            old_images_path = config.images_path
            if old_images_path != images_path:
                shutil.move(src=old_images_path, dst=images_path)
    else:
        images_path = ""
    
    return (image_save, images_path)

def config_write(path_to_config:str, config_data:dict)->None:
    """Write to a config"""
    with open(path_to_config, "w") as f:
        json.dump(config_data, f)

def all_config(path_to_config):
    """flow to write full config"""
    
    name = name_config()
    dinodex_path = dinodex_path_config()
    image_save, images_path = images_path_config()
    config_data = {
        "name":name,
        "dinodex_path": f"{dinodex_path}",
        "image_save":image_save,
        "images_path": f"{images_path}",
        }
    
    oldcheck = os.path.exists(path_to_config)
    if oldcheck:
        config = load_config()
        old_db_path = config.dinodex_path
        if old_db_path != dinodex_path:
            shutil.move(src=old_db_path, dst=dinodex_path)
        
        old_images_path = config.images_path
        if old_images_path != images_path:
            shutil.move(src=old_images_path, dst=images_path)
    
    config_write(path_to_config, config_data)