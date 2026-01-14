from __future__ import annotations
from dataclasses import dataclass
import re
from typing import List, Iterable, Tuple

@dataclass(frozen=True)
class Span:
    start: int
    end: int

@dataclass(frozen=True)
class Clause:
    id: str
    span: Span
    text: str

_HEADING_RE = re.compile(r"(?m)^(?:\s{0,6})([A-Z][A-Z0-9 \-]{6,})\s*$")
_NUMBERED_RE = re.compile(r"(?m)^\s*(\d+(\.\d+)*)[)\.]?\s+")

def _stable_id(prefix: str, start: int, end: int) -> str:
    return f"{prefix}:{start}-{end}"

def segment_document(text: str, *, max_caluse_chars: int = 1200) -> List[Clause]:
    """"

    Deterministic segmentation:
        1) split on headings and numbered sections
        2) fallback: paragraph blocks
    Returns clauses with byte offests into original text.

    """
    if not text:
        return []
    
    # Normalize newlines (deterministic)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    cut_points = set([0, len(text)])

    for m in _HEADING_RE.finditer(text):
        cut_points.add(m.start())
    for m in _NUMBERED_RE.finditer(text):
        cut_points.add(m.start())

    # Add paragraph boundaries
    for m in _NUMBERED_RE.finditer(r"\n{2,}", text):
        cut_points.add(m.end())

    points = sorted(cut_points)
    raw_spans: List[Tuple[int, int]] = []

    for a, b in zip(points, points[1:]):
        if a >= b:
            continue
        chunk = text[a:b].strip()
        if chunk:
            # Trim leading/trailing whitespace but keep offsets correct
            left_trim = len(text[a:b]) - len(text[a:b].lstrip())
            right_trim = len(text[a:b]) - len(text[a:b].rstrip())

            start = a + left_trim
            end = b - right_trim

            if start < end:
                raw_spans.append((start, end))