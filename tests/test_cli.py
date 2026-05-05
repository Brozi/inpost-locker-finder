from typer.testing import CliRunner
from unittest.mock import patch
import click
import requests
from rich.panel import Panel


from ilf.cli import app
from ilf.locker import Locker
from ilf import ExitCode, ERROR_MESSAGES



runner = CliRunner()

MOCK_LOCKERS = [
    Locker(
        name="PIS02",
        status="Operating",
        location_247=True,
        opening_hours="24/7",
        easy_access_zone='Yes',
        location_description="",
        address="Kasztanowa 46/2, 32-064 Pisary",
        address_details_city="Pisary",
        address_details_post_code="32-064",
        address_details_street="Kasztanowa",
        address_details_building=''
    )
]

@patch("ilf.cli.fetcher.get_operating_lockers")
def test_find_success(mock_get_operating_lockers):
    """Test find command success"""
    mock_get_operating_lockers.return_value = MOCK_LOCKERS
    result = runner.invoke(app, ['find', 'Pisary', '--json'])
    assert result.exit_code == 0

    stdout = click.unstyle(result.stdout)

    assert "PIS02" in stdout

    assert "Kasztanowa" in stdout

@patch("ilf.cli.fetcher.get_operating_lockers")
def test_cli_network_error(mock_get_operating_lockers):
    mock_get_operating_lockers.side_effect = requests.exceptions.ConnectionError("No DNS")

    result = runner.invoke(app, ['find', 'Pisary'])
    assert result.exit_code == 4

    assert "Network Error" in result.stderr


@patch("ilf.cli.fetcher.get_operating_lockers")
def test_cli_api_error(mock_get_operating_lockers):
    mock_get_operating_lockers.side_effect = requests.exceptions.HTTPError("500 Server Error")

    result = runner.invoke(app, ['find', 'Pisary'])

    assert result.exit_code == 1

    assert "Server Error" in result.stderr

