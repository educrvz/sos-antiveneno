# Refresh diff — MA — 2026-07-26

- **Candidato:** `extracted/MA.candidate.json`
- **Atual:** `extracted/MA.json`
- **Linhas atuais:** 154
- **Linhas no candidato:** 154
- **CNES adicionados:** 0
- **CNES removidos:** 0
- **CNES alterados:** 1
- **Overrides desta UF afetados:** 1

> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.

## CNES adicionados

Nenhum.

## CNES removidos

Nenhum.

## CNES alterados

### 2645424 — Centro de Saúde Candida Silva Rego (NOVA COLINAS)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | phone shown as 'Sem contato'; municipality inherited (blank in source) | phone shown as 'Sem contato' in source |

## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

### CNES 6483089 — tipos: note

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Hosp. Macrorregional de Urgência e Emergência de Presidente Dutra/SOCORRÃO (MA) — relato comunitário (29/04/2026) de telefone correto.

---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/MA.candidate.json extracted/MA.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
