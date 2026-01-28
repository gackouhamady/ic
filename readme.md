# ic

CLI tools for Newsgroups analysis.

## Usage

1. **Export**: `ic-ng20-export --category comp.graphics --n 20 --out data/`
2. **Train**: `ic-lda-train --texts data/ --model-out models/lda.pkl --topics 5`
3. **Describe**: `ic-lda-describe --model models/lda.pkl --doc data/comp.graphics/0.txt`
4. **Line__Count** : `ic-count-lines --file data/comp.graphics/0.txt`


## Install  setup
### Local install from GitHub (Linux/macOS)

```bash
git clone https://github.com/gackouhamady/ic.git
cd ic
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

### Local install from GitHub (Windows PowerShell)

```powershell
git clone https://github.com/gackouhamady/ic.git
cd ic
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e ".[dev]"
```
