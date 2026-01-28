from pathlib import Path

import pytest

from ic.linecount import count_lines_in_file, count_lines_in_text


def test_count_lines_in_text_basic() -> None:
    assert count_lines_in_text("") == 0
    assert count_lines_in_text("hello") == 1
    assert count_lines_in_text("a\nb") == 2


def test_count_lines_in_file(tmp_path: Path) -> None:
    p = tmp_path / "x.txt"
    p.write_text("a\nb\nc\n", encoding="utf-8")
    assert count_lines_in_file(p) == 3


def test_count_lines_in_file_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        count_lines_in_file(tmp_path / "missing.txt")
