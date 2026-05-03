"""Top level package for Inpost Locker Finder (ilf)"""
__app_name__ = 'inpost-locker-finder'
__version__ = '0.1.0'

from enum import IntEnum


#metadata

class ExitCode(IntEnum):
    SUCCESS = 0
    API_ERROR = 1
    NO_RESULTS = 2
    NETWORK_ERROR = 3
    UNEXPECTED_ERROR = 4
#defining error codes

ERROR_MESSAGES = {
    ExitCode.API_ERROR: "The InPost server returned an unexpected response",
    ExitCode.NO_RESULTS: "No lockers were found with given parameters",
    ExitCode.NETWORK_ERROR: "Could not connect to the internet. Please check your internet connection and try again",
    ExitCode.UNEXPECTED_ERROR: "Unexpected error occured. Please report it on GitHub Issues",
}
#defining error messages for the codes