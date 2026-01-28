Typer CLI (Hamady GACKOU)
=========================

:Author: Hamady GACKOU
:Goal: one executable with subcommands

Why Typer?
----------

The course mentions higher-level CLI libraries:

- argparse
- click
- typer

Typer will replace multiple executables with one CLI and subcommands, with:

- argument type checking
- automatic help
- shell auto-completion support (Typer feature)

This directly matches the project requirement. :contentReference[oaicite:15]{index=15}

Target CLI design
-----------------

One main command:

- ``ic``

Subcommands:

- ``ic ng20-export`` (export NG20)
- ``ic lda-train`` (train model)
- ``ic lda-describe`` (describe document)
- ``ic count-lines`` (count file lines)

Logging integration
-------------------

We add a global option, e.g. ``--log-level``, and call
a central ``configure_logging()`` at startup.

Course logging pattern:

- in each module: ``logger = logging.getLogger(__name__)``
- configure handlers/formatters in the main entrypoint once :contentReference[oaicite:16]{index=16}

Tests
-----

CLI subcommands should have unit tests for:

- argument validation
- outputs (captured stdout)
