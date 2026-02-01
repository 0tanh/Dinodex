import httpx

from rich import panel
import typer
import textual
from textual import on
from textual.widgets import Header, Footer,Static, Button
from textual.containers import Grid, Itemgrid
from textual.app import App, ComposeResult

from ..cli.cli_main import collect
from ..widget.Dino_Widgets import (MatrixNoise, Dino_Info, Dino_Pic)

class Dinodex(App): 
    def compose(self):
        yield Header()
        with Grid():
            yield Button("collect!", name="Collect", id="CollectButton")
            yield Dino_Info(None, id="Dino_Info")
            yield Dino_Pic(None, id="Dino_Pic")
        yield Footer()
    
    @on(Button.Pressed, "#CollectButton")
    async def collect_callback(self):
        async with httpx.AsyncClient():
            dino = await collect()
        
        dino_info = self.query_one("#Dino_Info")
        dino_info.dino_name = dino.name 
        dino_info.dino_species = dino.species 
        dino_info.dino_description = dino.description 
        dino_info.dino_period = dino.period 
        dino_info.dino_movement = dino.movement
        
        dino_pic = self.query_one("#Dino_Pic")
        dino_pic.dino_pic = dino.imageURL

if __name__ == "__main__":
    app = Dinodex()
    app.run() 