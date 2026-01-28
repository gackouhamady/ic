"""CLI Entry Points."""
import argparse
from pathlib import Path
from ic.ng20 import export_ng20_category
from ic.lda import train_lda_from_folder, save_model, load_model, describe_document

def ng20_export_app():
    parser = argparse.ArgumentParser(description="Export NG20 category to text files.")
    parser.add_argument("--category", required=True, help="Category name (e.g. comp.graphics)")
    parser.add_argument("--n", type=int, required=True, help="Number of docs")
    parser.add_argument("--out", required=True, help="Output folder")
    args = parser.parse_args()
    
    path = export_ng20_category(args.category, args.n, Path(args.out))
    print(f"Exported to {path}")

def lda_train_app():
    parser = argparse.ArgumentParser(description="Train LDA model from folder.")
    parser.add_argument("--texts", required=True, help="Input folder with .txt files")
    parser.add_argument("--model-out", required=True, help="Output pickle path")
    parser.add_argument("--topics", type=int, default=10, help="Number of topics")
    args = parser.parse_args()
    
    bundle = train_lda_from_folder(Path(args.texts), args.topics)
    save_model(bundle, Path(args.model_out))
    print(f"Model saved to {args.model_out}")

def lda_describe_app():
    parser = argparse.ArgumentParser(description="Describe document using trained LDA.")
    parser.add_argument("--model", required=True, help="Path to model pickle")
    parser.add_argument("--doc", required=True, help="Path to document .txt")
    args = parser.parse_args()
    
    bundle = load_model(Path(args.model))
    text = Path(args.doc).read_text(encoding="utf-8", errors="replace")
    desc = describe_document(bundle, text)
    
    print(f"--- Document: {args.doc} ---")
    for topic_id, words in desc:
        print(f"Topic {topic_id}: {', '.join(words)}")
