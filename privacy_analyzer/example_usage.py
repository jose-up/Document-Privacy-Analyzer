#!/usr/bin/env python3
"""
Example usage of the Privacy Analyzer library.
"""

from privacy_analyzer import PrivacyAnalyzer

# Example privacy policy text
SAMPLE_POLICY = """
PRIVACY POLICY

1. DATA COLLECTION AND SHARING

We collect personal information including your name, email address, and usage data.
We may share your personal data with third-party affiliates for marketing purposes.
We reserve the right to sell your personal information to partners.

2. TRACKING AND ANALYTICS

We use telemetry and analytics to track your usage patterns and diagnostic data.
This information helps us improve our services.

3. DEVICE CONTROL

We may remotely disable your account or device if we suspect unauthorized use.
Automatic updates may be applied to your device without prior notice.

4. MODIFICATION RESTRICTIONS

You may not jailbreak, reverse engineer, or circumvent our security measures.
Any attempt to tamper with our software is strictly prohibited.

5. LEGAL TERMS

All disputes will be resolved through binding arbitration. You waive your right
to participate in class action lawsuits. This agreement is governed by the laws
of California and all disputes must be resolved in California courts.

6. DATA RETENTION

We retain your personal data for up to 10 years after account closure.
We may not be able to delete all copies of your information from our backup systems.
"""


def main():
    # Create analyzer instance
    analyzer = PrivacyAnalyzer()
    
    # Analyze the document
    print("Analyzing privacy policy...\n")
    result = analyzer.analyze(SAMPLE_POLICY)
    
    # Print summary statistics
    print(f"Found {len(result.matches)} issues across {len(result.clauses)} clauses\n")
    
    # Print category summary
    print("Issues by category:")
    for category, count in sorted(result.category_summary.items()):
        print(f"  - {category}: {count}")
    
    print("\n" + "=" * 70 + "\n")
    
    # Print detailed findings grouped by category
    categorized = analyzer.get_matches_by_category(result)
    
    for category, matches in sorted(categorized.items()):
        print(f"\n[{category.upper()}]")
        for match in matches:
            print(f"  • {match.rationale}")
            print(f"    Evidence: \"{match.evidence_text}\"")
            print(f"    Confidence: {match.confidence:.0%}\n")
    
    print("=" * 70 + "\n")
    
    # Show only high-confidence matches (>= 85%)
    high_conf = analyzer.get_high_confidence_matches(result, threshold=0.85)
    print(f"High-confidence issues (≥85%): {len(high_conf)}")
    for match in high_conf:
        print(f"  • [{match.category}] {match.evidence_text}")
    
    print("\n" + "=" * 70 + "\n")
    
    # Generate full report
    print("FULL REPORT:")
    print(analyzer.generate_summary_report(result))
    
    # Save to JSON
    print("\nSaving to output.json...")
    with open("output.json", "w") as f:
        f.write(result.to_json())
    print("Done!")


if __name__ == "__main__":
    main()