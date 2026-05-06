import json

from rich.console import Console
from rich.table import Table

from ilf.locker import Locker


def print_lockers_table(lockers: list[Locker], location: str, limit: int = 3 ) -> None:
    """ Prints the lockers in a nice looking table
    :param lockers: the list being an instance of the class Locker
    :param location: the city or the post code to search
    :param limit: the maximum number of lockers to print, default=3
    """
    console = Console()

    table = Table(title=f"InPost Points in [underline]{location.title()}[/underline]", show_lines=True, title_style="bold")
    table.add_column("Point ID", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Address")
    table.add_column("Location Description", style="dim")
    table.add_column("Easy Access?", justify="center")
    table.add_column("Hours", justify="center")
    table.add_column("Map", style="bold cyan")



    for locker in lockers[:limit]:
        maps_link = f"[link={locker.build_map_link}]Google Maps[/link]"

        status_text = f"[green]{locker.status}[/green]" \
            if locker.status == "Operating" else"[red]{locker.status}[/red]"

        easy_access_text = f"[green]{locker.easy_access_zone}[/green]" \
            if locker.easy_access_zone == "Yes" else f"[red]{locker.easy_access_zone}[/red]"

        if "24/7" in locker.opening_hours:
            hours_text = "[bold black on bright_green]24/7[/]"
        else:
            hours_text = locker.opening_hours

        table.add_row(
            locker.name,
            status_text,
            locker.address,
            locker.location_description,
            easy_access_text,
            hours_text,
            maps_link


        )
    console.print(table)


def format_json(lockers: list[Locker], total_found, limit, location) -> str:
    """Prints the lockers as a json string for piping"""
    payload = {
        "metadata": {
            "total_found" : total_found,
            "limit" : limit,
            "location" : location
        },
        "lockers": [
            {
                "name": locker.name,
                "status": locker.status,
                "address": locker.address,
                "location_description": locker.location_description,
                "easy_access_zone": locker.easy_access_zone,
                "opening_hours": locker.opening_hours,
                "maps_link": locker.build_map_link
            }
            for locker in lockers
        ]
    }
    return json.dumps(payload)