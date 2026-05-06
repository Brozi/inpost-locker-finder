"""Top level package for Inpost Locker Finder (ilf)"""
__app_name__ = 'inpost-locker-finder'

from importlib.metadata import version, PackageNotFoundError

from enum import IntEnum

try:
    __version__ = version("inpost-locker-finder")
except PackageNotFoundError:
    __version__ = "dev (not installed)"


#metadata

class ExitCode(IntEnum):
    SUCCESS = 0
    API_ERROR = 1
    NO_RESULTS = 2
    NO_RESULTS_FROM_FILTERING = 3
    NETWORK_ERROR = 4
    UNEXPECTED_ERROR = 5
    HINT = 6
    NO_ARG = 7
#defining error codes

ERROR_MESSAGES = {
    ExitCode.API_ERROR: f"[bold red]The InPost server returned an unexpected response[/bold red]",
    ExitCode.NO_RESULTS: f"[bold red]No points were found within given parameters[/bold red]",
    ExitCode.NO_RESULTS_FROM_FILTERING: f"[bold yellow]Found points, but none matched your filters[/bold yellow]",
    ExitCode.HINT: "[bold yellow]Hint: When searching without a city, partial postal codes are not supported. Make sure you entered a full postal code.[/bold yellow]",
    ExitCode.NETWORK_ERROR: f"[bold red]Could not connect to the internet. Please check your internet connection and try again[/bold red]",
    ExitCode.UNEXPECTED_ERROR: f"[bold red]Unexpected error occured. Please report it on GitHub Issues[/bold red]",
    ExitCode.NO_ARG: f"[bold red] No argument provided - provide at least one[/bold red]"
}
#defining error messages for the codes