# Refresh diff — PI — 2026-07-26

- **Candidato:** `extracted/PI.candidate.json`
- **Atual:** `extracted/PI.json`
- **Linhas atuais:** 17
- **Linhas no candidato:** 17
- **CNES adicionados:** 0
- **CNES removidos:** 0
- **CNES alterados:** 17
- **Overrides desta UF afetados:** 0

> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.

## CNES adicionados

Nenhum.

## CNES removidos

Nenhum.

## CNES alterados

### 2323338 — Inst. de Doenças Tropicais Natan Portela – IDTNP (Teresina)

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | Inst. de Doenças Tropicais Natan Portela - IDTNP | Inst. de Doenças Tropicais Natan Portela – IDTNP |
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2323680 — Hosp. Reg. Senador Dirceu Arcoverde (Urucui)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2323915 — Hospital Regional Leônidas Melo (Barras)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2364816 — Hospital Regional de Bom Jesus (Bom Jesus)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2364883 — Hospital de Amarante (Amarante)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2364913 — Hospital Regional Mariana Pires Ferreira (Paulistana)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2365146 — Hospital Regional Tibério Nunes (Floriano)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2365383 — Hospital Regional Teresinha Nunes Barros (Sao João do Piauí)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2694301 — Hosp. Mun. Noberto Angelo Pereira (Fronteiras)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2777649 — Hospital Regional Senador José Candido Ferraz (São Raimundo Nonato)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2777746 — Hosp. Reg. Chagas Rodrigues (Piripiri)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2777754 — Hospital Regional de Campo Maior (Campo Maior)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2777762 — Hospital Regional Deolindo Couto (Oeiras)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2777770 — Hospital Regional Dr. João Pacheco Cavalcante (Corrente)

| Campo | Antes | Depois |
|---|---|---|
| `antivenoms_raw` | Botrópico, Crotálico, Elapídico, Fonêutrico, Loxoscélico, Laquetico, Escorpiônico | Botrópico, Crotálico, Elapídico, Fonêutrico, Loxoscélico, Laquético, Escorpiônico |
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 2777789 — Hospital Regional Estáquio Portela (Valença)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 4009622 — Hospital Regional Justino Luz (Picos)

| Campo | Antes | Depois |
|---|---|---|
| `antivenoms_raw` | Botrópico, Crotálico, Elapídico, Foneutrico, Loxoscelico, Laquetico, Escorpiônico | Botrópico, Crotálico, Elapídico, Fonêutrico, Loxoscélico, Laquético, Escorpiônico |
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

### 8015899 — Hospital Estadual Dirceu Arcoverde (Parnaíba)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | V2 PDF used; PI source is image-based | *(vazio)* |

## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

Nenhum override aplicável a esta UF.
---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/PI.candidate.json extracted/PI.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
