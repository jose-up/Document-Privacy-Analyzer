"""
Privacy Policy Analyzer

A tool for analyzing privacy policies and terms of service documents
to identify concerning clauses that may impact user privacy and rights.
"""

__version__ = "0.1.0"

from .analyzer import PrivacyAnalyzer, AnalysisResult
from .rules import Rule, RuleMatch, default_rules
from .segmenter import Clause, Span, segment_document

__all__ = [
    "PrivacyAnalyzer",
    "AnalysisResult",
    "Rule",
    "RuleMatch",
    "default_rules",
    "Clause",
    "Span",
    "segment_document",
]