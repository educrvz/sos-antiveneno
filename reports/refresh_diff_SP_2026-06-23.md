# Refresh diff — SP — 2026-06-23

- **Candidato:** `extracted/SP.new.json`
- **Atual:** `extracted/SP.json`
- **Linhas atuais:** 240
- **Linhas no candidato:** 243
- **CNES adicionados:** 3
- **CNES removidos:** 0
- **CNES alterados:** 0
- **Overrides desta UF afetados:** 6

> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.

## CNES adicionados

| CNES | Município | Nome | Endereço | Soros |
|---|---|---|---|---|
| 2082349 | Mauá | Hospital Nardini | Rua Regente Feijó, 166. Vila Bocaina | Botrópico, Crotálico, Escorpiônico, Loxoscélico, Fonêutrico |
| 2705680 | São José do Rio Preto | UPA Santo Antônio | Rua Ida Tagliavini Polachini, 580 – Vila Santo Antônio | Escorpiônico |
| 7706766 | São José do Rio Preto | UPA Tangará | Av. Pres. Getúlio Vargas, 381 – Jardim Tangará | Escorpiônico |

## CNES removidos

Nenhum.

## CNES alterados

Nenhum.
## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

### CNES 9164 — tipos: lat/lng

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Correção de coordenadas via reporte do usuário (distrito de São Francisco Xavier).

### CNES 2082187 — tipos: lat/lng, address, note

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Campus universitário não atende; endereço real é a Unidade de Emergência HCFMRP.

### CNES 2086271 — tipos: lat/lng

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Pin apontava para hospital errado; correção via reporte do usuário (Maternidade Municipal Zoraide Eva das Dores, Itapecerica da Serra/SP).

### CNES 9491252 — tipos: hide

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Dados misturados na fonte: CNES 9491252 está rotulado como 'Hospital de Base' em São José dos Campos, mas reaproveita endereço e telefone do CNES 2077396 (Hospital de Base de São José do Rio Preto). Sem dados confiáveis para o registro — ocultado para evitar pin enganoso.

### CNES 2034441 — tipos: lat/lng

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Correção de coordenadas via reporte do usuário (Pronto Socorro Municipal, Rio Claro/SP).

### CNES 4047184 — tipos: note

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Unidade de Retaguarda do Melhado (Araraquara/SP) — relato comunitário (06/05/2026) informando que, segundo a Secretaria Municipal de Saúde, o atendimento com soros antiofídicos e antiescorpiônicos é feito na UPA Central Amelia Bernardino Cutrale (Av. Maria Antônia Camargo de Oliveira, Vila Velosa; tel. (16) 3334-6900). Mantido visível com nota até confirmação oficial.

---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/SP.new.json extracted/SP.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
