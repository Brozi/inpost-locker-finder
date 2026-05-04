from typer.testing import CliRunner

from src.ilf import __app_name__, __version__, cli
from src.ilf.cli import app
from src.ilf.locker import Locker

from unittest.mock import patch

runner = CliRunner()

MOCK_LOCKERS = [
    Locker(
        name="PIS02",
        status="Operating",
        location_247=True,
        opening_hours="24/7",
        easy_access_zone=True,
        location_description="",
        address="Kasztanowa 46/2, 32-064 Pisary",
        address_details_city="Pisary",
        address_details_post_code="32-064",
        address_details_street="Kasztanowa",
        address_details_building=''
    )
]

def test_version():
    """Test that the version command actually works"""
    result = runner.invoke(app, ['--version'])

    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}" in result.stdout

def test_help():
    """Test help command"""
    result = runner.invoke(app, ['--help'], prog_name=__app_name__)
    assert result.exit_code == 0

    assert f"Usage: {__app_name__}" in result.stdout

    assert "inpost lockers" in result.stdout

@patch("src.ilf.cli.fetcher.get_operating_lockers")
def test_find_success(mock_get_operating_lockers):
    """Test find command success"""
    mock_get_operating_lockers.return_value = MOCK_LOCKERS
    result = runner.invoke(app, ['find', 'Pisary'])
    assert result.exit_code == 0

    assert "PIS02" in result.stdout

    assert "Kasztanowa" in result.stdout
