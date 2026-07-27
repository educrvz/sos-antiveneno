# Refresh diff — RO — 2026-07-26

- **Candidato:** `extracted/RO.new.json`
- **Atual:** `extracted/RO.json`
- **Linhas atuais:** 35
- **Linhas no candidato:** 31
- **CNES adicionados:** 2
- **CNES removidos:** 6
- **CNES alterados:** 19
- **Overrides desta UF afetados:** 0

> Este relatório não modifica nenhum arquivo. Use-o para decidir o que aceitar antes de promover o candidato a `extracted/{UF}.json`.

## CNES adicionados

| CNES | Município | Nome | Endereço | Soros |
|---|---|---|---|---|
| 36613 | Rio Crespo | Hospital De Pequeno Porte Elias De Oliveira Lima | Rua Ermelindo Milani, 1293 - Setor 02 | Botrópico, Laquético, Crotálico, Escorpiônico, Antiaracnídeo Loxoscélico |
| 99232 | Nova União | Hospital Municipal Expedito Gonçalves Ferreira | Rua Machado De Assis Nº 1496 | *(vazio)* |

## CNES removidos

| CNES | Município | Nome | Endereço | Soros |
|---|---|---|---|---|
| 2806711 | Chupinguaia | U M José Ivaldo De Souza | Rua Osvaldo Cruz N° 1495 Centro | Botrópico; Elapidico; Laquetico Escorpiônico, Crotálico, E Aracnídeo. |
| 28080544 | Colorado Do Oeste | Hospital Municipal Dr Pedro Grangeiro Xavier. | Rua Castanheira N°2711 - Minas Gerais. | Botrópico (Pentavalente), Botrópico (Pentavalente) E Antilaquético, Anticrotálico, Elapídico, Lonômoico, Escorpiônico, Aracnidio. |
| 2808625 | Mirante Da Serra | Hospital Municipal De Miante Da Serra SAMUEL MARQUES | Rua Minas Gerais, S/N. | Botrópico E Escorpiônico. |
| 36613-9464 | Rio Crespo | Hospital De Pequeno Porte Elias De Oliveira Lima | Rua Ermelindo Milani, 1293 - Setor 02 | Botrópico, Laquético, Crotálico, Escorpiônico, Antiaracnídeo Loxoscélico |
| 4003357 | Theobroma | Hospital Municipal José Almerindo do rosario | Av. pres. Jânio Quadros 1829, Theobroma, Ro, 76866-000 | Antibotropico Pentavalente, Antiaracnidio, Antitetânico, Escorpionico, Antirrabico. |
| 9322825 | Ariquemes | Unidade De Pronto Atendimento De Ariquemes | Avenida Tancredo Neves, 1500 - Setor Institucional | Botrópico, Laquético, Crotálico, Elapídico, Lonômico |

## CNES alterados

### 2334801 — Hospital São Lucas (69)33414295 28080544 Botrópico (Pentavalente),Botrópico (Pentavalente) E Antilaquético, Anticrotálico, Elapídico, Lonômoico, Escorpiônico, Aracnidio. (Cerejeiras Colorado Do Oeste Rua Castanheira N°2711 - Minas Gerais.)

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | Hospital São Lucas | Hospital São Lucas (69)33414295 28080544 Botrópico (Pentavalente),Botrópico (Pentavalente) E Antilaquético, Anticrotálico, Elapídico, Lonômoico, Escorpiônico, Aracnidio. |
| `municipality` | Cerejeiras | Cerejeiras Colorado Do Oeste Rua Castanheira N°2711 - Minas Gerais. |
| `antivenoms_raw` | Botrópico (Pentavalente), Crotálico, Elapídico; Laquético (Pentavalente), Aracnídico E Escorpiônico. | Botrópico (Pentavalente), Crotálico, Elapídico, Laquético (Pentavalente), Aracnídico E Escorpiônico. |

### 2495228 — Hospital Municipal Amélio João Da Silva (Rolim De Moura)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (69) 3442-1192/3091 | (69) 3442- 1192/3091 |

### 2495279 — Hospital Dr. Claudionor Couto Roriz (Ji-Paraná)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (69) 3416-4097/4181/4093 | (69) 3416- 4097/4181/4093 |

### 2495414 — Hospital E Maternidade Eufrasia Maria Da Conceição (Presidente Médici)

| Campo | Antes | Depois |
|---|---|---|
| `antivenoms_raw` | Botropico; Escorpionico, Aracnídeo. | Botropico, Escorpionico, Aracnídeo. |

### 2679477 — Hospital Municipal Vanessa E Vania Fuzari (69) 3643-1437 Botrópico, Laquético, Crotálico, Loxoscélico, Fonêutrico, Escorpiônico (Alta Floresta Alto Alegre Dos Parecis Hospital De Pequeno Porte Enfermeira Ana Neri Avenida Costa E Silva - Centro)

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | Hospital Municipal Vanessa E Vania Fuzari | Hospital Municipal Vanessa E Vania Fuzari (69) 3643-1437 Botrópico, Laquético, Crotálico, Loxoscélico, Fonêutrico, Escorpiônico |
| `municipality` | Alta Floresta | Alta Floresta Alto Alegre Dos Parecis Hospital De Pequeno Porte Enfermeira Ana Neri Avenida Costa E Silva - Centro |

### 2743612 — Hospital Municipal Jorge Cardoso De Sá (HPP) (Urupá Vale Do Anari Hospital De Pequeno Porte De Vale Do Anari)

| Campo | Antes | Depois |
|---|---|---|
| `municipality` | Urupá | Urupá Vale Do Anari Hospital De Pequeno Porte De Vale Do Anari |

### 2744422 — Hospital De Pequeno Porte Isabel Batista De Oliveira (Vale Do Paraíso)

| Campo | Antes | Depois |
|---|---|---|
| `address` | *(vazio)* | (69) 34641273 |
| `phones_raw` | (69) 34641273 |  |
| `source_notes` | address cell blank in source | *(vazio)* |

### 2798484 — Hospital Regional Adamastor Teixeira De Oliveira (Vilhena)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (69) 3321-3821/3322-4070 | (69) 3321- 3821/3322-4070 |

### 2807076 — Hospital Regional De Buritis (Buritis)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (69) 3238-2406/2408 | (69) 3238- 2406/2408 |

### 2808528 — Hospital Unidade Mista De Cabixi. (Cabixi)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | antivenoms listed as 'Rotálico' in source (likely typo for Crotálico) | *(vazio)* |

### 2808552 — Maria Aparecida Maurício (Corumbiara)

| Campo | Antes | Depois |
|---|---|---|
| `antivenoms_raw` | Botrópico; Crotálico; Elapídico; Laquétio; Aracnídeo, Escorpiônico, Lonômico. | Botrópico, Crotálico, Elapídico, Laquétio, Aracnídeo, Escorpiônico, Lonômico. |

### 2808587 — Hospital Municipal Angelina Georgetti (Espigão Do Oeste)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (69) 3912-8054/8022 | (69) 3912- 8054/8022 |

### 2808617 — Hospital Municipal De Machadinho D'oeste (Machadinho D'oeste)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (69) 3581-3286/2119 | (69) 3581- 3286/2119 |

### 2808633 — Hospital Municipal Ancelmo Bianchini (Nova Brasilândia)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | *(vazio)* | - |
| `source_notes` | phone cell shown as '-' in source | *(vazio)* |

### 4003039 — Hospital Municipal De Monte Negro (Monte Negro)

| Campo | Antes | Depois |
|---|---|---|
| `address` | R. Francisco Prestes, 2576-Setor 2 | R. Francisco Prestes, 2576- Setor 2 |
| `phones_raw` | (69) 999493-3219 | (69) 999493- 3219 |

### 506745 — Rua Sena Madureira, 99, Bairro São Pedro (UPA - Anna Beatriz Oliveira Da Silva)

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | UPA - Anna Beatriz Oliveira Da Silva | Rua Sena Madureira, 99, Bairro São Pedro |
| `municipality` | Ji-Paraná | UPA - Anna Beatriz Oliveira Da Silva |
| `address` | Rua Sena Madureira, 99, Bairro São Pedro |  |
| `phones_raw` | *(vazio)* |  |
| `source_notes` | phone cell blank in source | *(vazio)* |

### 5618347 — Rua Abunã, 308 - Vila Extrema (Hospital Regional De Extrema)

| Campo | Antes | Depois |
|---|---|---|
| `health_unit_name` | Hospital Regional De Extrema | Rua Abunã, 308 - Vila Extrema |
| `municipality` | Porto Velho | Hospital Regional De Extrema |
| `address` | Rua Abunã, 308 - Vila Extrema | (69) 3252- 1502/1233 |
| `phones_raw` | (69) 3252-1502/1233 |  |
| `source_notes` | municipality inherited (blank in source); antivenoms partially abbreviated | *(vazio)* |

### 7499264 — Unidade Básica De Saúde Vanildo Chagas Hadman (Cujubim)

| Campo | Antes | Depois |
|---|---|---|
| `source_notes` | phone appears as just '69' in source (fragment) | *(vazio)* |

### 7704364 — Hospital De Urgência E Emergência Regional De Cacoal (HEURO) (Cacoal)

| Campo | Antes | Depois |
|---|---|---|
| `phones_raw` | (69) 3441-2747/8623/6101 | (69) 3441- 2747/8623/6101 |

## Auditoria de overrides

Para cada override desta UF, comparação com o MS atualizado.
Decida manualmente se cada um continua válido antes de promover o candidato.

Nenhum override aplicável a esta UF.
---

Próximos passos sugeridos:

1. Revisar cada seção acima. Decidir aceitar/rejeitar/modificar.
2. Aplicar ajustes manuais no candidato se necessário.
3. Substituir: `cp extracted/RO.new.json extracted/RO.json`
4. Atualizar `data/source_dates.json` com a nova data do MS.
5. Rodar `./scripts/refresh_dataset.sh`.
6. Validar contagem (`python3 scripts/validate_hospitals_json.py app/hospitals.json`).
7. Commit + push.
