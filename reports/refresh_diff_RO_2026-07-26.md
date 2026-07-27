# Refresh diff — RO — 2026-07-26

- **Candidato:** `extracted/RO.candidate.json`
- **Atual:** `extracted/RO.json`
- **Linhas atuais:** 35
- **Linhas no candidato:** 35
- **CNES adicionados:** 0
- **CNES removidos:** 0
- **CNES alterados:** 0
- **Overrides desta UF afetados:** 0

> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.

## CNES adicionados

Nenhum.

## CNES removidos

Nenhum.

## CNES alterados

Nenhum.
## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

Nenhum override aplicável a esta UF.
---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/RO.candidate.json extracted/RO.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
