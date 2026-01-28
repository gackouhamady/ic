"""Line counting utilities.

This module provides:
- a function to count lines in a text string
- a function to count lines in a file path

All public functions log their calls using the standard `logging` module.
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def count_lines_in_text(text: str) -> int:
    """Count the number of lines in a text.

    A "line" is defined the same way as Python's `str.splitlines()`:
    it splits on universal newlines and does not include the line break
    characters in the resulting list.

    Args:
        text: Input text.

    Returns:
        Number of lines found in `text`.

    Examples:
        >>> count_lines_in_text("")
        0
        >>> count_lines_in_text("hello")
        1
        >>> count_lines_in_text("a\\n")
        1
        >>> count_lines_in_text("a\\nb")
        2
    """
    logger.info("count_lines_in_text called (len=%s)", len(text))
    return len(text.splitlines())


def count_lines_in_file(path: Path) -> int:
    """Count the number of lines in a text file.

    The file is read as UTF-8. If the content contains invalid bytes,
    they are replaced to keep the function robust.

    Args:
        path: Path to the input file.

    Returns:
        Number of lines in the file.

    Raises:
        FileNotFoundError: If the file does not exist.

    Examples:
        This doctest uses a temporary file, as requested:

        >>> import tempfile
        >>> from pathlib import Path
        >>> with tempfile.NamedTemporaryFile() as tmp:
        ...     _ = tmp.write(b"hello\\nworld\\n")
        ...     tmp.flush()
        ...     count_lines_in_file(Path(tmp.name))
        2
    """
    logger.info("count_lines_in_file called (path=%s)", path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    text = path.read_text(encoding="utf-8", errors="replace")
    return count_lines_in_text(text)
