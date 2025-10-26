"""Tjost - Virtual Machine Setup Manager"""

import click
import json
import logging
from importlib.metadata import version
from tjost.config import Config
from tjost.logging_manager import LoggingManager


logger = logging.getLogger(__name__)


@click.group(context_settings={"auto_envvar_prefix": "TJOST"})
@click.pass_context
@click.option(
    "-c",
    "--config",
    "config_path",
    help="Path to configuration file.",
    type=click.Path(),
)
@click.option(
    "-n",
    "--non-interactive",
    default=False,
    help="Run in non-interactive mode and skip user inputs.",
    is_flag=True,
)
@click.option(
    "-v",
    "--verbose",
    "verbosity",
    count=True,
    help="Enable verbose output. Multiple -v options (max 3) increase the verbosity.",
)
def cli(
    ctx: click.Context,
    config_path: click.Path,
    non_interactive: bool,
    verbosity: int,
):
    """Tjost - Easily manage virtual machine setups for test environments."""
    logging_manager = LoggingManager(verbosity=verbosity)
    config = Config(path=config_path)

    journal_enabled: bool = config.get("logging.journal.enabled")
    if journal_enabled:
        journal_log_level: int = config.get("logging.journal.level")
        logging_manager.add_journal_handler(verbosity=journal_log_level)

    ctx.ensure_object(dict)
    ctx.obj["config"] = config


@cli.command("doctor")
@click.pass_context
def cli_doctor(ctx: click.Context):
    """Check the Tjost installation for potential issues."""
    click.echo("Running Tjost doctor... (not implemented)")


@cli.command("version")
@click.pass_context
@click.option(
    "-r",
    "--raw",
    "is_raw",
    is_flag=True,
    help="Show raw version string.",
    default=False,
)
def cli_version(ctx: click.Context, is_raw: bool):
    """Show the version of the Tjost CLI."""
    if ctx.parent.params.get("non_interactive"):
        is_raw = True
    if is_raw:
        click.echo(version("tjost"))
    else:
        click.echo(f"Tjost version {version('tjost')}")


# -----------------------------------------------------------------------------------------------------------------------
# Configuration Subcommands
# -----------------------------------------------------------------------------------------------------------------------
@cli.group("config")
def cli_config():
    """Manage the Tjost configuration."""
    pass


@cli_config.command("show")
@click.pass_context
def config_show(ctx: click.Context):
    """Show current configuration."""
    config = ctx.obj["config"]
    click.echo(json.dumps(config.get(), indent=2))


@cli_config.command("set")
@click.pass_context
@click.argument("key")
@click.argument("value")
def config_set(ctx: click.Context, key: str, value: str):
    """Set a configuration value."""
    config = ctx.obj["config"]
    config.set(key, value)


@cli_config.command("get")
@click.pass_context
@click.argument("key")
def config_get(ctx: click.Context, key: str):
    """Get a configuration value."""
    config = ctx.obj["config"]
    click.echo(config.get(key))
