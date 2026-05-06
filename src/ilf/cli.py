from ilf.format import print_lockers_table, format_json
from ilf.api import InPostFetcher
from ilf.locker import Locker
from ilf import ExitCode, ERROR_MESSAGES
from ilf import __app_name__, __version__

import requests.exceptions
from typing import Optional
from rich.console import Console
from rich.panel import Panel

import typer
import sys
import locale
err_console = Console(stderr=True)
console = Console()


app = typer.Typer(no_args_is_help=True,
                  context_settings={"help_option_names": ["-h", "--help"]},
                  rich_markup_mode="markdown",
                  add_completion=False)
fetcher = InPostFetcher()

@app.command(no_args_is_help=True,
             epilog="**Examples:**\n\n\n\n* `ilf find Kraków` (Finds default amount of lockers)\n\n\n\n* `ilf find 31-876 --24h` (Finds 24/7 lockers in a specific postal code)\n\n\n\n* `ilf find Warszawa -s \"Złota\" --all` (Finds all lockers on Złota street)"
             )
def find(
        location:Optional[str] = typer.Argument(None, help="The name of the city or the postal code to search", metavar="TEXT: CITY/POSTCODE", show_default=False, ),
        limit: int = typer.Option(15, "--limit", "-l", help="Number of lockers to display. **Example:** `--limit 10`", rich_help_panel="Display Options"),
        show_all: bool = typer.Option(False, "--all", "-a", help="Show all lockers found", rich_help_panel="Display Options"),
        post_code: str = typer.Option(None, "--post-code", "-p", help="Filter by postal code. **Example:** `--post-code 30`, `--post-code 31-876`", rich_help_panel="Filtering Options"),
        street: str = typer.Option(None, "--street", "-s", help="Filter by street. **Example:** `--street Karmelicka`", rich_help_panel="Filtering Options"),
        location_247: bool = typer.Option(False, "--24h", "-d", help="Filter by the point being open *24/7*.", rich_help_panel="Filtering Options"),
        easy_access_zone: bool = typer.Option(False, "--easy-access-zone", "-e", help="Filter by the point having the Easy Access Zone", rich_help_panel="Filtering Options"),
        json_output: bool = typer.Option(False, "--json", "-j", help="Output results in JSON format", rich_help_panel="Output Options"),
):
    """Find operating InPost points in a given city/postal code. For help type **`ilf find --help`**

    This command downloads and displays all available Inpost points for the specified **city** or **postal code**.\\
    By default it sorts them by **postal code**, and **24/7** availability, displaying the first **15* results.\\
    You can use the display options (`-l`, `-a`) to control how the lockers are displayed. \\
    The flag `-j` can be used to render the output in json for pipe ability \\
    You can use the **filtering flags** (`-p`, `-s`, `-e`, `-d`) to filter the results of the search. You can also use them together.\\
    The code can be **any** number of digits (first one, first two or the entire code).\\
    The street can also be **any** string, as well as the entire address.\
    """
    """
    :param city: the name of the city to find lockers for
    :param limit: the number of lockers to display, default=3
    :param show_all: flag to show all lockers found
    :param post_code: filter lockers by postal code
    """
    if not location:
        if not sys.stdin.isatty():
            raw_data = sys.stdin.buffer.read()

            try:
                # 2. Try decoding as UTF-8 (with BOM support)
                location = raw_data.decode('utf-8-sig').strip()
            except UnicodeDecodeError:
                # 3. Fallback: Use the system's local codepage (e.g., CP1250 in Poland)
                # This fixes the error when files are saved in legacy Windows formats
                location = raw_data.decode(locale.getpreferredencoding(), errors='replace').strip()
        else:
            err_console.print(
                Panel(f"{ERROR_MESSAGES[ExitCode.NO_ARG]}",title="Command Failed", border_style="red", expand=False))
            raise typer.Exit(code=ExitCode.NO_ARG)



    location = location.title()
    search_city = None
    search_postcode = post_code

    if location[0].isdigit():
        search_postcode = location
    else:
        search_city = location
    try:
        api_post_code = search_postcode if not search_city else None
        # if search city empty, api_post_code is post_code
        # this allows the program to query the endpoint based on post_code
        # improves speed
        with err_console.status("[bold yellow]Fetching points from InPost...[/bold yellow]", spinner="dots"):
            lockers = fetcher.get_operating_lockers(city=search_city, post_code=api_post_code)

        if not lockers:
            params_str = _build_params_string(
                location=api_post_code,
                street=street
            )
            #if there are no lockers from the api call
            if not search_city:
                if len(api_post_code) < 5:
                    err_console.print(Panel(f"{ERROR_MESSAGES[ExitCode.NO_RESULTS]}: {params_str}\n{ERROR_MESSAGES[ExitCode.HINT]}",
                                        title="Search Failed", border_style="red", expand=False))
                    raise typer.Exit(code=ExitCode.NO_RESULTS)
                else:
                    err_console.print(
                        Panel(f"{ERROR_MESSAGES[ExitCode.NO_RESULTS]}: {params_str}",
                              title="Search Failed", border_style="red", expand=False))
                    raise typer.Exit(code=ExitCode.NO_RESULTS)

            else:
                params_str = _build_params_string(
                    location=search_city,
                    post_code=post_code,
                    street=street
                )
                err_console.print(Panel(f"{ERROR_MESSAGES[ExitCode.NO_RESULTS]}: {params_str}",title="Search Failed", border_style="red"))
            raise typer.Exit(code=ExitCode.NO_RESULTS)

        lockers, found_lockers = _filter_and_sort_lockers(lockers,
                                           post_code,
                                           street,
                                           limit,
                                           show_all,
                                           location_247,
                                           easy_access_zone
                                           )
        if not lockers:
            params_str = _build_params_string(
                post_code=post_code,
                street=street
            )
            #if there are no lockers after filtering
            err_console.print(Panel(f"[yellow][underline]{location}[/underline]: "
                                    f"{ERROR_MESSAGES[ExitCode.NO_RESULTS_FROM_FILTERING]}: "
                                    f"[italic]{params_str}[/italic][/yellow]",
                        title="Search Failed",
                        border_style="bold yellow", expand=False))
            raise typer.Exit(code=ExitCode.NO_RESULTS)

        if show_all:
            limit = len(lockers)

        displayed_count = min(len(lockers), limit)
        if json_output:
            json_str = format_json(lockers, found_lockers, displayed_count)
            typer.echo(json_str)
            err_console.print(f"[bold green]Success![/bold green] Found [bold]{found_lockers}[/bold] points matching your filters in [cyan]{location}[/cyan].\nJSON Output: {displayed_count} points")
        else:
            print_lockers_table(lockers, location, limit=limit)

            success_text = (
                f"[bold green]Success![/bold green] Found [bold]{found_lockers}[/bold] points matching your filters in [cyan]{location}[/cyan].\n"
                f"Displaying [bold]{displayed_count}[/bold] points."
            )
            err_console.print(Panel(success_text, border_style="green", expand=False))
        raise typer.Exit(code=ExitCode.SUCCESS)

    except typer.Exit:

        raise

    except requests.exceptions.ConnectionError:
        err_console.print(
            Panel(ERROR_MESSAGES[ExitCode.NETWORK_ERROR], title="Network Error", border_style="red"))
        raise typer.Exit(code=ExitCode.NETWORK_ERROR)


    except requests.exceptions.HTTPError as e:
        err_console.print(
            Panel(ERROR_MESSAGES[ExitCode.API_ERROR] + f": {e}", title="Server Error", border_style="red"))
        raise typer.Exit(code=ExitCode.API_ERROR)


    except Exception:
        err_console.print(Panel(ERROR_MESSAGES[ExitCode.UNEXPECTED_ERROR], title="Unexpected Error", border_style="red"))
        raise typer.Exit(code=ExitCode.UNEXPECTED_ERROR)

def _filter_and_sort_lockers(lockers: list[Locker],
    post_code: str | None,
    street: str | None,
    limit: int,
    show_all: bool,
    location_247: bool,
    easy_access_zone: bool,
) -> tuple[list[Locker], int]:

    if easy_access_zone:
        lockers = [locker for locker in lockers if locker.easy_access_zone == "Yes"]

    if location_247:
        lockers = [locker for locker in lockers if "24/7" in locker.opening_hours]

    if post_code:
        lockers = [locker for locker in lockers if locker.address_details_post_code.startswith(post_code)]


    if street:
        lockers = [locker for locker in lockers if street.lower() in locker.address_details_street.lower()]

    lockers.sort(key=lambda locker: (locker.address_details_post_code, not locker.location_247))
    # sort lockers by post code and location 24/7

    found_lockers = len(lockers)

    if not show_all:
        # if user wants to get all lockers
        lockers = lockers[:limit]
    return lockers, found_lockers

def _build_params_string(**kwargs) -> str:
    """Builds a comma seperated string of the active search parameters"""
    active_params = []
    for key, value in kwargs.items():
        if value:
            key = key.replace("_", " ").title()
            active_params.append(f"{key}: [bold]{value}[/bold]")
    return ", ".join(active_params)



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
    inpost-locker-finder (ilf or locker-finder for short): A tool for finding InPost points in a given location.
    """
    return
