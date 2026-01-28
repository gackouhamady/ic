Visualization (Hamady GACKOU)
=============================

:Author: Hamady GACKOU
:Project: ic (Packaging Python TP)
:Goal: generate one relevant figure per step (CLI / endpoint)

Overview
--------

This project generates visual outputs to make each step of the pipeline easier to
understand and to provide evidence of execution in the report.

We generate **one image per main step**:

- NG20 export: distribution of document lengths
- LDA training: topic summary (top words per topic) + 2D map (t-SNE) of documents
- LDA describe: topic distribution for a given document
- Line counting: per-line length visualization

All figures are generated with ``matplotlib`` and saved as ``.png``.

Where images are stored
-----------------------

Two locations are used:

1) Runtime outputs (after executing commands)
   - stored next to the produced data/model (recommended for reproducibility)

2) Documentation static files
   - stored under: ``doc/source/_static/figures/``
   - copied from runtime outputs to be embedded in the HTML documentation

Create the static folder if it does not exist:

.. code-block:: bash

   mkdir -p doc/source/_static/figures

NG20 export figure
------------------

After exporting NG20 documents (category C, first N docs), we generate:

- ``doc_lengths.png`` : histogram of document lengths

Command:

.. code-block:: bash

   ic-ng20-export --category comp.graphics --n 50 --out data

Expected outputs:

- texts: ``data/comp.graphics/0.txt ... 49.txt``
- figure: ``data/comp.graphics/doc_lengths.png``

Example inclusion in docs (after copying into ``_static/figures``):

.. image:: /_static/figures/example_doc_lengths.png
   :alt: Histogram of NG20 document lengths

LDA training figures
--------------------

After training the LDA model from a folder of ``.txt`` files, we generate:

- ``lda_topics.png`` : list of topics with their top words (summary figure)
- ``lda_tsne.png`` : 2D visualization (t-SNE) of document-topic vectors

Command:

.. code-block:: bash

   ic-lda-train --texts data --model-out models/lda.pkl --topics 10

Expected outputs:

- model: ``models/lda.pkl``
- figures:
  - ``models/lda_topics.png``
  - ``models/lda_tsne.png``

Example inclusion in docs:

.. image:: /_static/figures/example_lda_topics.png
   :alt: Top words per LDA topic

.. image:: /_static/figures/example_lda_tsne.png
   :alt: t-SNE map of document-topic vectors

Why t-SNE?
~~~~~~~~~~

t-SNE is applied on the **document-topic distributions** produced by LDA.
This gives a compact 2D map of the corpus and helps visually check whether
documents form clusters.

LDA describe figure
-------------------

When describing a document with a trained model, we generate:

- ``<doc>.topics.png`` : bar chart of topic probabilities for the given document

Command:

.. code-block:: bash

   ic-lda-describe --model models/lda.pkl --doc data/comp.graphics/0.txt

Expected output:

- standard output: 3 top topics, each described by 5 words
- figure: ``data/comp.graphics/0.topics.png``

Example inclusion in docs:

.. image:: /_static/figures/example_doc_topics.png
   :alt: Topic distribution for one document

Line count figure
-----------------

For the line counting feature, we generate:

- ``<file>.lines.png`` : bar chart of line lengths (characters)

Command (after Typer integration):

.. code-block:: bash

   ic count-lines data/comp.graphics/0.txt

Expected outputs:

- standard output: number of lines
- figure: ``data/comp.graphics/0.lines.png``

Copy figures into the documentation
-----------------------------------

After running the commands, copy the generated images into the docs folder:

.. code-block:: bash

   cp data/comp.graphics/doc_lengths.png doc/source/_static/figures/example_doc_lengths.png
   cp models/lda_topics.png doc/source/_static/figures/example_lda_topics.png
   cp models/lda_tsne.png doc/source/_static/figures/example_lda_tsne.png
   cp data/comp.graphics/0.topics.png doc/source/_static/figures/example_doc_topics.png

Then rebuild the documentation:

.. code-block:: bash

   sphinx-apidoc -o doc/source/api/ src/ic -f
   sphinx-build -b html doc/source doc/build/html

CI/CD integration
-----------------

In CI/CD, the simplest approach is:

1) run the CLI commands on a small dataset (few docs)
2) copy the generated figures into ``doc/source/_static/figures/``
3) run ``sphinx-build``

This guarantees that the final HTML documentation always contains the figures.

Summary
-------

This visualization layer provides a clean, reproducible way to:

- validate each step of the pipeline
- show results in the final report
- keep visual outputs consistent between local runs and CI/CD builds