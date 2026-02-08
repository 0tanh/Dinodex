from textual.widgets import Static 
from textual.widget import Widget
from textual.app import RenderResult, ComposeResult 
from textual.strip import Strip 
from textual.reactive import  reactive
from textual.containers import  Container
from textual.screen import Screen

from src.assets.no_dino import NO_DINO

from ..db.dino_classes import Dinosaur

NO_DINO

class Dino_Info_Reactive(Static):
    """Custom Widget to Display Dino Info"""
    # dino_name = Reactive()
    dino_name = reactive(NO_DINO.name, recompose=True, repaint=True)
    dino_species = reactive(NO_DINO.species, recompose=True)
    dino_description = reactive(NO_DINO.description, recompose=True)
    dino_period = reactive(NO_DINO.period, recompose=True)
    dino_movement = reactive(NO_DINO.movement, recompose=True)
    
    def __init__(self, dino:Dinosaur|None, id=''):
        super().__init__()
        self.id = id
        # self.dino = dino
    
    def render(self)->RenderResult:
        return ""
    
    def compose(self)->ComposeResult:
        with Container():
            yield Static(self.dino_name)
            yield Static(self.dino_species)
            yield Static(self.dino_description)
            yield Static(self.dino_period)
            yield Static(self.dino_movement)        

class Dino_Info(Static):
    """Custom Widget to Display Dino Info"""
    # dino_name = Reactive()
    
    def __init__(self, dino:Dinosaur, id=''):
        super().__init__()
        self.id = id
        self.dino = dino
    
    def render(self)->RenderResult:
        return ""
    
    def compose(self)->ComposeResult:
        with Container():
            yield Static(self.dino.name)
            yield Static(self.dino.species)
            yield Static(self.dino.description)
            yield Static(self.dino.period)
            yield Static(self.dino.movement) 

class Dino_Ascii_Reactive(Static):
    dino_ascii = reactive("%", recompose=True, repaint=True)
    
    def compose(self)->ComposeResult:
        yield Static(self.dino_ascii)
    
class Dino_Ascii(Static):
    
    def compose(self)->ComposeResult:
        yield Static(self.content)
 
#TODO
class Dino_Pic(Screen):
    
    dino_pic = reactive("", recompose=True)
    
    def __init__(self):
            super().__init__()
            # self.id = id
            # self.dino = dino

    def compose(self):
        yield Static(self.dino_pic)

class Dino_Collect_With_Pic(Screen):
    
    def compose(self):
        yield Dino_Info(None)
        yield 
        

class MatrixNoise(Widget):
    def render_line(self, y) -> Strip:
        
        ...