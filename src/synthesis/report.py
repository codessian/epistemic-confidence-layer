from typing import List, Dict

def markdown_summary(claims: List[Dict], consensus: List[Dict]) -> str:
    lines = ["# ECL Report", ""]
    for c in claims:
        text = str(c.get("text", "")).strip()
        claim_hash = str(c.get("hash", ""))
        claim_id = str(c.get("id", ""))
        if not text:
            continue
        lines.append(f"- **Claim**: {text}  (`{claim_hash}`)")
        cc = next((x for x in consensus if x.get("claim_id") == claim_id), None)
        if cc:
            ecs = float(cc.get("ecs", 0.0))
            agree = float(cc.get("agreement_score", 0.0))
            div = float(cc.get("diversity_score", 0.0))
            lines.append(f"  - ECS: {ecs:.2f} (agree={agree:.2f}, div={div:.2f})")
    return "\n".join(lines)
