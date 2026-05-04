from rich.console import Console
from rich.table import Table

from src.ilf.locker import Locker


def print_lockers_table(lockers: list[Locker], city:str, limit: int = 3 ) -> None:
    """ Prints the lockers in a nice looking table
    :param lockers: the list being an instance of the class Locker
    :param city: the name of the city
    :param limit: the maximum number of lockers to print, default=3
    """
    console = Console()

    table = Table(title=f"Closest InPost Lockers in {city.title()}")
    table.add_column("Locker ID", style="blue", no_wrap=True)
    table.add_column("Status", style="cyan")
    table.add_column("Address", style="magenta")
    table.add_column("Location Description", style="yellow")
    table.add_column("Accessible?", style="red")
    table.add_column("Opening hours", style="green")



    for locker in lockers[:limit]:
        table.add_row(
            locker.name,
            locker.status,
            locker.address,
            locker.location_description,
            str(locker.easy_access_zone),
            locker.opening_hours,
        )
    console.print(table)