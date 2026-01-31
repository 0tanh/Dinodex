from rich import panel
import typer
import textual
from textual.widgets import Header, Footer,Static
from textual.app import App, ComposeResult


gui = App()

class Dinodex(App): 
    def compose(self):
        yield Header()
        yield Static("Hi betty <3")
        yield Footer()