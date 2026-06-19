import argparse
import csv
import re
from datetime import datetime

import pandas as pd


DT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$")
LEADING_NUM_RE = re.compile(r"^\s*([-+]?\d+(\.\d+)?)")


def looks_like_datetime(s: str) -> bool:
    if not isinstance(s, str):
        return False
    s = s.strip()
    if not DT_RE.match(s):
        return False
    try:
        datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        return True
    except Exception:
        return False


def to_number_cell(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return x
    s = str(x).strip()
    if s == "" or s.lower() == "nan":
        return None
    m = LEADING_NUM_RE.match(s)
    if not m:
        return None
    v = m.group(1)
    try:
        if "." in v:
            return float(v)
        return int(v)
    except Exception:
        return None


def detect_data_start(rows):
    for i, r in enumerate(rows):
        if len(r) == 0:
            continue
        if looks_like_datetime(r[0]):
            return i
    raise RuntimeError("Non trovo l'inizio dei dati: nessuna riga con StartDate in formato YYYY-MM-DD HH:MM:SS")


def default_keep_columns(header):
    keep = []

    def add_prefix(prefix):
        for h in header:
            if h.startswith(prefix):
                keep.append(h)

    add_prefix("QID6_")
    add_prefix("QID7_")
    add_prefix("QID8_")
    add_prefix("QID11_")
    add_prefix("QID13_")
    add_prefix("QID28_")
    add_prefix("QID27_")
    add_prefix("QID14_")

    for h in ["QID17", "QID18", "QID19", "QID20", "QID21", "QID22", "QID23", "QID24"]:
        if h in header:
            keep.append(h)

    return keep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", required=True)
    ap.add_argument("--keep-all", action="store_true")
    ap.add_argument("--keep", nargs="*", default=None)
    args = ap.parse_args()

    with open(args.inp, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows or len(rows[0]) < 5:
        raise RuntimeError("CSV vuoto o non valido")

    header = rows[0]
    data_start = detect_data_start(rows)

    data_rows = rows[data_start:]

    df = pd.DataFrame(data_rows, columns=header)

    if args.keep_all:
        keep_cols = header
    elif args.keep is not None and len(args.keep) > 0:
        keep_cols = [c for c in args.keep if c in df.columns]
        if not keep_cols:
            raise RuntimeError("Nessuna delle colonne richieste con --keep esiste nel CSV")
    else:
        keep_cols = default_keep_columns(header)

    df = df[keep_cols].copy()

    for c in df.columns:
        df[c] = df[c].map(to_number_cell)

    df = df.dropna(how="all")

    non_empty_cols = [c for c in df.columns if df[c].notna().any()]
    df = df[non_empty_cols]

    df.to_csv(args.out, index=False, encoding="utf-8")
    print(f"OK: scritto {args.out} con {len(df)} righe e {len(df.columns)} colonne")


if __name__ == "__main__":
    main()
