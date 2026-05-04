from src.ilf.format import print_lockers_table
from src.ilf.api import InPostFetcher
from src.ilf import ExitCode, ERROR_MESSAGES
from src.ilf import __app_name__, __version__

from typing import Optional
import typer

app = typer.Typer(no_args_is_help=True,
                  context_settings={"help_option_names": ["-h", "--help"]})
fetcher = InPostFetcher()

@app.command()
def find(
        city:str,
        limit: int = typer.Option(3, "--limit", "-l", help="Number of lockers to display. Example: --limit 10"),
        show_all: bool = typer.Option(False, "--all", "-a", help="Show all lockers found"),
        post_code: str = typer.Option(None, "--post-code", "-p", help="Filter by postal code. Example: --post-code 30, --post-code 31-876"),
        street: str = typer.Option(None, "--street", "-s", help="Filter by street. Example: --street Karmelicka"),
):
    """Find 3 closest operating InPost lockers. \b
    This command downloads all available Inpost lockers for the specified city. By default it sorts them by postal code, and 24/7 availability, displaying the first 3 results.

    You can use the filtering flags (-p, -s) to filter the results of the search. You can also use them together.
    The code can be any number of digits (first one, first two or the entire code), and the street can also be any string, as well
    as the entire address.
    """
    """
    :param city: the name of the city to find lockers for
    :param limit: the number of lockers to display, default=3
    :param show_all: flag to show all lockers found
    :param post_code: filter lockers by postal code
    """
    try:
        typer.secho("Fetching lockers...", fg=typer.colors.BRIGHT_YELLOW)
        lockers = fetcher.get_operating_lockers(city)

        if not lockers:
        #if there are no lockers
            typer.secho(ERROR_MESSAGES[ExitCode.NO_RESULTS], fg=typer.colors.YELLOW)
            raise typer.Exit(code=ExitCode.NO_RESULTS)

        if show_all:
        #if user wants to get all lockers
            limit = len(lockers)

        if post_code:
            lockers = [loc for loc in lockers if loc.address_details_post_code.startswith(post_code)]

            if not lockers:
                typer.secho(f"No lockers found in {city} for postal code {post_code}", fg=typer.colors.YELLOW)
                raise typer.Exit(code=ExitCode.NO_RESULTS)

        if street:
            lockers = [loc for loc in lockers if street.lower() in loc.address_details_street.lower()]

        lockers.sort(key=lambda locker: (locker.address_details_post_code, locker.location_247)
                     ,reverse=False
        )
        #sort lockers by post code and location 24/7 if

        print_lockers_table(lockers, city, limit=limit)

        displayed_count = min(len(lockers), limit)
        typer.secho(f"Success! Found {len(lockers)} lockers in {city}.", fg=typer.colors.GREEN)
        typer.secho(f"Displaying {displayed_count} lockers.", fg=typer.colors.GREEN)
        raise typer.Exit(ExitCode.SUCCESS)

    except typer.Exit:

        raise
    except Exception:
        typer.secho(ERROR_MESSAGES[ExitCode.UNEXPECTED_ERROR], fg=typer.colors.RED)
        raise typer.Exit(code=ExitCode.UNEXPECTED_ERROR)

def _version_callback(value: bool):
    """--version command callback.
    :param value:  passes the state of this command. Checks whether the command is there or not.
    to typer. Its a flag - it either is there or is isnt"""
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit(ExitCode.SUCCESS)

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
    inpost-locker-finder (ilf or locker-finder for short): A tool for finding
    nearest inpost lockers.
    For help type ilf <command> --help/-h
    """
    return
