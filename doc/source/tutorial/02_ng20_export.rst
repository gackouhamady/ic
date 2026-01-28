NG20 export (Hamady GACKOU)
===========================

:Author: Hamady GACKOU
:Module: ``ic.ng20``
:CLI: ``ic-ng20-export`` (legacy) / ``ic ng20-export`` (Typer future)

Goal
----

Export the first N documents from a given 20 Newsgroups category:

- input arguments:
  - category C (e.g. ``comp.graphics``)
  - number of documents N
  - output folder D
- process:
  - fetch NG20 texts
  - select the first N documents for category C
  - create folder ``D/C``
  - write files ``i.txt`` (i = document index)

Implementation
--------------

Python module: ``src/ic/ng20.py``

Key function:

- ``export_ng20_category(category: str, n_docs: int, out_dir: Path) -> Path``

Good practices used:

- pathlib paths (recommended in course) :contentReference[oaicite:5]{index=5}
- package installed instead of changing ``sys.path`` (course warning) :contentReference[oaicite:6]{index=6}
- module logger: ``logger = logging.getLogger(__name__)`` (course logging) :contentReference[oaicite:7]{index=7}

CLI usage (current)
-------------------

.. code-block:: bash

   ic-ng20-export --category comp.graphics --n 50 --out data

Expected output:

- folder: ``data/comp.graphics/``
- files: ``0.txt ... 49.txt``

Tests
-----

Unit test example (pytest):

- create temp directory
- run export for N=2
- assert files exist

The course recommends pytest for unit tests. :contentReference[oaicite:8]{index=8}

Logging
-------

All calls should be logged using the standard logging module (course section). :contentReference[oaicite:9]{index=9}
