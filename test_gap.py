from analysis.evidence import collect_evidence
from analysis.signals import (
    calculate_signals,
    calculate_trend_momentum,
    calculate_confidence
)
from analysis.gap_detector import (
    detect_gap,
    calculate_opportunity_score,
    classify_opportunity,
)
from analysis.report import build_report


query = "graphene water purification"


evidence = collect_evidence(query)

signals = calculate_signals(evidence)
trend_momentum = calculate_trend_momentum(
    evidence["demand"]
)
gap = detect_gap(
    signals,
    trend_momentum,
)
opportunity_score = calculate_opportunity_score(
    signals,
    gap,
)

opportunity = classify_opportunity(
    opportunity_score,
)
confidence = calculate_confidence(evidence)
report = build_report(
    query,
    evidence,
    signals,
    gap,
    confidence,
)


print("\n" + "=" * 60)
print("GAPFINDER REPORT")
print("=" * 60)

print("\nTechnology:")
print(query)

print("\nOpportunity Score:")
print(f"{opportunity_score}/100")

print("Classification:")
print(opportunity)

print("\nSignals")
print("-" * 30)

for name, score in signals.items():
    print(f"{name.capitalize():12} {score}/100")

print("\nGap Analysis")
print("-" * 30)

print(
    "Technology strength:",
    gap["technology_strength"]
)

print(
    "Commercial supply:",
    gap["supply_strength"]
)

print(
    "Gap score:",
    gap["gap_score"]
)
print(
    "Trend momentum:",
    gap["trend_momentum"]
)

print(
    "Emerging-gap bonus:",
    gap["emerging_gap_bonus"]
)

print(
    "Gap classification:",
    gap["category"]
)

print("\nEvidence")
print("-" * 30)

for name, value in report["evidence"].items():
    print(f"{name}: {value}")

print("\nFindings")
print("-" * 30)

for finding in report["findings"]:
    print(f"• {finding}")

print("\nConclusion")
print("-" * 30)

print(report["conclusion"])