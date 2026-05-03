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
        desc_1 = locker.location_description
        desc_2 = locker.location_description_1
        desc_3 = locker.location_description_2

        raw_desc = [desc_1, desc_2, desc_3]

        cleaned_desc = ", ".join(filter(None, raw_desc))

        if not locker.opening_hours:
            if locker.location_247:
                locker.opening_hours = "24/7"
            locker.opening_hours = 'No data'


        table.add_row(
            locker.name,
            locker.status,
            f"{locker.address_line1}, {locker.address_line2}",
            cleaned_desc,
            str(locker.easy_access_zone),
            locker.opening_hours,
        )
    console.print(table)