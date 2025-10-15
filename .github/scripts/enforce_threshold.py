import json, sys, argparse, pathlib

def main():
    p = pathlib.Path("benchmarks/results/metrics.json")
    if not p.exists():
        print("metrics.json not found; failing to avoid silent regressions.")
        sys.exit(1)
    m = json.loads(p.read_text())
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_regress", type=float, default=0.02,
                        help="allowable ECE regression (+delta) before failing")
    args = parser.parse_args()
    before = m.get("ece_before"); after = m.get("ece_after")
    if before is None or after is None:
        print("ECE values missing; failing to avoid silent regressions.")
        sys.exit(1)
    delta = after - before
    print(f"ECE delta: {delta:+.3f} (limit {args.max_regress:+.3f})")
    if delta > args.max_regress:
        print("ECE regression beyond threshold — failing CI.")
        sys.exit(1)
    print("ECE within threshold — OK.")

if __name__ == "__main__":
    main()