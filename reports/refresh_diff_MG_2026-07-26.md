# Refresh diff — MG — 2026-07-26

- **Candidato:** `extracted/MG.candidate.json`
- **Atual:** `extracted/MG.json`
- **Linhas atuais:** 292
- **Linhas no candidato:** 292
- **CNES adicionados:** 0
- **CNES removidos:** 0
- **CNES alterados:** 0
- **Overrides desta UF afetados:** 6

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

### CNES 8000956 — tipos: note

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Policlínica Pronto Atendimento (Conselheiro Lafaiete/MG) — dois relatos comunitários independentes (29/04/2026 e 03/05/2026) de que a policlínica está desativada há cerca de um ano e o serviço foi transferido para UPA 24h Dr. Luiz de Souza Dias (Rua Vereador Alfredo Mafuz, 525; tel. (31) 3764-9892). Mantido visível com nota até confirmação oficial.

### CNES 2219564 — tipos: note

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Hospital Universitário Clemente de Faria (Montes Claros/MG) — relato comunitário (10/05/2026) informando que o telefone publicado é da central Unimontes; o ramal direto do HUCF é (38) 3224-8000.

### CNES 2134071 — tipos: note

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Hospital Imaculada Conceição (Conceição do Mato Dentro/MG) — correção oficial da Secretaria Municipal de Saúde (contato.soroja@gmail.com, 13/05/2026) informando que, no município, os soros antiveneno são disponibilizados exclusivamente na UPA Dr. Juvêncio Guimarães (Antibotrópico, Anticrotálico e Antiescorpiônico). UPA ainda não consta na lista oficial PESA — logado em outreach/ para encaminhamento ao Ministério/Abracit.

### CNES 7802951 — tipos: lat/lng

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** UPA Adolpho Pereira Resende (Carmo do Paranaíba/MG) — endereço Ministerial geocodifica para local errado (~1.8 km do prédio real); coordenadas verificadas manualmente pelo mantenedor (30/05/2026, confirmado também por OSM como amenity=hospital). Endereço-texto preservado por política.

### CNES 2775999 — tipos: lat/lng, note

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Santa Casa Misericórdia (Passos/MG) — a lista oficial PESA do MS lista o endereço como 'Rua Barão de Passos', mas relato comunitário (13/05/2026) e a lógica do bairro 'Santa Casa' indicam que o endereço da Santa Casa e da UPA Passos (CNES 4042751) estão invertidos na fonte. Endereço-texto preservado por política; pin corrigido manualmente pelo mantenedor para a localização real da Santa Casa.

### CNES 4042751 — tipos: lat/lng, note

**Status:** ✅ MS inalterado — override segue válido.

**Reason gravado:** Unidade Pronto Atendimento (Passos/MG) — a lista oficial PESA do MS lista o endereço como 'Rua Santa Casa, 164', mas relato comunitário (13/05/2026) indica que os endereços da UPA e da Santa Casa Misericórdia (CNES 2775999) estão invertidos na fonte. Endereço-texto preservado por política; pin corrigido manualmente pelo mantenedor para a localização real da UPA.

---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/MG.candidate.json extracted/MG.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
