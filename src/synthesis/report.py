from typing import List, Dict

def markdown_summary(claims: List[Dict], consensus: List[Dict]) -> str:
    lines = ["# ECL Report", ""]
    for c in claims:
        lines.append(f"- **Claim**: {c['text']}  (`{c['hash']}`)")
        cc = next((x for x in consensus if x["claim_id"] == c["id"]), None)
        if cc:
            lines.append(f"  - ECS: {cc['ecs']:.2f} (agree={cc['agreement_score']:.2f}, div={cc['diversity_score']:.2f})")
    return "\n".join(lines)