# Refresh diff — PE — 2026-07-26

- **Candidato:** `extracted/PE.new.json`
- **Atual:** `extracted/PE.json`
- **Linhas atuais:** 15
- **Linhas no candidato:** 14
- **CNES adicionados:** 1
- **CNES removidos:** 2
- **CNES alterados:** 13
- **Overrides desta UF afetados:** 0

> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.

## CNES adicionados

| CNES | Município | Nome | Endereço | Soros |
|---|---|---|---|---|
| 7226001 | Recife | Hospital da Restauração | Avenida Gov. Agamenon Magalhães, s/n - Derby | 655 Botrópico, Crotálico, Elapídico, Escorpiônico, Fonêutrico, Loxoscélico, Laquético |

## CNES removidos

| CNES | Município | Nome | Endereço | Soros |
|---|---|---|---|---|
| 6042414 | Petrolina | Hospital Universitário de Petrolina (HU-UNIVASF) | Avenida José de Sá Maniçoba, s/n - Centro | Botrópico, Crotálico, Elapídico, Escorpiônico, Fonêutrico, Loxoscélico |
| 655 | Recife | Hospital da Restauração | Avenida Gov. Agamenon Magalhães, s/n - Derby | Botrópico, Crotálico, Elapídico, Escorpiônico, Fonêutrico, Loxoscélico, Laquético |

## CNES alterados

### 2348489 — Hospital Regional Professor Agamenon Magalhães (Serra Talhada)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (87) 3831-9600 | (87) 3831- 9600 |

### 2356287 — Hospital Regional Inácio de Sá (Salgueiro)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (87) 3276-1190 | (87) 3276- 1190 |

### 2428385 — Hospital Regional Emília Câmara (Afogados da Ingazeira)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (87) 3838-8868 | (87) 3838- 8868 |

### 2428393 — Hospital Regional Sílvio Magalhães (Palmares)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (81) 3661-8400 | (81) 3661- 8400 |

### 2430711 — Avenida Joaquim Nabuco, s/n - Centro (Hospital Dom Malan/IMIP (Pediatria))

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | Hospital Dom Malan/IMIP (Pediatria) | Avenida Joaquim Nabuco, s/n - Centro |
| `municipality` | Petrolina | Hospital Dom Malan/IMIP (Pediatria) |
| `address` | Avenida Joaquim Nabuco, s/n - Centro | (87) 3202- 7000 |
| `phones_raw` | (87) 3202-7000 |  |

### 2551764 — Hospital e Policlínica Rui de Barros Correia (Arcoverde)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (87) 3821-8300 | (87) 3821- 8300 |

### 2702983 — Hospital Dom Moura (Garanhuns)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (87) 3761-6100 | (87) 3761- 6100 |

### 2711885 — Hospital Belarmino Correia (Goiana)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (81) 3626-8639 | (81) 3626- 8639 |

### 2711990 — Hospital Jaboatão Prazeres (Jaboatão dos Guararapes)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (81) 3184-4201 | (81) 3184- 4201 |

### 2712008 — Hospital João Murilo (Vitória de Santo Antão)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (81) 3526-8833 | (81) 3526- 8833 |

### 2712032 — Hospital Regional de Limoeiro (Limoeiro)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (81) 3628-8800 | (81) 3628- 8800 |

### 2712040 — Hospital Regional Fernando Bezerra (Ouricuri)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (87) 3874-4844 | (87) 3874- 4844 |

### 7498810 — Hospital Mestre Vitalino (Caruaru)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (81)3725-7750 | (81)3725- 7750 |

## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

Nenhum override aplicável a esta UF.
---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/PE.new.json extracted/PE.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
