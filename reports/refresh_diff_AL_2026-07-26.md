# Refresh diff — AL — 2026-07-26

- **Candidato:** `extracted/AL.new.json`
- **Atual:** `extracted/AL.json`
- **Linhas atuais:** 15
- **Linhas no candidato:** 14
- **CNES adicionados:** 0
- **CNES removidos:** 1
- **CNES alterados:** 5
- **Overrides desta UF afetados:** 1

> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.

## CNES adicionados

Nenhum.

## CNES removidos

| CNES | Município | Nome | Endereço | Soros |
|---|---|---|---|---|
| 2720035 | Maceió | Hospital Escola Dr. Helvio Auto - HEHA | Rua Cônego Fernando Lyra, no Trapiche da Barra | Botrópico, Crotálico, Laquético, Elapídico, Escorpiônico, Fonêutrico, Lonômico, Loxoscélico |

## CNES alterados

### 3015408 — Unidade de Emergência Dr. Daniel Houly (Arapiraca)

| Campo | Antes | Depois |
|---|---|---|
| `address` | Rod. AL 220, km 05 s/n Arapiraca | Rod. AL 220,km 05 s/n Arapiraca |
| `phones_raw` | (82) 359-2450 e 3529-2488 | (82) 359-2450 e 3529- 2488 |

### 4156714 — Av. Maceió, 341 - Tabuleiro do Martins, Maceió - AL, 57061- 110 (UPA Galba Novaes)

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | UPA Galba Novaes | Av. Maceió, 341 - Tabuleiro do Martins, Maceió - AL, 57061- 110 |
| `municipality` | Maceió | UPA Galba Novaes |
| `address` | Av. Maceió, 341 - Tabuleiro do Martins, Maceió - AL, 57061-110 | (82) 3315-3504 |
| `phones_raw` | (82) 3315-3504 |  |
| `source_notes` | municipality inherited from previous row (blank in source) | *(vazio)* |

### 4156730 — Av. Juca Sampaio, 600, Jacintinho (UPA 24 horas Dr Ismar Gatto)

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | UPA 24 horas Dr Ismar Gatto | Av. Juca Sampaio, 600, Jacintinho |
| `municipality` | Maceió | UPA 24 horas Dr Ismar Gatto |
| `address` | Av. Juca Sampaio, 600, Jacintinho | (82) 3023-5682 |
| `phones_raw` | (82) 3023-5682 |  |
| `source_notes` | municipality inherited from previous row (blank in source) | *(vazio)* |

### 7753470 — Hospital Regional da Mata (União dos Palmares)

| Campo | Antes | Depois |
|---|---|---|
| `address` | BR-104 - União dos Palmares, AL, 57800-000 | BR-104 - União dos Palmares, AL, 57800- 000 |

### 7916043 — UPA Maragogi (Maragogi)

| Campo | Antes | Depois |
|---|---|---|
| `address` | AL-101, 200 - Maragogi, AL, 57955-000 | AL-101, 200 - Maragogi, AL, 57955- 000 |

## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

### CNES 4156714 — tipos: lat/lng

**Status:** 🟡 REVISAR — MS mudou endereço — re-verificar lat/lng e address override

**Reason gravado:** Correção de coordenadas via reporte do usuário (UPA Galba Novaes, Maceió/AL).

---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/AL.new.json extracted/AL.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
