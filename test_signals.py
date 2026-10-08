from analysis.evidence import collect_evidence
from analysis.signals import (
    calculate_signals,
    calculate_confidence,
)


evidence = collect_evidence(
    "graphene water purification"
)

signals = calculate_signals(evidence)

confidence = calculate_confidence(
    evidence
)


print("\n" + "=" * 50)
print("GAPFINDER SIGNALS")
print("=" * 50)

for name, score in signals.items():
    print(f"{name.capitalize():12} {score}/100")

print("\nEvidence confidence:")
print(f"{confidence}/100")