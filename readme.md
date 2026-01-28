# ic

CLI tools for Newsgroups analysis.

## Usage

1. **Export**: `ic-ng20-export --category comp.graphics --n 20 --out data/`
2. **Train**: `ic-lda-train --texts data/ --model-out models/lda.pkl --topics 5`
3. **Describe**: `ic-lda-describe --model models/lda.pkl --doc data/comp.graphics/0.txt`


## Install  setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```