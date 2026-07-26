# Refresh diff — TO — 2026-07-26

- **Candidato:** `extracted/TO.new.json`
- **Atual:** `extracted/TO.json`
- **Linhas atuais:** 37
- **Linhas no candidato:** 32
- **CNES adicionados:** 0
- **CNES removidos:** 5
- **CNES alterados:** 7
- **Overrides desta UF afetados:** 0

> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.

## CNES adicionados

Nenhum.

## CNES removidos

| CNES | Município | Nome | Endereço | Soros |
|---|---|---|---|---|
| 2370727 | Centenário | Unidade Básica de Saúde Antônio Gonçalves Lima | Avenida Ceará, s/n - Centro | Botrópico, Crotálico, Escorpiônico |
| 2469340 | Itacajá | Hospital Municipal N. S. da Conceição | Rua Costa e Silva, 201 - Centro | Botrópico, Crotálico, Escorpiônico, Aracnídeo |
| 2647095 | Xambioá | Hospital Regional de Xambioá | Avenida G, Qd. 16, Lote 18, NO 69 - Setor Leste | Botrópico, Crotálico, Elapídico, Escorpiônico, Aracnídeo, Lonômico |
| 2755149 | Paraíso do Tocantins | Hospital Regional de Paraíso Dr. Alfredo Oliveira Barros | Rua 3 Qda 02 LTS 01 AO 19, s/n - Setor Aeroporto | Botrópico, Crotálico, Elapídico, Escorpiônico, Aracnídeo, Lonômico |
| 3331326 | Gurupi | Unidade de Pronto Atendimento Dra. Márcia Mucky | Avenida Fernando de Noronha, 99 - Jardim São Lucas | Botrópico, Crotálico, Elapídico, Escorpiônico, Aracnídeo, Lonômico |

## CNES alterados

### 2467577 — Rua Tocantins, s/n - Centro (Unidade Básica de Saúde Alquino Gomes da Silva)

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | Unidade Básica de Saúde Alquino Gomes da Silva | Rua Tocantins, s/n - Centro |
| `municipality` | Recursolândia | Unidade Básica de Saúde Alquino Gomes da Silva |
| `address` | Rua Tocantins, s/n - Centro | (63) 3438-1163 |
| `phones_raw` | (63) 3438-1163 |  |

### 2468972 — Hospital Regional de Augustinópolis (Augustinópolis)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (63)3456-1292/1313 | (63)3456- 1292/1313 |

### 2492555 — Aureny II, Rua Perimetral II, 04, Qd. 72 e 73 (Pronto Atendimento Sul (UPA - Sul))

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | Pronto Atendimento Sul (UPA - Sul) | Aureny II, Rua Perimetral II, 04, Qd. 72 e 73 |
| `municipality` | Palmas | Pronto Atendimento Sul (UPA - Sul) |
| `address` | Aureny II, Rua Perimetral II, 04, Qd. 72 e 73 | (63)32127925 |
| `phones_raw` | (63)32127925 |  |
| `source_notes` | Municipality inherited from Palmas (merged cell in source) | *(vazio)* |

### 2755289 — 203 Norte, Al. LO 06, APM 02 - Plano Norte (Pronto Atendimento Norte (UPA - Norte))

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | Pronto Atendimento Norte (UPA - Norte) | 203 Norte, Al. LO 06, APM 02 - Plano Norte |
| `municipality` | Palmas | Pronto Atendimento Norte (UPA - Norte) |
| `address` | 203 Norte, Al. LO 06, APM 02 - Plano Norte | (63) 3218-5110 |
| `phones_raw` | (63) 3218-5110 |  |
| `source_notes` | Municipality inherited from Palmas (merged cell in source) | *(vazio)* |

### 2786109 — Rua Pres. Juscelino Kubitscheck, 1641 - Setor Central (Hospital Regional de Gurupi)

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | Hospital Regional de Gurupi | Rua Pres. Juscelino Kubitscheck, 1641 - Setor Central |
| `municipality` | Gurupi | Hospital Regional de Gurupi |
| `address` | Rua Pres. Juscelino Kubitscheck, 1641 - Setor Central | (63) 3315-0212 |
| `phones_raw` | (63) 3315-0212 |  |

### 2786125 — Hospital Regional Porto Nacional (Porto Nacional Recursolândia)

| Campo | Antes | Depois |
|---|---|---|
| `municipality` | Porto Nacional | Porto Nacional Recursolândia |

### 3668770 — Rua Raquel de Carvalho, nº 420 - Centro (Hospital Materno Infantil Tia Dedé)

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | Hospital Materno Infantil Tia Dedé | Rua Raquel de Carvalho, nº 420 - Centro |
| `municipality` | Porto Nacional | Hospital Materno Infantil Tia Dedé |
| `address` | Rua Raquel de Carvalho, nº 420 - Centro | (63) 3218-1792 |
| `phones_raw` | (63) 3218-1792 |  |
| `source_notes` | Municipality inherited from Porto Nacional (merged cell in source) | *(vazio)* |

## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

Nenhum override aplicável a esta UF.
---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/TO.new.json extracted/TO.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
