from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Optional
import json

from .segmenter import segment_document, Clause
from .rules import Rule, RuleMatch, default_rules


@dataclass
class AnalysisResult:
    """Complete analysis result for a document."""
    text: str
    clauses: List[Clause]
    matches: List[RuleMatch]
    category_summary: Dict[str, int]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "text": self.text,
            "clauses": [
                {
                    "id": c.id,
                    "span": {"start": c.span.start, "end": c.span.end},
                    "text": c.text
                }
                for c in self.clauses
            ],
            "matches": [
                {
                    "rule_id": m.rule_id,
                    "category": m.category,
                    "description": m.description,
                    "evidence_start": m.evidence_start,
                    "evidence_end": m.evidence_end,
                    "evidence_text": m.evidence_text,
                    "rationale": m.rationale,
                    "confidence": m.confidence
                }
                for m in self.matches
            ],
            "category_summary": self.category_summary
        }
    
    def to_json(self, indent: Optional[int] = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)


class PrivacyAnalyzer:
    """Main analyzer class for privacy policy documents."""
    
    def __init__(self, rules: Optional[List[Rule]] = None):
        """
        Initialize the analyzer with a set of rules.
        
        Args:
            rules: List of Rule objects. If None, uses default_rules().
        """
        self.rules = rules if rules is not None else default_rules()
    
    def analyze(self, text: str, max_clause_chars: int = 1200) -> AnalysisResult:
        """
        Analyze a privacy policy document.
        
        Args:
            text: The document text to analyze
            max_clause_chars: Maximum characters per clause for segmentation
            
        Returns:
            AnalysisResult containing clauses, matches, and summary
        """
        # Step 1: Segment the document into clauses
        clauses = segment_document(text, max_clause_chars=max_clause_chars)
        
        # Step 2: Apply rules to each clause
        all_matches: List[RuleMatch] = []
        
        for clause in clauses:
            for rule in self.rules:
                matches = rule.apply(clause.text, clause.span.start)
                all_matches.extend(matches)
        
        # Step 3: Generate category summary
        category_summary: Dict[str, int] = {}
        for match in all_matches:
            category_summary[match.category] = category_summary.get(match.category, 0) + 1
        
        return AnalysisResult(
            text=text,
            clauses=clauses,
            matches=all_matches,
            category_summary=category_summary
        )
    
    def get_matches_by_category(self, result: AnalysisResult) -> Dict[str, List[RuleMatch]]:
        """
        Group matches by category.
        
        Args:
            result: AnalysisResult from analyze()
            
        Returns:
            Dictionary mapping category names to lists of matches
        """
        categorized: Dict[str, List[RuleMatch]] = {}
        for match in result.matches:
            if match.category not in categorized:
                categorized[match.category] = []
            categorized[match.category].append(match)
        return categorized
    
    def get_high_confidence_matches(
        self, 
        result: AnalysisResult, 
        threshold: float = 0.8
    ) -> List[RuleMatch]:
        """
        Filter matches by confidence threshold.
        
        Args:
            result: AnalysisResult from analyze()
            threshold: Minimum confidence level (0.0 to 1.0)
            
        Returns:
            List of matches with confidence >= threshold
        """
        return [m for m in result.matches if m.confidence >= threshold]
    
    def generate_summary_report(self, result: AnalysisResult) -> str:
        """
        Generate a human-readable summary report.
        
        Args:
            result: AnalysisResult from analyze()
            
        Returns:
            Formatted string report
        """
        lines = []
        lines.append("=" * 60)
        lines.append("PRIVACY POLICY ANALYSIS REPORT")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"Total clauses analyzed: {len(result.clauses)}")
        lines.append(f"Total issues found: {len(result.matches)}")
        lines.append("")
        lines.append("ISSUES BY CATEGORY:")
        lines.append("-" * 60)
        
        for category, count in sorted(result.category_summary.items()):
            lines.append(f"  {category}: {count} issue(s)")
        
        lines.append("")
        lines.append("DETAILED FINDINGS:")
        lines.append("-" * 60)
        
        categorized = self.get_matches_by_category(result)
        for category, matches in sorted(categorized.items()):
            lines.append(f"\n[{category.upper()}]")
            for i, match in enumerate(matches, 1):
                lines.append(f"  {i}. {match.rationale}")
                lines.append(f"     Evidence: \"{match.evidence_text}\"")
                lines.append(f"     Confidence: {match.confidence:.0%}")
                lines.append(f"     Location: characters {match.evidence_start}-{match.evidence_end}")
                lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)