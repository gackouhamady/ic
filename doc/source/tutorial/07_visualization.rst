Visualization (Hamady GACKOU)
=============================

:Author: Hamady GACKOU
:Goal: graphical display of document/topics

Goal
----

Provide a feature to display a document or topic results graphically.

A typical approach:
-------------------

1) Generate a figure (PNG) using matplotlib:

- e.g. top words per topic as a bar chart
- or a table-like plot of topic/keywords

2) Save the image under:

- ``doc/source/_static/figures/``

3) Include it in the documentation:

.. code-block:: rst

   .. image:: /_static/figures/topic_words.png
      :alt: Top words per topic

Build integration
-----------------

A simple approach is to generate figures before ``sphinx-build`` in CI/CD,
so the final HTML includes them.

Next step
---------

We will add a script (or a function) that produces the figure from:

- a trained model pickle
- optionally a document to describe

Then include the generated images here.
