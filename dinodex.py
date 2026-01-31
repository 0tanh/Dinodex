from typing import Annotated
from src.cli.cli_main import cli
from src.gui.gui_main import Dinodex 

@cli.command(name="gui", help="render a gui with this")
def gui_run():
    app = Dinodex()
    app.run()

if __name__ == "__main__":
    cli()