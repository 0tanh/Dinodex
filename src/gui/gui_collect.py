from ascii_magic import AsciiArt
from rich.errors import MarkupError
from textual.app import App
from textual.widgets import Footer 
from textual.containers import Grid

from assets.no_dino import NO_DINO_ASCII
from db.dino_classes import Dinosaur
from widget.Dino_Widgets import (Dino_Ascii, Dino_Info)

NO_DINO_ASCII

class Dinodex_Collect(App):
    def __init__(self, dino: Dinosaur, dino_ascii: AsciiArt):
        self.dino = dino
        self.dino_ascii = dino_ascii.to_ascii(columns=120, enhance_image=True)
        super().__init__()
        
    def compose(self):
        
        with Grid():
            try:
                yield Dino_Ascii(self.dino_ascii, id="DinoScii")
            except MarkupError:
                yield Dino_Ascii()
            yield Dino_Info(self.dino, id="Dino_Info")
        yield Footer()