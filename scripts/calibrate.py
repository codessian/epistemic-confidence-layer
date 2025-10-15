from __future__ import annotations
import argparse, json, os, random
import numpy as np
from src.ecl.calibration.isotonic import fit_isotonic, save_calibrator as save_iso
from src.ecl.calibration.platt import fit_platt, save_calibrator as save_platt

def toy_dataset(n: int = 200, seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    y_true = np.random.binomial(1, 0.5, size=n)
    # Slight overconfidence to make calibration visible
    y_score = np.clip(np.random.beta(2, 2, size=n), 0.01, 0.99)
    return y_score.tolist(), y_true.tolist()

def main():
    ap = argparse.ArgumentParser(description="Fit and persist a calibrator")
    ap.add_argument("--fit-toy", action="store_true", help="Use toy dataset")
    ap.add_argument("--save", required=True, help="Output path for calibrator.pkl")
    ap.add_argument("--method", choices=["isotonic", "platt"], default="isotonic")
    args = ap.parse_args()

    if args.fit_toy:
        scores, labels = toy_dataset()
    else:
        raise SystemExit("Provide dataset loader or use --fit-toy")

    if args.method == "isotonic":
        cal = fit_isotonic(scores, labels)
        save_iso(cal, args.save)
    else:
        cal = fit_platt(scores, labels)
        save_platt(cal, args.save)
    print(json.dumps({"saved": args.save, "method": args.method}))

if __name__ == "__main__":
    main()