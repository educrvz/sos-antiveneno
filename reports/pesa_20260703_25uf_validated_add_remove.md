# PESA 2026-07-03 validated add/remove counts

Review date: 2026-07-26

Scope: 25 UFs only. BA and SP are excluded and carried forward.

Method: old CNES values from `extracted/{UF}.json` were searched directly in the new 2026-07-03 PDF text. Candidate additions from table extraction were then inspected against PDF context to remove phone/CEP/parser artifacts.

## Corrected answer

- Validated new places added: 4
- Validated old places removed: 1
- All validated add/remove changes are in RJ.

The earlier 30 added / 137 removed counts were candidate parser-review counts. They should not be used as production facts.

## One-by-one UF summary

| UF | Added | Removed |
|---|---:|---:|
| AC | 0 | 0 |
| AL | 0 | 0 |
| AM | 0 | 0 |
| AP | 0 | 0 |
| CE | 0 | 0 |
| DF | 0 | 0 |
| ES | 0 | 0 |
| GO | 0 | 0 |
| MA | 0 | 0 |
| MG | 0 | 0 |
| MS | 0 | 0 |
| MT | 0 | 0 |
| PA | 0 | 0 |
| PB | 0 | 0 |
| PE | 0 | 0 |
| PI | 0 | 0 |
| PR | 0 | 0 |
| RJ | 4 | 1 |
| RN | 0 | 0 |
| RO | 0 | 0 |
| RR | 0 | 0 |
| RS | 0 | 0 |
| SC | 0 | 0 |
| SE | 0 | 0 |
| TO | 0 | 0 |

## Validated additions

| UF | CNES | New city | New name | Notes |
|---|---:|---|---|---|
| RJ | 2287919 | Barra do Piraí | Hospital Nova Santa Casa de Barra do Piraí | Present in 2026-07-03 RJ PDF; absent from old RJ extraction. |
| RJ | 2287927 | Barra do Piraí | Hospital e Maternidade Maria de Nazaré | Present in 2026-07-03 RJ PDF; absent from old RJ extraction. |
| RJ | 2276186 | Paraíba do Sul | Hospital Nossa Senhora da Piedade | Present in 2026-07-03 RJ PDF; absent from old RJ extraction. |
| RJ | 4751140 | Petrópolis / Pedro do Rio | UPH Pedro do Rio | Present in 2026-07-03 RJ PDF; absent from old RJ extraction. Candidate parser put unit/address into shifted columns, but PDF context is clear. |

## Validated removals

| UF | CNES | Old city | Old name | Notes |
|---|---:|---|---|---|
| RJ | 6855334 | Itaperuna | UPA Itaperuna | Old CNES absent from 2026-07-03 RJ PDF text. New RJ PDF instead lists Posto de Urgência de Itaperuna, CNES 2279274, which already existed in old data. |

## False positives removed from earlier candidate counts

| UF | Token | Why not a new CNES |
|---|---|---|
| AP | 68980 | CEP fragment from existing Companhia Especial de Fronteira row, old CNES was blank in source. |
| PE | 7226001 | Part of 0800-7226001 phone for Hospital da Restauração; old CNES remains 655. |
| RO | 36613 | CEP fragment from old malformed CNES/CEP value 36613-9464 for Rio Crespo, not a new CNES. |
| RO | 99232 | Phone fragment from Nova União row, old CNES was blank in source. |
| MA | 98/99-prefixed tokens | Parser false positives from phone numbers and wrapped address fragments; all old valid MA CNES are present in new PDF text. |

## Production confidence

High confidence for add/remove counts after this pass: 4 added, 1 removed, excluding BA/SP.

Still do not push full refreshed hospital data until field-level text changes and geocoding are reviewed, because the candidate extractor still produces shifted fields in some states. The add/remove question is now separated from that parser noise.
