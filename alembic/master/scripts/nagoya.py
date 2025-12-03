#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_nagoya_0based.py

Reads Nagoya-表1.csv and writes a JSON-like file (created_at/updated_at written as identifier `now`).
This script treats all index values provided in the spec as 0-based.

Usage:
  python convert_nagoya_0based.py Nagoya-表1.csv nagoya_shop_data.json

Behavior:
 - Default skip rows (0-based): {9, 19, 21}
 - Processing order: 売上 then 経費, iterate date columns left-to-right.
 - Title matching is substring-based using MAPPING.
 - Amounts are cleaned (commas removed) and formatted to two decimals.
 - Output id starts at 229 by default.
"""
import csv
import re
import sys
from pathlib import Path

MAPPING = {
    '生鮮': 20,
    '菓子': 21,
    '飲料': 22,
    '惣菜': 23,
    '日用品': 24,
    '人件': 25,
    '広告宣伝': 26,
    '物流': 27,
    'その他': 28,
    '雑費': 29,
}

# default skip indices are 0-based per user's instruction
DEFAULT_SKIP_ZERO_BASED = {9, 19, 21}

DATE_RE = re.compile(r"\s*(\d{4})年\s*(\d{1,2})月\s*")

def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.reader(f))

def find_header(reader, keyword):
    for i, row in enumerate(reader):
        for j, cell in enumerate(row):
            if cell == keyword:
                return i, j
    return None, None

def parse_date_columns_exact(header_row, title_col_idx):
    date_cols = []
    for col_idx in range(title_col_idx + 1, len(header_row)):
        cell = header_row[col_idx]
        if not cell:
            continue
        s = str(cell).replace('"', '').strip()
        m = DATE_RE.match(s)
        if m:
            date_cols.append((col_idx, (int(m.group(1)), int(m.group(2)))))
    return date_cols

def read_title_rows(reader, header_row_idx, title_col_idx, skip_zero_based):
    rows = []
    i = header_row_idx + 1
    while i < len(reader):
        row = reader[i]
        if title_col_idx >= len(row):
            break
        title_raw = (row[title_col_idx] or "").strip()
        if title_raw in ("", "売上", "経費"):
            break
        # skip aggregate/profit lines explicitly
        if any(x in title_raw for x in ("売上合計", "経費合計", "利益")):
            i += 1
            continue
        # skip user requested rows (0-based)
        if i in skip_zero_based:
            i += 1
            continue
        rows.append((title_raw, row, i))
        i += 1
    return rows

def clean_amount(cell):
    if cell is None:
        return None
    s = str(cell).strip()
    if s == "":
        return None
    s = s.replace('"','').replace(',', '')
    s = re.sub(r"[^\d\.\-]", "", s)
    if s == "" or s == ".":
        return None
    try:
        return f"{float(s):.2f}"
    except:
        return None

def build_entries_by_exact_cols(reader, section_keyword, start_id, skip_zero_based, shop_id=3):
    header_idx, title_col_idx = find_header(reader, section_keyword)
    if header_idx is None:
        return [], start_id
    date_cols = parse_date_columns_exact(reader[header_idx], title_col_idx)
    title_rows = read_title_rows(reader, header_idx, title_col_idx, skip_zero_based)
    entries = []
    cur_id = start_id
    for col_idx, (year, month) in date_cols:
        for title_raw, row_values, row_idx in title_rows:
            matched = None
            for k, v in MAPPING.items():
                if k in title_raw:
                    matched = v
                    break
            if matched is None:
                continue
            amt_cell = row_values[col_idx] if col_idx < len(row_values) else ""
            cleaned = clean_amount(amt_cell)
            if cleaned is None:
                continue
            entries.append({
                "id": cur_id,
                "shop_id": shop_id,
                "shop_account_title_id": matched,
                "year": year,
                "month": month,
                "amount": cleaned,
            })
            cur_id += 1
    return entries, cur_id

def write_json_like(entries, outpath: Path):
    with outpath.open('w', encoding='utf-8') as fw:
        fw.write("[\n")
        for i, e in enumerate(entries):
            fw.write(" " * 4 + "{\n")
            fw.write(f'{" " * 8}"id": {e["id"]},\n')
            fw.write(f'{" " * 8}"shop_id": {e["shop_id"]},\n')
            fw.write(f'{" " * 8}"shop_account_title_id": {e["shop_account_title_id"]},\n')
            fw.write(f'{" " * 8}"year": {e["year"]},\n')
            fw.write(f'{" " * 8}"month": {e["month"]},\n')
            fw.write(f'{" " * 8}"amount": {e["amount"]},\n')
            fw.write(f'{" " * 8}"created_at": now,\n')
            fw.write(f'{" " * 8}"updated_at": now\n')
            fw.write(" " * 4 + "}")
            if i != len(entries) - 1:
                fw.write(",\n")
            else:
                fw.write("\n")
        fw.write("]\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_nagoya_0based.py Nagoya-表1.csv nagoya_shop_data.json", file=sys.stderr)
        sys.exit(1)
    csv_path = Path(sys.argv[1])
    json_path = Path(sys.argv[2])

    reader = read_csv(csv_path)
    skip_zero_based = DEFAULT_SKIP_ZERO_BASED.copy()

    entries = []
    cur_id = 229
    s_entries, cur_id = build_entries_by_exact_cols(reader, "売上", cur_id, skip_zero_based, shop_id=3)
    entries.extend(s_entries)
    e_entries, cur_id = build_entries_by_exact_cols(reader, "経費", cur_id, skip_zero_based, shop_id=3)
    entries.extend(e_entries)

    write_json_like(entries, json_path)
    print(f"Wrote {len(entries)} entries to {json_path}")

if __name__ == "__main__":
    main()
