import httpx

from rich import panel
import typer
import textual
from textual import on
from textual.widgets import Header, Footer,Static, Button
from textual.app import App, ComposeResult

from ..cli.cli_main import collect

class Dinodex(App): 
    def compose(self):
        yield Header()
        yield Static("Hi betty <3")
        yield Footer()
        yield Button(name="Collect", id="collectbutton")
    
    @on(Button.Pressed, "#collectbutton")
    async def collect_callback():
        async with httpx.AsyncClient():
            dino = await collect()
        return dino