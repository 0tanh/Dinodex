from rich import panel
import typer
import textual
from textual.widgets import Header, Footer,Static
from textual.app import App, ComposeResult

from ..cli.cli_main import hello_world

gui = App()

class Dinodex(App): 
    def compose(self):
        yield Header()
        yield Static("Hi betty <3")
        yield Static(f"{hello_world()}")
        yield Footer()