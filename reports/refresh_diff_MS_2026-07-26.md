# Refresh diff — MS — 2026-07-26

- **Candidato:** `extracted/MS.new.json`
- **Atual:** `extracted/MS.json`
- **Linhas atuais:** 67
- **Linhas no candidato:** 66
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
| 2482606 | Iguatemi | Pronto Atendimento Municipal | Rua Gelson Andrade Moreira, 1003 - Centro | Crotálico, Escorpiônico, Botrópico, Fonêutrico, Loxoscélico, Elapídico |

## CNES alterados

### 2375680 — Santa Casa de Cassilândia (Cassilândia)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | *(vazio)* |  |
| `source_notes` | phone cell blank in source | *(vazio)* |

## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

Nenhum override aplicável a esta UF.
---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/MS.new.json extracted/MS.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
