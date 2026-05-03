from typer.testing import CliRunner
from src.ilf import __app_name__, __version__, cli
from src.ilf.cli import app
from src.ilf.locker import Locker

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ['--version'])

    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}" in result.stdout

def test_help():
    result = runner.invoke(app, ['--help'], prog_name=__app_name__)
    assert result.exit_code == 0

    assert f"Usage: {__app_name__}" in result.stdout

    assert "inpost lockers" in result.stdout

def test_find():
    result = runner.invoke(app, ['find', 'Pisary'])
    assert result.exit_code == 0

    assert isinstance(result.stdout, Locker)