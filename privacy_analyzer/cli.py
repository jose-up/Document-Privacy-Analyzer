#!/usr/bin/env python3
"""
Command-line interface for the Privacy Policy Analyzer.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from typing import Optional

from .analyzer import PrivacyAnalyzer


def read_file(filepath: str) -> str:
    """Read text from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        sys.exit(1)


def write_file(filepath: str, content: str) -> None:
    """Write content to a file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing to file {filepath}: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze privacy policies and terms of service documents for concerning clauses.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a document and print summary to console
  privacy-analyzer policy.txt
  
  # Save detailed JSON output
  privacy-analyzer policy.txt --json output.json
  
  # Save human-readable report
  privacy-analyzer policy.txt --report report.txt
  
  # Filter by confidence threshold
  privacy-analyzer policy.txt --min-confidence 0.85
  
  # Show only specific categories
  privacy-analyzer policy.txt --categories data_sharing device_control
        """
    )
    
    parser.add_argument(
        'input',
        help='Path to the privacy policy or terms of service document'
    )
    
    parser.add_argument(
        '--json',
        metavar='FILE',
        help='Save detailed analysis as JSON to FILE'
    )
    
    parser.add_argument(
        '--report',
        metavar='FILE',
        help='Save human-readable report to FILE'
    )
    
    parser.add_argument(
        '--min-confidence',
        type=float,
        default=0.0,
        metavar='THRESHOLD',
        help='Only show matches with confidence >= THRESHOLD (0.0-1.0, default: 0.0)'
    )
    
    parser.add_argument(
        '--categories',
        nargs='+',
        metavar='CATEGORY',
        help='Only show matches from specified categories'
    )
    
    parser.add_argument(
        '--max-clause-chars',
        type=int,
        default=1200,
        metavar='N',
        help='Maximum characters per clause (default: 1200)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress console output (useful when saving to files)'
    )
    
    args = parser.parse_args()
    
    # Validate confidence threshold
    if not 0.0 <= args.min_confidence <= 1.0:
        print("Error: --min-confidence must be between 0.0 and 1.0", file=sys.stderr)
        return 1
    
    # Read input document
    if not args.quiet:
        print(f"Reading document: {args.input}")
    
    text = read_file(args.input)
    
    # Analyze the document
    if not args.quiet:
        print("Analyzing document...")
    
    analyzer = PrivacyAnalyzer()
    result = analyzer.analyze(text, max_clause_chars=args.max_clause_chars)
    
    # Filter by confidence if requested
    filtered_matches = [
        m for m in result.matches 
        if m.confidence >= args.min_confidence
    ]
    
    # Filter by category if requested
    if args.categories:
        filtered_matches = [
            m for m in filtered_matches 
            if m.category in args.categories
        ]
    
    # Update result with filtered matches
    if args.min_confidence > 0.0 or args.categories:
        # Recalculate category summary for filtered matches
        category_summary = {}
        for match in filtered_matches:
            category_summary[match.category] = category_summary.get(match.category, 0) + 1
        
        result.matches = filtered_matches
        result.category_summary = category_summary
    
    # Save JSON if requested
    if args.json:
        if not args.quiet:
            print(f"Saving JSON to: {args.json}")
        write_file(args.json, result.to_json())
    
    # Generate and save/print report
    report = analyzer.generate_summary_report(result)
    
    if args.report:
        if not args.quiet:
            print(f"Saving report to: {args.report}")
        write_file(args.report, report)
    
    if not args.quiet:
        print("\n" + report)
    
    # Exit with status code based on findings
    if result.matches:
        return 0  # Found issues (successful analysis)
    else:
        if not args.quiet:
            print("\nNo concerning clauses found.")
        return 0


if __name__ == '__main__':
    sys.exit(main())