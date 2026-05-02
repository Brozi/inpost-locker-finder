from src.ilf.api import InPostFetcher
from src.ilf import ExitCode, ERROR_MESSAGES
from src.ilf import __app_name__, __version__
from typing import Optional
import typer
app = typer.Typer(no_args_is_help=True)

def _version_callback(value: bool):
    #--version command. value: bool passes the state of this command
    #to typer. Its a flag - it either is there or is isnt
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()
@app.callback()
def main(
    _version: Optional[bool] = typer.Option(
        False,
        "--version",
        "-v",
        help=f"Show the {__app_name__}'s version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    """
    inpost-locker-finder (ilf or locker finder for short): A tool for finding
    nearest inpost lockers.
    For help type ilf <command> --help/-h
    """
    return
