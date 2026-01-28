Line count, doctest, and Hypothesis (Hamady GACKOU)
===================================================

:Author: Hamady GACKOU
:Module: ``ic.linecount``
:CLI: (legacy) / ``ic count-lines`` (Typer future)

Goal
----

Create a command that:

- takes a file path as argument
- counts number of lines
- prints the number to standard output

Required functions
------------------

1) A function that takes a string and returns its number of lines:

- ``count_lines_in_text(text: str) -> int``

2) A function that takes a file path and returns its number of lines:

- ``count_lines_in_file(path: Path) -> int``

Doctest
-------

A doctest is defined in the docstring and uses a temporary file,
as requested in the statement:

.. code-block:: python

   import tempfile

   with tempfile.NamedTemporaryFile() as tmp:
       print(tmp.name)
       tmp.write(b"hello")

The course explains doctests and shows how examples in docstrings
can be checked automatically. :contentReference[oaicite:12]{index=12}

Running doctests with pytest
----------------------------

We enable doctests via ``pytest.ini``:

.. code-block:: ini

   [pytest]
   addopts = --doctest-modules

Then:

.. code-block:: bash

   pytest -q

Hypothesis (property-based testing)
-----------------------------------

Property: line counting must match ``splitlines`` behavior:

.. code-block:: python

   from hypothesis import given
   from hypothesis import strategies as st

   @given(st.text())
   def test_count_lines_matches_splitlines(text: str) -> None:
       assert count_lines_in_text(text) == len(text.splitlines())

The course recommends property-based tests and cites Hypothesis as an example tool. :contentReference[oaicite:13]{index=13}

Logging
-------

All calls are logged via the module-level logger. :contentReference[oaicite:14]{index=14}
