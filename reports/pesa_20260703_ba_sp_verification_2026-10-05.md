# BA/SP — verification against the 2026-07-03 MS PDFs

Date: 2026-10-05

## Why this report exists

Commit `945dd30` (2026-08-02) set `data/source_dates.json` to `2026-07-03` for BA and SP, but `extracted/BA.json` and `extracted/SP.json` were last changed in June and no comparison report was committed. This report closes that gap.

## Sources

| UF | Previous source | New source | SHA-1 of new PDF (matches `data/source_hashes.json`) |
|---|---|---|---|
| BA | `BA_20260105.pdf` | `BA_20260703.pdf` | `159d9fd3d1d640eb729488826c6797112b6a8e98` |
| SP | `SP_20260525.pdf` | `SP_20260703.pdf` | `703c2303d0fcb075d6708176d5b7983f7de31e82` |

## Method

1. Full-text extraction of old and new PDFs with pdfplumber, then a token-level comparison (word multiset) of the whole document.
2. CNES set comparison: every 4–7 digit CNES in the new PDF text vs `extracted/{UF}.json` and the published `app/hospitals.json`.
3. Any non-identical token was inspected in context.

## Results

**BA:** 6,017 tokens in both versions; **zero token differences**. Same content, new file (the January PDF was larger due to rendering, not content). All 253 published BA CNES appear in the new PDF; no CNES in the new PDF is missing from the dataset (one 7-digit hit, `9817191`, is a phone fragment, not a CNES).

**SP:** 5,344 → 5,341 tokens. Every difference is a line-wrap/re-layout artifact (phones, CEPs and addresses split across lines differently, e.g. `3553-1144/99716-` + `4744` → `3553-` + `1144/99716-4744`). **No phone, address, unit or antivenom change.** All published SP CNES appear in the new PDF; no new CNES. Santa Casa de Itápolis is still listed without a CNES in the source, as before.

## Conclusion

The published BA and SP data already matches the 2026-07-03 Ministry PDFs. The `2026-07-03` source date is accurate. No change to `extracted/`, `hospitals.json` or overrides is required.
