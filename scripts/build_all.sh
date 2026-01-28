#!/usr/bin/env bash
set -euo pipefail

python -m pip install -e ".[dev]"

flake8 src tests
pytest -q

mkdir -p doc/source/api
sphinx-apidoc -o doc/source/api/ src/ic -f

# Generate figures
ic-ng20-export --category comp.graphics --n 10 --out data
ic-lda-train --texts data --model-out models/lda.pkl --topics 10
ic-lda-describe --model models/lda.pkl --doc data/comp.graphics/0.txt

# Copy figures into Sphinx static folder
mkdir -p doc/source/_static/figures
cp data/comp.graphics/doc_lengths.png \
  doc/source/_static/figures/example_doc_lengths.png
cp models/lda_topics.png \
  doc/source/_static/figures/example_lda_topics.png
cp models/lda_tsne.png \
  doc/source/_static/figures/example_lda_tsne.png
cp data/comp.graphics/0.topics.png \
  doc/source/_static/figures/example_doc_topics.png

sphinx-build -b html doc/source doc/build/html
