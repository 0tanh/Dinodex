import textual
from textual.widgets import Static, TabbedContent
from textual.widget import Widget
from textual.app import RenderResult, ComposeResult 
from textual.strip import Strip, StripRenderable
import textual.types
from textual.reactive import Reactive, reactive
from textual.containers import VerticalGroup, Grid, ItemGrid, Container
from rich.live import Live


from ..db.dino_classes import Dinosaur

class Dino_Info(Static):
    
    # dino_name = Reactive()
    dino_name = reactive("my name", recompose=True, repaint=True)
    dino_species = reactive("what dino", recompose=True)
    dino_description = reactive("about me", recompose=True)
    dino_period = reactive("from when", recompose=True)
    dino_movement = reactive("how i move", recompose=True)
    
    def __init__(self, dino:Dinosaur|None, id):
        super().__init__()
        self.id = id
        self.dino = dino
    
    def render(self)->RenderResult:
        return ""
    
    def compose(self)->ComposeResult:
        with Container():
            yield Static(self.dino_name)
            yield Static(self.dino_species)
            yield Static(self.dino_description)
            yield Static(self.dino_period)
            yield Static(self.dino_movement)        

class Dino_Pic(Widget):
    
    dino_pic = reactive("", recompose=True)
    
    def __init__(self, dino:Dinosaur|None, id):
            super().__init__()
            self.id = id
            self.dino = dino

    def compose(self):
        yield Static(self.dino_pic)
    
class MatrixNoise(Widget):
    def render_line(self, y) -> Strip:
        
        ...