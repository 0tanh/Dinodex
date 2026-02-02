import ascii_magic
from dotenv import load_dotenv

load_dotenv()

from ..db.dino_classes import Dinosaur

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

NO_DINO = Dinosaur(data, "Mrs Non Exist", "never")
NO_DINO_ASCII = ascii_magic.from_image("src/assets/missing_dino.png")
