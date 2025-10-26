"""Tjost smoke tests"""

from click.testing import CliRunner
from tjost.main import cli


def test_cli_version():
    """Test the 'tjost version' command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "Tjost version" in result.output


def test_cli_version_raw():
    """Test the 'tjost version --raw' command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["version", "--raw"])
    assert result.exit_code == 0
    assert "Tjost version" not in result.output  # Raw output should not have prefix


def test_cli_doctor():
    """Test the 'tjost doctor' command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["doctor"])
    assert result.exit_code == 0
    assert "Running Tjost doctor" in result.output


def test_cli_config_show():
    """Test the 'tjost config show' command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["config", "show"])
    assert result.exit_code == 0
    assert "{" in result.output  # Basic check for JSON output


def test_cli_config_set_and_get():
    """Test the 'tjost config set' and 'tjost config get' commands."""
    runner = CliRunner()
    set_result = runner.invoke(cli, ["config", "set", "test_key", "test_value"])
    assert set_result.exit_code == 0

    get_result = runner.invoke(cli, ["config", "get", "test_key"])
    assert get_result.exit_code == 0
    assert "test_value" in get_result.output


def test_cli_explicit_config_file_missing():
    """Test behavior when an explicit config file is missing."""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["--config", "/non_existent_config.yaml", "config", "show"]
    )
    assert result.exit_code != 0
    assert "not found" in result.output
