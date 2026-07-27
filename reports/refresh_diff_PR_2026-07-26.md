# Refresh diff — PR — 2026-07-26

- **Candidato:** `extracted/PR.candidate.json`
- **Atual:** `extracted/PR.json`
- **Linhas atuais:** 204
- **Linhas no candidato:** 204
- **CNES adicionados:** 0
- **CNES removidos:** 0
- **CNES alterados:** 0
- **Overrides desta UF afetados:** 2

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

### CNES 2738252 — tipos: note

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Hospital do Coração (Cascavel/PR) — três relatos comunitários (27/04, 01/05 e 21/05/2026) afirmando que o hospital foi desativado e o último (21/05, arquiteto) confirma demolição do prédio. Mantido visível com nota explícita até confirmação oficial.

### CNES 2683202 — tipos: note

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Hospital Municipal Dr. Amadeu Puppi (Ponta Grossa/PR) — relato comunitário (03/05/2026) de que o atendimento para acidentes com animais peçonhentos foi descentralizado para HU-UEPG e UPAs do município; mantido visível com nota até confirmação oficial.

---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/PR.candidate.json extracted/PR.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
