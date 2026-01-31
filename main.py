from typing import Annotated
from src.cli.cli_main import cli
from src.gui.gui_main import ProvingThisWorks

@cli.command(name="gui", help="render a gui with this")
def gui_run():
    app = ProvingThisWorks()
    app.run()

if __name__ == "__main__":
    cli()