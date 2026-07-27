# Refresh diff — AC — 2026-07-26

- **Candidato:** `extracted/AC.candidate.json`
- **Atual:** `extracted/AC.json`
- **Linhas atuais:** 17
- **Linhas no candidato:** 17
- **CNES adicionados:** 0
- **CNES removidos:** 0
- **CNES alterados:** 1
- **Overrides desta UF afetados:** 0

> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.

## CNES adicionados

Nenhum.

## CNES removidos

Nenhum.

## CNES alterados

### 2001500 — Hospital de Clínicas Raimundo Chaar (Brasiléia)

| Campo | Antes | Depois |
|---|---|---|
| `address` | BR 317, km 01, Bairro ALberto Castro s/n | BR 317, km 01, Bairro Alberto Castro s/n |

## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

Nenhum override aplicável a esta UF.
---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/AC.candidate.json extracted/AC.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
