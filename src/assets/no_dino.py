import ascii_magic
from dotenv import load_dotenv
import os

from rich.console import Console

from db.dino_classes import Dinosaur

load_dotenv()
data =  {
    "data":[
        {
            "name": "i don't exist oh saurus",
            "description" : "i was never here",
            "image" : {
                "imageURL": "https://images.template.net/560549/Sad-Dinosaur-Clipart-edit-online.webp"
            },
            "temporalRange": "-infinity",
            "locomotionType": "running away lmfao"
        }
    ]
}

missing_dino = os.getenv("PATH_TO_MISSING_DINO")

NO_DINO = Dinosaur(data, "Mrs Non Exist", "never")

if missing_dino:
    NO_DINO_ASCII = ascii_magic.from_image("assets/missing_dino.png")
    NO_DINO_IMG_PATH = "assets/missing_dino.png"
else:
    NO_DINO_ASCII = ascii_magic.from_image("assets/missing_dino.png")
    NO_DINO_IMG_PATH = "assets/missing_dino.png"