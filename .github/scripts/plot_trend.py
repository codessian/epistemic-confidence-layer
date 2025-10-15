import argparse, csv
import matplotlib.pyplot as plt
from datetime import datetime

ap = argparse.ArgumentParser()
ap.add_argument("--csv", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()

dates, before, after = [], [], []
with open(args.csv) as f:
    r = csv.DictReader(f)
    for row in r:
        dates.append(datetime.fromisoformat(row["date"]))
        before.append(float(row["ece_before"]))
        after.append(float(row["ece_after"]))

plt.figure(figsize=(8,4.5))
plt.plot(dates, before, marker="o", label="ECE (before)")
plt.plot(dates, after, marker="o", label="ECE (after)")
plt.xlabel("Date"); plt.ylabel("ECE"); plt.title("Nightly ECE Trend")
plt.legend(); plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(args.out, dpi=160)
print("Wrote", args.out)