#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert CSV (two tables: 売上 / 経費) into a single JSON-like array file.
- created_at / updated_at are written as the identifier `now` (unquoted) as requested.
  NOTE: that makes the output NOT strict JSON. If you need valid JSON, change
  the output format to use a quoted ISO timestamp.

Usage:
  python convert_csv_to_json_by_substring.py input.csv output.json

Assumptions about CSV layout (matches your example):
- A header row contains the literal '売上' or '経費' in some column (e.g. col index 2).
  The date columns follow that cell (e.g. "2022年3月", "2022年6月", ...).
- Subsequent rows have the title in the same column as the '売上'/'経費' cell,
  and amounts aligned under the date columns.
- Rows for "売上合計", "経費合計", "利益" are ignored.
"""

import csv
import re
import sys
from pathlib import Path

# substring -> id mapping
MAPPING = {
    '生鮮': 1,
    '加工': 2,
    '菓子': 3,
    '飲料': 4,
    '惣菜': 5,
    '人件': 6,
    '水道光熱': 7,
    '広告宣伝': 8,
    '物流': 9,
    'その他': 10,
}

SKIP_SUBSTRINGS = ("売上合計", "経費合計", "利益")

DATE_RE = re.compile(r"\s*(\d{4})年\s*(\d{1,2})月\s*")

def parse_dates_from_header(row, pos):
    """Parse (year, month) tuples from header cells after pos."""
    dates = []
    for cell in row[pos+1:]:
        if not cell:
            dates.append(None)
            continue
        cell_s = cell.replace('"', '').strip()
        m = DATE_RE.match(cell_s)
        if m:
            dates.append((int(m.group(1)), int(m.group(2))))
        else:
            dates.append(None)
    return dates

def clean_amount(cell):
    """Return formatted string like '1234.00' or None if not a valid number."""
    if cell is None:
        return None
    s = str(cell).strip()
    if s == "":
        return None
    # remove commas and any surrounding quotes
    s = s.replace('"', '').replace(',', '')
    # remove any non-digit except dot and minus
    s = re.sub(r"[^\d\.\-]", "", s)
    if s == "" or s == ".":
        return None
    try:
        f = float(s)
        return f"{f:.2f}"
    except Exception:
        return None

def find_header_positions(reader):
    """Return list of tuples (row_index, col_index, header_type('売上'|'経費'))"""
    headers = []
    for i, row in enumerate(reader):
        for j, cell in enumerate(row):
            if cell == '売上' or cell == '経費':
                headers.append((i, j, cell))
                # if same row contains both, both will be recorded; acceptable
                break
    return headers

def main(infile: str, outfile: str):
    infile = Path(infile)
    outfile = Path(outfile)

    with infile.open(newline='', encoding='utf-8-sig') as f:
        reader = list(csv.reader(f))

    headers = find_header_positions(reader)
    if not headers:
        print("ERROR: no '売上' or '経費' header found in CSV.", file=sys.stderr)
        sys.exit(1)

    entries = []
    id_counter = 1

    # Process each header block in order of appearance
    for header_row_idx, title_col_idx, header_type in headers:
        dates = parse_dates_from_header(reader[header_row_idx], title_col_idx)
        # iterate following rows until a blank row or another header row
        i = header_row_idx + 1
        while i < len(reader):
            row = reader[i]
            # guard index
            if title_col_idx >= len(row):
                # treat as empty title -> break section
                break
            raw_title = (row[title_col_idx] or "").strip()
            # stop if we encountered another header marker in same column
            if raw_title in ('売上', '経費'):
                break
            # empty row indicates end of this section
            if raw_title == "":
                break
            # skip sum/profit rows
            if any(skip in raw_title for skip in SKIP_SUBSTRINGS):
                i += 1
                continue
            # determine mapping by substring match
            mapped_id = None
            for key_sub, val in MAPPING.items():
                if key_sub in raw_title:
                    mapped_id = val
                    break
            if mapped_id is None:
                # warn and skip
                print(f"WARNING: unmapped title at line {i+1}: '{raw_title}' - skipping", file=sys.stderr)
                i += 1
                continue
            # for each date column, read amount
            for idx, dt in enumerate(dates):
                if dt is None:
                    continue
                year, month = dt
                col_idx = title_col_idx + 1 + idx
                amt_cell = row[col_idx] if col_idx < len(row) else ""
                cleaned = clean_amount(amt_cell)
                if cleaned is None:
                    continue
                # append entry; amount stored as formatted number string for writing
                entries.append({
                    "id": id_counter,
                    "shop_id": 1,
                    "shop_account_title_id": mapped_id,
                    "year": year,
                    "month": month,
                    "amount": cleaned,
                })
                id_counter += 1
            i += 1

    # write output as requested: created_at/updated_at as identifier now (unquoted)
    with outfile.open('w', encoding='utf-8') as fw:
        fw.write("[\n")
        for n, e in enumerate(entries):
            fw.write("  {\n")
            fw.write(f'    "id": {e["id"]},\n')
            fw.write(f'    "shop_id": {e["shop_id"]},\n')
            fw.write(f'    "shop_account_title_id": {e["shop_account_title_id"]},\n')
            fw.write(f'    "year": {e["year"]},\n')
            fw.write(f'    "month": {e["month"]},\n')
            fw.write(f'    "amount": {e["amount"]},\n')
            fw.write('    "created_at": now,\n')
            fw.write('    "updated_at": now\n')
            fw.write("  }")
            if n != len(entries) - 1:
                fw.write(",\n")
            else:
                fw.write("\n")
        fw.write("]\n")

    print(f"Wrote {len(entries)} entries to {outfile}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_csv_to_json_by_substring.py input.csv output.json", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
