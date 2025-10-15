import argparse, csv, json, os, datetime

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics", required=True)
    ap.add_argument("--out-csv", required=True)
    args = ap.parse_args()
    with open(args.metrics) as f:
        m = json.load(f)
    row = {
        "date": datetime.date.today().isoformat(),
        "ece_before": f"{m.get('ece_before', '')}",
        "ece_after": f"{m.get('ece_after', '')}",
        "n_samples": f"{m.get('n_samples', '')}",
    }
    header = ["date","ece_before","ece_after","n_samples"]
    exists = os.path.exists(args.out_csv)
    with open(args.out_csv, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        if not exists:
            w.writeheader()
        w.writerow(row)
    print("Appended trend:", row)

if __name__ == "__main__":
    main()