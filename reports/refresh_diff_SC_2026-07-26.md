# Refresh diff — SC — 2026-07-26

- **Candidato:** `extracted/SC.new.json`
- **Atual:** `extracted/SC.json`
- **Linhas atuais:** 143
- **Linhas no candidato:** 142
- **CNES adicionados:** 0
- **CNES removidos:** 1
- **CNES alterados:** 1
- **Overrides desta UF afetados:** 0

> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.

## CNES adicionados

Nenhum.

## CNES removidos

| CNES | Município | Nome | Endereço | Soros |
|---|---|---|---|---|
| 2491095 | Canoinhas | Unidade de Pronto Atendimento Orestes Golanovski | R. Benjamin Constant, s/n, Boa Vista | Aracnídico, Escorpiônico, Lonômico |

## CNES alterados

### 2665107 — Hospital Santo Antônio de Itaiópolis (Itaiópolis)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (47) 99762-1405 | (47) 99762- 1405 |

## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

Nenhum override aplicável a esta UF.
---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/SC.new.json extracted/SC.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
