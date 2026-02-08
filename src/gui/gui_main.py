import httpx
from textual import on
from textual.app import App
from textual.containers import Grid
from textual.widgets import Button, Footer, Header

from rich.console import Console

from ..cli.cli_main import collect
from ..widget.Dino_Widgets import Dino_Info_Reactive, Dino_Ascii_Reactive
from ..db.writing import ascii_dino_from_url, which_path_to_images

class Dinodex(App):
    
    BINDING = [("c", "push_screen('DinoPic')")]
    
    console = Console()
    def compose(self):
        yield Header()
        with Grid():
            yield Dino_Ascii_Reactive(id="DinoScii")
            yield Button("collect!", name="Collect", id="CollectButton")
            yield Dino_Info_Reactive(None, id="Dino_Info")
            # yield Dino_Pic(id="Dino_Pic")
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
        
        dino_url = dino.imageURL
        
        img_path = which_path_to_images(dino_url)
        dino_ascii_obj = ascii_dino_from_url(img_path, dino_url)
        
        dino_ascii_raw = dino_ascii_obj.to_ascii(columns=120,
                                            enhance_image = True)
        
        dino_scii = self.query_one("#DinoScii")
        dino_scii.dino_ascii = dino_ascii_raw



if __name__ == "__main__":
    app = Dinodex()
    app.run()
