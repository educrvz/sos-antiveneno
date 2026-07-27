# Refresh diff — RN — 2026-07-26

- **Candidato:** `extracted/RN.new.json`
- **Atual:** `extracted/RN.json`
- **Linhas atuais:** 5
- **Linhas no candidato:** 5
- **CNES adicionados:** 0
- **CNES removidos:** 0
- **CNES alterados:** 2
- **Overrides desta UF afetados:** 0

> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.

## CNES adicionados

Nenhum.

## CNES removidos

Nenhum.

## CNES alterados

### 2389061 — Hospital Regional Tarcísio Maia (Mossoró)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (84) 3315-3379/3414 | (84) 3315- 3379/3414 |

### 2654261 — Avenida Pedro Álvares Cabral, s/n - Parque dos Coqueiros (Hosp. Pediátrico Maria Alice Fernandes)

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | Hosp. Pediátrico Maria Alice Fernandes | Avenida Pedro Álvares Cabral, s/n - Parque dos Coqueiros |
| `municipality` | Natal | Hosp. Pediátrico Maria Alice Fernandes |
| `address` | Avenida Pedro Álvares Cabral, s/n - Parque dos Coqueiros | (84) 3232- 7717/5408 |
| `phones_raw` | (84) 3232-7717/5408 |  |

## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

Nenhum override aplicável a esta UF.
---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/RN.new.json extracted/RN.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
