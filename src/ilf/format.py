from rich.console import Console
from rich.table import Table

from src.ilf.locker import Locker


def print_lockers_table(lockers: list[Locker], city:str) -> None:
    """ Prints the lockers in a nice looking table"""
    console = Console()

    table = Table(title=f"Closest InPost Lockers in {city.title()}")
    table.add_column("Locker ID", style="blue", no_wrap=True)
    table.add_column("Status", style="cyan")
    table.add_column("Address", style="magenta")
    table.add_column("Location Description", style="yellow")
    table.add_column("Accessible?", style="red")
    table.add_column("Opening hours", style="green")



    for locker in lockers[:3]:
        table.add_row(
            locker.name,
            locker.status,
            locker.address,
            locker.location_description,
            str(locker.easy_access_zone),
            locker.opening_hours,
        )
    console.print(table)