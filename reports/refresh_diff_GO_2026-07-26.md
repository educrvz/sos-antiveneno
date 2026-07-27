# Refresh diff — GO — 2026-07-26

- **Candidato:** `extracted/GO.candidate.json`
- **Atual:** `extracted/GO.json`
- **Linhas atuais:** 87
- **Linhas no candidato:** 87
- **CNES adicionados:** 0
- **CNES removidos:** 0
- **CNES alterados:** 2
- **Overrides desta UF afetados:** 3

> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.

## CNES adicionados

Nenhum.

## CNES removidos

Nenhum.

## CNES alterados

### 2343525 — Hospital de Caridade São Pedro D’alcântara (Goiás)

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | Hospital de Caridade São Pedro D'alcântara | Hospital de Caridade São Pedro D’alcântara |

### 2534967 — Hospital Regional de Formosa Dr César Saad Fayad (Formosa)

| Campo | Antes | Depois |
|---|---|---|
| `antivenoms_raw` | Botrópico, Crotálico. Escorpiônico, Fonêutrico, Loxoscélico, Lonômico, Elapídico | Botrópico, Crotálico, Escorpiônico, Fonêutrico, Loxoscélico, Lonômico, Elapídico |

## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

### CNES 2569701 — tipos: note

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Hospital Municipal de São Domingos (São Domingos/GO) — relato comunitário (29/04/2026) de possível encerramento; mantido visível com nota até confirmação oficial.

### CNES 2535556 — tipos: lat/lng

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Hospital das Clínicas Dr. Serafim de Carvalho (Jataí/GO) — pin apontava para uma escola; coordenadas corrigidas e verificadas manualmente no Google Maps (mantenedor, 09/05/2026).

### CNES 2342073 — tipos: note

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Hospital Municipal Gumercino Barbosa (Alto Paraíso de Goiás/GO) — relato comunitário (18/06/2026) informando que a unidade está sem soro em estoque no momento. Data ausente na planilha; usada a data da última linha datada da planilha (18/06/2026) como âncora para manter o padrão de atribuição.

---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/GO.candidate.json extracted/GO.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
