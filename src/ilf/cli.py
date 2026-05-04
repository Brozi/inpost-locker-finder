from src.ilf.format import print_lockers_table, format_json
from src.ilf.api import InPostFetcher
from src.ilf.locker import Locker
from src.ilf import ExitCode, ERROR_MESSAGES
from src.ilf import __app_name__, __version__

from typing import Optional
import typer

app = typer.Typer(no_args_is_help=True,
                  context_settings={"help_option_names": ["-h", "--help"]},
                  rich_markup_mode="markdown",
                  add_completion=False)
fetcher = InPostFetcher()

@app.command(no_args_is_help=True)
def find(
        city:str = typer.Argument(help="The name of the city"),
        limit: int = typer.Option(3, "--limit", "-l", help="Number of lockers to display. Example: --limit 10", rich_help_panel="Display Options"),
        show_all: bool = typer.Option(False, "--all", "-a", help="Show all lockers found", rich_help_panel="Display Options"),
        post_code: str = typer.Option(None, "--post-code", "-p", help="Filter by postal code. Example: --post-code 30, --post-code 31-876", rich_help_panel="Filtering Options"),
        street: str = typer.Option(None, "--street", "-s", help="Filter by street. Example: --street Karmelicka", rich_help_panel="Filtering Options"),
        json_output: bool = typer.Option(False, "--json", "-j", help="Output results in JSON format", rich_help_panel="Output Options"),
):
    """Find operating Inpost lockers in a given city.

    This command downloads all available Inpost lockers for the specified city.\\
    \\
    By default it sorts them by postal code, and 24/7 availability, displaying the first 3 results.\\
    \\
    You can use the filtering flags (-p, -s) to filter the results of the search. You can also use them together.\\
    \\
    The code can be any number of digits (first one, first two or the entire code).\\
    \\
    The street can also be any string, as well as the entire address.
    """
    """
    :param city: the name of the city to find lockers for
    :param limit: the number of lockers to display, default=3
    :param show_all: flag to show all lockers found
    :param post_code: filter lockers by postal code
    """
    try:
        typer.secho("Fetching lockers...", fg=typer.colors.BRIGHT_YELLOW, err=True)

        lockers = fetcher.get_operating_lockers(city)
        found_lockers = len(lockers)
        if not lockers:
            #if there are no lockers
            typer.secho(ERROR_MESSAGES[ExitCode.NO_RESULTS], fg=typer.colors.YELLOW, err=True)
            raise typer.Exit(code=ExitCode.NO_RESULTS)

        lockers = _filter_and_sort_lockers(lockers, post_code, street, limit, show_all)
        if not lockers:
            params_str = _build_params_string(
                post_code=post_code,
                street=street
            )
            typer.secho(f"No lockers found in {city} for given parameters: {params_str}",
                        fg=typer.colors.YELLOW,
                        err=True)
            raise typer.Exit(code=ExitCode.NO_RESULTS)

        if show_all:
            limit = len(lockers)

        if json_output:
            json_str = format_json(lockers)
            typer.echo(json_str)
            typer.secho(f"Success! Found {found_lockers} lockers in {city}.",
                        fg=typer.colors.GREEN,
                        err=True)
        else:
            print_lockers_table(lockers, city, limit=limit)
            displayed_count = min(len(lockers), limit)
            typer.secho(f"Success! Found {found_lockers} lockers in {city}.",
                        fg=typer.colors.GREEN,
                        err=True)
            typer.secho(f"Displaying {displayed_count} lockers.",
                        fg=typer.colors.GREEN,
                        err=True)
        raise typer.Exit(code=ExitCode.SUCCESS)

    except typer.Exit:

        raise

    except Exception as e:
        import traceback
        typer.secho(f"Debug traceback", fg=typer.colors.RED, err=True)
        traceback.print_exc()

        typer.secho(ERROR_MESSAGES[ExitCode.UNEXPECTED_ERROR],
                    fg=typer.colors.RED,
                    err=True)
        raise typer.Exit(code=ExitCode.UNEXPECTED_ERROR)

def _filter_and_sort_lockers(lockers: list[Locker],
    post_code: str | None,
    street: str | None,
    limit: int,
    show_all: bool
) -> list[Locker]:

    if post_code:
        lockers = [loc for loc in lockers if loc.address_details_post_code.startswith(post_code)]

    if street:
        lockers = [loc for loc in lockers if street.lower() in loc.address_details_street.lower()]

    lockers.sort(key=lambda locker: (locker.address_details_post_code, not locker.location_247))
    # sort lockers by post code and location 24/7

    if not show_all:
        # if user wants to get all lockers
        lockers = lockers[:limit]
    return lockers

def _build_params_string(**kwargs) -> str:
    """Builds a comma seperated string of the active search parameters"""
    active_params = []
    for key, value in kwargs.items():
        if value:
            active_params.append(f"{key}='{value}'")
    return ",".join(active_params)



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
    """
    return
