# Refresh diff — SE — 2026-07-26

- **Candidato:** `extracted/SE.new.json`
- **Atual:** `extracted/SE.json`
- **Linhas atuais:** 17
- **Linhas no candidato:** 14
- **CNES adicionados:** 0
- **CNES removidos:** 3
- **CNES alterados:** 5
- **Overrides desta UF afetados:** 0

> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.

## CNES adicionados

Nenhum.

## CNES removidos

| CNES | Município | Nome | Endereço | Soros |
|---|---|---|---|---|
| 2372 | Aracaju | Hospital Municipal Zona Sul Desembargador Fernando Franco | Avenida Tarcisio Daniel - Farolandia | Botrópico, Crotálico, Elapídico, Escorpiônico, Fonêutrico, Loxoscélico, Lonômico |
| 2421534 | Neópolis | Hospital de Neópolis | Avenida José Odin Ribeiro, 791 - Centro | Botrópico, Crotálico, Elapídico, Escorpiônico, Fonêutrico, Loxoscélico, Lonômico |
| 2546000 | Simão Dias | Unidade de Pronto Atendimento 24H Pedro Valadares | Rua Júlio Manoel Oliveira, s/n - Centro | Botrópico, Crotálico, Elapídico, Escorpiônico, Fonêutrico, Loxoscélico, Lonômico |

## CNES alterados

### 2421542 — Hosp. Regional Governador João Alves Filho (Nossa Senhora da Glória)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (79) 3411-1335/1783/7007 | (79) 3411- 1335/1783/7007 |

### 2423529 — Hosp. Amparo de Maria (Estância)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (79) 3522-1314/2354/5888 | (79) 3522- 1314/2354/5888 |

### 2477661 — Hosp. Dr. Pedro Garcia Moreno (Itabaiana)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (79) 2431-1430/2086/2710 | (79) 2431- 1430/2086/2710 |

### 3841375 — Avenida Maranhão, s/n - 18 do Forte (79) 3248-1205 2372 Botrópico, Crotálico, Elapídico, Escorpiônico, Fonêutrico, Loxoscélico, Lonômico (Pronto Socorro Nestor Piva Avenida Tarcisio Daniel - Farolandia)

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | Pronto Socorro Nestor Piva | Avenida Maranhão, s/n - 18 do Forte (79) 3248-1205 2372 Botrópico, Crotálico, Elapídico, Escorpiônico, Fonêutrico, Loxoscélico, Lonômico |
| `municipality` | Aracaju | Pronto Socorro Nestor Piva Avenida Tarcisio Daniel - Farolandia |
| `address` | Avenida Maranhão, s/n - 18 do Forte | (79) 3212-0401 |
| `phones_raw` | (79) 3212-0401 |  |

### 6451632 — Pronto Atendimento 24h Fernando Franco (Nossa Senhora do Socorro)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (79) 3254-8074/3279-1125 | (79) 3254- 8074/3279-1125 |

## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

Nenhum override aplicável a esta UF.
---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/SE.new.json extracted/SE.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
