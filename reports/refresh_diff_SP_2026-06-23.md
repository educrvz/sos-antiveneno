# Refresh diff — SP — 2026-06-23

- **Candidato:** `extracted/SP.new.json`
- **Atual:** `extracted/SP.json`
- **Linhas atuais:** 240
- **Linhas no candidato:** 243
- **CNES adicionados:** 3
- **CNES removidos:** 0
- **CNES alterados:** 13
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

### 135062 — Nova UPA Vila Cristina Piracicaba (Piracicaba)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | *(vazio)* | CNES shown as 6 digits in source |

### 2079224 — Hospital São José - Itapui (Itapuí)

| Campo | Antes | Depois |
|---|---|---|
| `address` | Avenida Paes de Barros,326-Centro | Avenida Paes de Barros,326- Centro |

### 2080095 — Santa Casa de Misericórdia (José Bonifácio)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (17) 3265- 9022 | (17) 3265-9022 |

### 2080923 — Hospital São Vicente (São José do Rio Pardo)

| Campo | Antes | Depois |
|---|---|---|
| `address` | Rua Coronel Alípio Dias, 620 -Centro | Rua Coronel Alípio Dias, 620 - Centro |

### 2082632 — HOSPITAL E MATERNIDADE SÃO JOSÉ (Barra Bonita)

| Campo | Antes | Depois |
|---|---|---|
| `address` | RUA 14 DE DEZEMBRO,490-CENTRO | RUA 14 DE DEZEMBRO,490- CENTRO |

### 2086336 — Hospital e Maternidade de Mairiporã (Mairiporã)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (11) 4419- 4422 | (11) 4419-4422 |

### 3028399 — Hospital Estadual Prof. Carlos da Silva Lacaz - Criança (Francisco Morato)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (11) 4489- 9444 | (11) 4489-9444 |

### 4048830 — Pronto Socorro Dr. Adaucto Freire de Andrade Monte Alto (Monte Alto)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (16) 3242-2100 / 8358 | (16) 3242-2100/8358 |

### 6878687 — Hospital Estadual Dr. Albano da Franca Rocha Sobrinho (Franco da Rocha)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (11) 3336- 8200 | (11) 3336-8200 |

### 6997600 — UPA Batatais José Antônio da Silva Neto (Batatais)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (16) 3761-9474 / 9499 | (16) 3761-9474/9499 |

### 7792115 — UPA Dr. Pedro T. F. Reis (Sertãozinho)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (16) 3947-1270 / 11590 | (16) 3947-1270/11590 |

### 9164 — UPA São Francisco Xavier (São José dos Campos)

| Campo | Antes | Depois |
|---|---|---|
| `address` | Rua Quinze de Novembro, s/n -Centro | Rua Quinze de Novembro, s/n - Centro |

### 9364226 — Unidade de Pronto Atendimento de Agenor de Campos (Mongaguá)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (13) 3507-1110 / 3506-5044 | (13) 3507-1110/3506-5044 |

## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

### CNES 9164 — tipos: lat/lng

**Status:** 🟡 REVISAR — MS mudou endereço — re-verificar lat/lng e address override

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
