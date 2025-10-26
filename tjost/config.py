"""Tjost configuration module"""

import click
import git
import jsonschema
import jsonschema_default
import logging
import os
import pathlib
import yaml
from tjost.helpers import deep_merge

logger = logging.getLogger(__name__)

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "defaults": {
            "type": "object",
            "properties": {
                "provider": {
                    "type": "string",
                    "enum": [
                        "libvirt",
                        "vmware",
                    ],
                    "default": "libvirt",
                },
                "memory": {
                    "type": "integer",
                    "default": 2048,
                },
                "cpus": {
                    "type": "integer",
                    "default": 2,
                },
            },
        },
        "logging": {
            "type": "object",
            "properties": {
                "journal": {
                    "type": "object",
                    "properties": {
                        "enabled": {
                            "type": "boolean",
                            "default": False,
                        },
                        "level": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 3,
                            "default": 3,
                        },
                    },
                },
            },
        },
    },
}


class Config:
    """Tjost configuration class"""

    data: dict
    path: click.Path
    file_required: bool = False

    def __init__(self, path: click.Path = None):
        """
        Initialize the Config class.

        Automatically searches for a configuration file starting in the working directory.
        If the directory is part of a git repository, a file named `.tjost.yaml` in the
        repository root is used. If the directory is not part of a git repository, the same
        file is looked for in the current working directory.

        If a path is provided and the file does not exist, the method exits with an error.
        Otherwise only the content of the provided file is used.

        :param path: Path to the configuration file.
        """
        self.discover_config_path(path)
        self.load_config()
        logger.debug(f"Configuration loaded: {self.data}")

    def get(self, key: str = None) -> any:
        """
        Get a configuration value by key.

        :param key: The configuration key to retrieve the value from. If None, returns the entire configuration.
        :return: The configuration value.
        """

        def traverse(data: dict, keys: list) -> any:
            """
            Traverse nested dictionary to get the value for a given key path.

            :param data: The dictionary to traverse.
            :param keys: List of keys representing the path to traverse.
            :return: The value at the specified key path or the default value.
            """
            if len(keys) > 1:
                data = data.get(keys[0], {})
                return traverse(data, keys[1:])
            return data.get(keys[0])

        if key is None:
            return self.data
        return traverse(self.data, key.split("."))

    def set(self, key: str, value: any):
        """
        Set a configuration value by key.

        :param key: The configuration key to set the value for.
        :param value: The value to set.
        """
        self.data[key] = value
        try:
            jsonschema.validate(instance=self.data, schema=SCHEMA)
        except jsonschema.ValidationError as e:
            logger.error(f"Configuration data is invalid: {e}")
            raise SystemExit(1)
        self.save_config()

    def discover_config_path(self, path: click.Path = None):
        """
        Discover the configuration file path if the provided path is None. Otherwise return the provided path.

        :param path: Optional path to the configuration file.
        :return: Path to the configuration file.
        """
        if path is not None:
            self.file_required = True
            self.path = pathlib.Path(path)
            return
        try:
            # Test environments usually have a git repository
            logger.debug("Discovering git repository root")
            repo = git.Repo(search_parent_directories=True)
            discover_path = pathlib.Path(f"{repo.working_tree_dir}/.tjost.yaml")
            logger.debug(f"Found git repository root at {repo.working_tree_dir}")
        except git.exc.InvalidGitRepositoryError:
            # If we don't find a git repo, use the current working directory
            logger.debug("Falling back to current working directory")
            discover_path = pathlib.Path(f"{os.getcwd()}/.tjost.yaml")
        self.path = discover_path

    def load_config(self):
        """
        Load configuration from a file.
        """
        logger.info(f"Loading configuration from {self.path}")
        try:
            with click.open_file(self.path, "r") as f:
                data = yaml.full_load(f)
                jsonschema.validate(instance=data, schema=SCHEMA)
        except jsonschema.ValidationError as e:
            logger.error(f"Configuration file {self.path} is invalid: {e}")
            raise SystemExit(1)
        except FileNotFoundError:
            msg = f"Configuration file {self.path} not found"
            if self.file_required:
                logger.error(msg)
                raise SystemExit(1)
            logger.warning(msg)
            data = {}
        default_data = jsonschema_default.create_from(SCHEMA, {})
        self.data = deep_merge(default_data, data)

    def save_config(self):
        """
        Save configuration to a file.
        """
        logger.info(f"Saving configuration to {self.path}")
        with click.open_file(self.path, "w") as f:
            yaml.dump(self.data, f)
