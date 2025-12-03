#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert Osaka-表1.csv into osaka_shop_data.json in the requested format.
- Indent: 4 spaces
- created_at/updated_at are written as the identifier `now` (unquoted) per request.
- IDs start at 121.
- Process order: 売上 then 経費, and within each section iterate columns (dates) left-to-right,
  emitting entries for each title in the order they appear under the section.
- Skips CSV row indices 8, 17, 19 (0-based counting as requested by user).
"""

import csv
import re
import sys
from pathlib import Path

MAPPING = {
    '菓子': 11,
    '飲料': 12,
    'おもちゃ': 13,
    '日用品': 14,
    '人件': 15,
    '広告宣伝': 16,
    '物流': 17,
    'その他': 18,
    '販管': 19,
}

SKIP_ROW_INDICES = {8, 17, 19}  # 0-based indices as given by user
DATE_RE = re.compile(r"\s*(\d{4})年\s*(\d{1,2})月\s*")

def parse_csv(path: Path):
    with path.open(newline='', encoding='utf-8-sig') as f:
        reader = list(csv.reader(f))
    return reader

def find_section_header(reader, keyword):
    # return (row_index, col_index) where a cell equals keyword
    for i, row in enumerate(reader):
        for j, cell in enumerate(row):
            if cell == keyword:
                return i, j
    return None, None

def parse_dates(header_row, title_col_idx):
    dates = []
    for cell in header_row[title_col_idx+1:]:
        if not cell:
            dates.append(None)
            continue
        s = cell.replace('"', '').strip()
        m = DATE_RE.match(s)
        if m:
            dates.append((int(m.group(1)), int(m.group(2))))
        else:
            dates.append(None)
    return dates

def read_titles_and_amounts(reader, start_row, title_col_idx, dates_len):
    """
    Read rows starting at start_row+1 until a blank row or next empty title cell.
    Return list of tuples: (title_raw, [amount_cell *dates_len])
    """
    rows = []
    i = start_row + 1
    while i < len(reader):
        row = reader[i]
        # if title column out of range or empty -> end of section
        if title_col_idx >= len(row):
            break
        title_raw = (row[title_col_idx] or "").strip()
        # stop on encountering another header marker
        if title_raw in ("売上", "経費"):
            break
        # empty row -> break
        if title_raw == "":
            break
        # skip rows whose index are in SKIP_ROW_INDICES (user requested)
        if i in SKIP_ROW_INDICES:
            i += 1
            continue
        # gather amount cells for dates_len columns starting title_col_idx+1
        amounts = []
        for k in range(dates_len):
            idx = title_col_idx + 1 + k
            val = row[idx] if idx < len(row) else ""
            amounts.append(val)
        rows.append((title_raw, amounts))
        i += 1
    return rows

def clean_amount(cell):
    if cell is None:
        return None
    s = str(cell).strip()
    if s == "":
        return None
    s = s.replace('"', '').replace(',', '')
    s = re.sub(r"[^\d\.\-]", "", s)
    if s == "" or s == ".":
        return None
    try:
        f = float(s)
        return f"{f:.2f}"
    except:
        return None

def build_entries(reader, section_keyword, id_start):
    header_row_idx, title_col_idx = find_section_header(reader, section_keyword)
    if header_row_idx is None:
        return [], id_start
    dates = parse_dates(reader[header_row_idx], title_col_idx)
    dates_len = len(dates)
    title_rows = read_titles_and_amounts(reader, header_row_idx, title_col_idx, dates_len)
    entries = []
    cur_id = id_start
    # process by columns (left-to-right), for each column iterate title rows in listed order
    for col_idx, dt in enumerate(dates):
        if dt is None:
            continue
        year, month = dt
        for title_raw, amounts in title_rows:
            # skip sum/profit rows by substring
            if any(skip in title_raw for skip in ("売上合計", "経費合計", "利益")):
                continue
            # determine mapping by substring match
            matched = None
            for key_sub, val in MAPPING.items():
                if key_sub in title_raw:
                    matched = val
                    break
            if matched is None:
                # if title not in mapping, skip
                continue
            amt_cell = amounts[col_idx] if col_idx < len(amounts) else ""
            cleaned = clean_amount(amt_cell)
            if cleaned is None:
                continue
            entries.append({
                "id": cur_id,
                "shop_id": 2,
                "shop_account_title_id": matched,
                "year": year,
                "month": month,
                "amount": cleaned,
            })
            cur_id += 1
    return entries, cur_id

def write_output(entries, outfile: Path):
    with outfile.open('w', encoding='utf-8') as fw:
        fw.write('[\n')
        for i, e in enumerate(entries):
            fw.write(' ' * 4 + '{\n')
            fw.write(f'{" " * 8}"id": {e["id"]},\n')
            fw.write(f'{" " * 8}"shop_id": {e["shop_id"]},\n')
            fw.write(f'{" " * 8}"shop_account_title_id": {e["shop_account_title_id"]},\n')
            fw.write(f'{" " * 8}"year": {e["year"]},\n')
            fw.write(f'{" " * 8}"month": {e["month"]},\n')
            fw.write(f'{" " * 8}"amount": {e["amount"]},\n')
            fw.write(f'{" " * 8}"created_at": now,\n')
            fw.write(f'{" " * 8}"updated_at": now\n')
            fw.write(' ' * 4 + '}')
            if i != len(entries) - 1:
                fw.write(',\n')
            else:
                fw.write('\n')
        fw.write(']\n')

def main(csv_path: str, out_json: str):
    reader = parse_csv(Path(csv_path))
    entries = []
    cur_id = 121
    # process 売上 then 経費
    s_entries, cur_id = build_entries(reader, "売上", cur_id)
    entries.extend(s_entries)
    e_entries, cur_id = build_entries(reader, "経費", cur_id)
    entries.extend(e_entries)
    # write json-like file
    write_output(entries, Path(out_json))
    print(f"Wrote {len(entries)} entries to {out_json}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_osaka_csv.py Osaka-表1.csv osaka_shop_data.json", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
