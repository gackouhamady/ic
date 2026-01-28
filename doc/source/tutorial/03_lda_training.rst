LDA training (Hamady GACKOU)
============================

:Author: Hamady GACKOU
:Module: ``ic.lda``
:CLI: ``ic-lda-train`` (legacy) / ``ic lda-train`` (Typer future)

Goal
----

Train an LDA model from exported ``.txt`` files:

- inputs:
  - path to a folder containing texts
  - path to an output folder/file for the trained model (pickle)
- process:
  - recursively find all ``.txt`` files
  - vectorize with ``CountVectorizer``
  - train ``LatentDirichletAllocation``
  - save bundle as pickle

Implementation
--------------

Python module: ``src/ic/lda.py``

Key functions:

- ``train_lda_from_folder(folder: Path, n_topics: int = 10) -> LDAModelBundle``
- ``save_model(bundle: LDAModelBundle, path: Path) -> None``
- ``load_model(path: Path) -> LDAModelBundle``

Robustness note (small corpora)
-------------------------------

When the corpus is very small (e.g. 2 files), fixed parameters like ``min_df=2`` and ``max_df=0.95``
can raise:

- ``ValueError: max_df corresponds to < documents than min_df``

To avoid this, we adapt ``min_df`` for small numbers of documents.

CLI usage (current)
-------------------

.. code-block:: bash

   ic-lda-train --texts data --model-out models/lda.pkl --topics 10

Tests
-----

Unit tests use a temp folder with small text files and check:

- returned model uses expected ``n_topics``
- pickle save/load works

The course also mentions tests of properties (Hypothesis) for generating many inputs automatically. :contentReference[oaicite:10]{index=10}

Logging
-------

Every public function logs its calls (course logging pattern). :contentReference[oaicite:11]{index=11}
