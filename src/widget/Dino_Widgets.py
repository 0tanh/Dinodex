import textual
from textual.widgets import Static
from textual.widget import Widget, 
from textual.app import RenderResult, VisualType
from textual.types import VisualType
from rich.live import Live


from db.dino_classes import Dinosaur

class Dinobox(Static):
    def __init__(self, dino:Dinosaur, content: VisualType = "", *, expand: bool = False, shrink: bool = False, markup: bool = True, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.dino = dino
        super().__init__(content, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)
    
    def __init_subclass__(cls, dino: Dinosaur, can_focus: bool | None = None, can_focus_children: bool | None = None, inherit_css: bool = True, inherit_bindings: bool = True) -> None:
        
        return super().__init_subclass__(can_focus, can_focus_children, inherit_css, inherit_bindings)
    
    def render(self)->RenderResult:
        return Static()