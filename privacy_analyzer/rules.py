from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple


@dataclass(frozen=True)
class RuleMatch:
    rule_id: str
    category: str
    description: str
    evidence_start: int
    evidence_end: int
    evidence_text: str
    rationale: str

@dataclass(frozen=True)
class Rule:
    rule_id: str
    category: str
    confidence: float
    pattern: re.Pattern
    rationale: str

    def apply(self, clause_text: str, clause_offset: int) -> List[RuleMatch]:
        matches: List[RuleMatch] = []
        for m in self.pattern.finditer(clause_text):
            s = caluse_offset + m.start()
            e = clause_offset + m.end()
            matches.append(
                RuleMatch(
                    rule_id=self.rule_id,
                    category=self.category,
                    confidence=self.confidence,
                    evidence_start=s,
                    evidence_end=e,
                    evidence_text=m.group(0),
                    rationale=self.rationale
                )
            )
            
            
            return matches
        
def default_rules() -> List[Rule]:
    """
    Starter categories algined with your "user-impact" framing.
    Keep partterns conservative to reduce false positives.
    """
    def R(rule_id: str, category: str, conf: float, pat: str, rationale: str) -> Rule:
        return Rule(rule_id, category, conf, re.compile(pat, re.IGNORECASE), rationale)

    return [
        # Data collection / sharing
        R("DATA_SHARE_1", "data_sharing", 0.85,
          r"\bshare\b.*\b(third[- ]party|affiliates?)\b|\bdisclose\b.*\b(third[- ]party|affiliates?)\b",
          "Mentions sharing/disclosing data with third parties or affiliates."),
        R("DATA_SELL_1", "data_sharing", 0.90,
          r"\bsell\b.*\b(personal (data|information)|information)\b",
          "Mentions selling personal data/information."),
        R("TRACK_1", "tracking_telemetry", 0.80,
          r"\b(telemetry|analytics|tracking|usage data|diagnostic data)\b",
          "Mentions telemetry/analytics/tracking or diagnostic/usage data."),

        # Account / access / device control
        R("REMOTE_DISABLE_1", "device_control", 0.90,
          r"\b(disable|suspend|terminate|deactivate)\b.*\b(account|service|device)\b",
          "Mentions disabling/suspending/terminating an account/service/device."),
        R("REMOTE_UPDATE_1", "device_control", 0.75,
          r"\b(remote|automatic)\b.*\b(update|patch|modify)\b",
          "Mentions remote or automatic updates/modifications."),

        # Modifications / anti-circumvention language
        R("MOD_RESTRICT_1", "modification_restrictions", 0.85,
          r"\b(jailbreak|circumvent|bypass|reverse engineer|decompile|tamper)\b",
          "Mentions restrictions on modification, circumvention, or reverse engineering."),

        # Arbitration / waiver / legal posture (consumer-impactful)
        R("ARBITRATION_1", "legal_terms", 0.90,
          r"\b(binding )?arbitration\b|\bclass action\b.*\bwaive\b",
          "Mentions arbitration or class-action waiver language."),
        R("CHOICE_LAW_1", "legal_terms", 0.70,
          r"\bgoverned by\b.*\blaws? of\b|\bjurisdiction\b",
          "Mentions governing law or jurisdiction."),

        # Data retention / deletion
        R("RETENTION_1", "data_retention", 0.75,
          r"\b(retain|retention)\b.*\b(data|information)\b|\bstore\b.*\bfor\b.*\b(days|months|years)\b",
          "Mentions data retention/storage duration."),
        R("DELETE_LIMIT_1", "data_retention", 0.70,
          r"\b(may|can)\b.*\bnot\b.*\b(delete|erasure|remove)\b|\bdeletion\b.*\bnot\b.*\bguaranteed\b",
          "Mentions limits on deletion/erasure guarantees."),
    ]