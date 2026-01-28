Setup (Hamady GACKOU)
=====================

:Author: Hamady GACKOU
:Project: ic (Packaging Python TP)
:Last update: |today|

Objectives
----------

This tutorial documents, step by step, the whole practical work:

- create an installable Python package (recommended ``src/`` layout)
- provide a CLI to export NG20 text, train LDA, describe documents, count lines
- write unit tests (pytest) + property-based tests (Hypothesis)
- document the API with Sphinx + ``sphinx-apidoc``
- add logging to all calls
- migrate to a single Typer CLI (subcommands)
- expose an HTTP API with FastAPI (OpenAPI)
- add a visualization feature and include it in this documentation

This follows the recommendations of the course support (structure, tests, docs, logging, CLI). :contentReference[oaicite:1]{index=1}

Project structure
-----------------

Recommended structure (root directory):

- ``pyproject.toml`` (build system)
- ``setup.cfg`` (metadata, dependencies, entrypoints)
- ``requirements.txt`` (pinned versions for an application)
- ``src/ic`` (package code)
- ``tests`` (pytest tests)
- ``doc`` (Sphinx documentation)

The course explicitly recommends this layout. :contentReference[oaicite:2]{index=2}

Installation (development mode)
-------------------------------

Create and activate an environment, then install editable:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
   python -m pip install -U pip
   python -m pip install -e ".[dev]"

The course shows ``pip install -e ".[dev]"`` for development. :contentReference[oaicite:3]{index=3}

Quality checks
--------------

Run style + tests:

.. code-block:: bash

   flake8 src tests
   pytest -q

Documentation build
-------------------

Generate API docs + build HTML:

.. code-block:: bash

   sphinx-apidoc -o doc/source/api/ src/ic -f
   sphinx-build -b html doc/source doc/build/html

The course recommends Sphinx for general documentation and ``sphinx-apidoc`` for API docs. :contentReference[oaicite:4]{index=4}
