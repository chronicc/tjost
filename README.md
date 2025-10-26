Tjost
=====

Easily manage virtual machine setups for test environments.

Getting started
---------------

1. Install tjost with `pip install tjost`.
2. Run `tjost` and use the help messages to navigate the tool.

Usage
-----

### Shell Completion

To enable shell completion run one of the following commands.

```shell
# Bash
eval "$(_TJOST_COMPLETE=bash_source tjost)"

# Zsh
eval "$(_TJOST_COMPLETE=zsh_source tjost)"

# Fish
_TJOST_COMPLETE=fish_source tjost | source
```

### Journald logging

To enable journald logging, install the optional dependencies for systemd.

```shell
# Use the package that is provided by your os manufacturer
sudo apt install libsystemd-dev

# Install the systemd dependencies for tjost
pip install tjost[systemd]
```

Configure journald logging in the configuration.

```yaml
# .tjost.yaml

logging:
  journal:
    enabled: true
```

Development
-----------

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Run `uv sync` to install the python dependencies.
3. Run `source .venv/bin/activate` to activate the python virtual environment.
