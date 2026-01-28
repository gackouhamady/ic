from hypothesis import given
from hypothesis import strategies as st

from ic.linecount import count_lines_in_text


@given(st.text())
def test_count_lines_matches_splitlines(text: str) -> None:
    assert count_lines_in_text(text) == len(text.splitlines())
