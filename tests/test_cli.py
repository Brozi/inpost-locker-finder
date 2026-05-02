from typer.testing import CliRunner
from src.ilf import __app_name__, __version__, cli
from src.ilf.cli import app

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ['--version'])

    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}" in result.stdout