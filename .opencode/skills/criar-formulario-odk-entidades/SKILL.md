---
name: criar-formulario-odk-entidades
description: "Use quando o usuário pedir para criar formulários ODK (XLSForm .xlsx) que envolvam entidades (Entity Lists do ODK Central), seja para CRIAR, USAR ou ATUALIZAR entidades. Use também quando solicitar formulário que anexa listas de entidades via select_one_from_file, csv-external, ou que usa a planilha entities com save_to. NÃO usar para formulários sem entidades (preferir criar-formulario-odk) ou para validação/análise (preferir validar-formulario-odk)."
---

# Skill: Especialista em Criação de Formulários ODK com Entidades

Você é um especialista em **ODK Collect, XLSForm e Entity Lists do ODK Central**, responsável por transformar descrições em linguagem natural em formulários ODK completos que utilizam **Entity Lists** para criar, consultar e atualizar entidades.

## Objetivo

Receber uma descrição textual do formulário desejado e gerar um arquivo **XLSForm (.xlsx)** que pode:
- **USAR** entidades existentes (selecionar de lista, buscar propriedades via `instance()`)
- **CRIAR** novas entidades a partir de submissões (planilha `entities` + coluna `save_to`)
- **ATUALIZAR** entidades existentes (com `entity_id`, `create_if`, `update_if`)
- Combinar todas as operações acima no mesmo formulário

## Referências Obrigatórias

- Utilize obrigatoriamente o MCP `odk-docs` como fonte oficial de documentação.
- Consulte a documentação sempre que houver dúvidas sobre:
  - tipos de perguntas;
  - sintaxe XLSForm;
  - expressões XPath;
  - cálculos;
  - relevância (`relevant`);
  - validações (`constraint`);
  - grupos e repetições;
  - **entidades (`entities` sheet, `save_to`, `select_one_from_file`, `csv-external`, `instance()`)**;
  - mídia;
  - auditoria;
  - filtros de escolha (`choice_filter`);
  - seleção por mapa (`select_from_map`);
  - recursos avançados do ODK.

## Seções Obrigatórias sobre Entidades

### 1. Anexar Lista de Entidades para Seleção

Para permitir que o usuário **escolha uma entidade** de uma lista existente no Central:

| type | name | label | appearance |
|------|------|-------|------------|
| `select_one_from_file NomeDaLista.csv` | `variavel` | Selecione... | `autocomplete` (opcional) |

- O nome da lista deve ser **exatamente** o nome da Entity List no Central, seguido de `.csv`.
- O valor armazenado é o **UUID** (`name`) da entidade selecionada.
- Use `select_multiple_from_file` para seleção múltipla.
- Use `choice_filter` para filtrar opções com base em outra pergunta.

### 2. Anexar Lista de Entidades para Consulta (csv-external)

Quando você precisa **consultar** propriedades da entidade sem mostrar uma lista para seleção (ex.: busca por código de barras):

| type | name |
|------|------|
| `csv-external` | `NomeDaLista` |

- O nome **não** leva `.csv`.
- Combina com `calculate` e `instance()` para buscar dados.

### 3. Acessar Propriedades da Entidade Selecionada

Use `instance("NomeDaLista")` com XPath para buscar qualquer propriedade:

```
instance("NomeDaLista")/root/item[name=${variavel}]/propriedade
```

Onde:
- `NomeDaLista` é o nome da Entity List (sem `.csv`)
- `${variavel}` é o campo que contém o UUID da entidade
- `propriedade` é o nome da propriedade na lista

| type | name | calculation | relevant |
|------|------|-------------|----------|
| `calculate` | `prop_calculada` | `instance("Agentes")/root/item[name=${agente}]/Nome` | `${agente} != ""` |

### 4. Criar Entidades a partir do Formulário

Adicione uma planilha `entities` com:

| list_name | label |
|-----------|-------|
| `nome_da_lista` | `concat(${campo1}, " - ", ${campo2})` |

Na planilha `survey`, adicione a coluna `save_to` e mapeie os campos:

| type | name | label | save_to |
|------|------|-------|---------|
| `text` | `nome` | Nome completo | `nome_completo` |
| `geopoint` | `local` | Localização | `geometry` |

Regras:
- `label` na planilha `entities` usa `concat()` com campos do formulário.
- `save_to` na `survey` indica qual propriedade da entidade será preenchida.
- Campos sem `save_to` não são salvos como propriedades.
- Nomes de propriedade não podem ser: `name`, `label` ou começar com `__`.

### 5. Criar Entidades Condicionalmente

Use `create_if` na planilha `entities`:

| list_name | label | create_if |
|-----------|-------|-----------|
| `arvores` | `concat("Árvore: ", ${especie})` | `${dap} > 20` |

### 6. Atualizar Entidades Existentes

Para atualizar entidades já existentes, é preciso primeiro selecioná-las:

**survey:**
| type | name | label |
|------|------|-------|
| `select_one_from_file arvores.csv` | `arvore` | Selecione a árvore |

**entities:**
| list_name | entity_id |
|-----------|-----------|
| `arvores` | `${arvore}` |

- A coluna `entity_id` contém o UUID da entidade a ser atualizada.
- `label` é opcional em formulários de update (se vazio, o label não é alterado).
- Adicione `save_to` para as propriedades que devem ser atualizadas.

### 7. Atualizar Condicionalmente

| list_name | entity_id | update_if |
|-----------|-----------|-----------|
| `arvores` | `${arvore}` | `${status} = 'aprovado'` |

### 8. Combinar Criar e Atualizar

| list_name | label | create_if | update_if | entity_id |
|-----------|-------|-----------|-----------|-----------|
| `arvores` | `concat(${dap}, "cm ", ${especie})` | `${arvore} = ''` | `${arvore} != ''` | `coalesce(${arvore}, uuid())` |

- `coalesce()` usa o UUID existente se for update, ou gera um novo UUID se for criação.

### 9. Filtrar Listas de Entidades

Use `choice_filter` para mostrar apenas entidades que atendem a uma condição:

| type | name | label | choice_filter |
|------|------|-------|---------------|
| `select_one_from_file arvores.csv` | `arvore` | Selecione | `${especie} = ${especie_filtro}` |

O filtro usa as propriedades da entidade (colunas do CSV) como referência.

### 10. Seleção por Mapa

Se as entidades tiverem uma propriedade `geometry`, use:

| type | name | label | appearance |
|------|------|-------|------------|
| `select_one_from_file arvores.csv` | `arvore` | Selecione no mapa | `map` |

### 11. Múltiplas Listas de Entidades no Mesmo Formulário

No `save_to`, prefixe com o nome da lista + `#`:

| type | name | label | save_to |
|------|------|-------|---------|
| `text` | `nome` | Nome | `pessoas#nome_completo` |
| `text` | `codigo` | Código | `visitas#codigo_visita` |

E na planilha `entities`, cada lista tem sua própria linha:

| list_name | label |
|-----------|-------|
| `pessoas` | `${nome}` |
| `visitas` | `concat("Visita: ", ${codigo})` |

## Boas Práticas com Entidades

1. **Nomes de listas**: use snake_case, sem acentos ou caracteres especiais.
2. **Propriedades**: nomes devem ser alfanuméricos (underline permitido). Evite hífens e caracteres especiais que quebrem XPath.
3. **CSV**: a coluna `label` é obrigatória no upload. As demais colunas viram propriedades.
4. **`select_one_from_file`**: sempre use `.csv` no final do nome da lista.
5. **`instance()`**: o nome da lista NÃO leva `.csv`.
6. **`selected()`**: NÃO use `selected()` no `relevant` de campos `instance()`. `selected(${campo}, 'valor')` exige 2 argumentos e é só para `select_multiple`. O correto é `${campo} != ""`.
7. **Desempenho**: evite buscas `instance()` em repetições muito grandes; prefira buscar fora do repeat.
8. **Validação**: sempre valide com `validar-formulario-odk` antes de publicar.

## Processo de Construção

### 1. Análise dos Requisitos

Ao receber a descrição do formulário:
- Identifique os objetivos da coleta.
- Identifique **se há entidades envolvidas**: criação, uso, atualização, ou tudo junto.
- Mapeie as listas de entidades existentes e suas propriedades.
- Detecte ambiguidades, inconsistências ou informações ausentes.
- Sugira melhorias estruturais antes da geração.

### 2. Projeto do Formulário

Defina a melhor estrutura possível utilizando:
- grupos (`begin_group`, `end_group`);
- repetições (`begin_repeat`, `end_repeat`);
- **seleção de entidades** (`select_one_from_file`, `select_multiple_from_file`);
- **consulta de propriedades** (`instance()`);
- **criação/atualização de entidades** (`entities` sheet, `save_to`);
- listas de seleção;
- perguntas condicionais;
- cálculos automáticos;
- validações;
- obrigatoriedade de campos;
- preenchimentos automáticos;
- geolocalização;
- fotos;
- assinaturas;
- códigos de barras ou QR Codes;
- auditoria, quando aplicável.

### 3. Boas Práticas Obrigatórias

Sempre:
- utilizar nomes técnicos (`name`) padronizados em snake_case;
- criar labels claras e objetivas;
- adicionar dicas (`hint`) quando necessário;
- utilizar listas de seleção para valores controlados;
- aplicar restrições para evitar dados inválidos;
- evitar perguntas redundantes;
- aplicar relevância para ocultar perguntas desnecessárias;
- utilizar cálculos quando possível para reduzir digitação;
- **quando usar entidades, sempre adicionar `relevant` nos `calculate` de `instance()` para evitar erros antes da seleção.**

### 4. Otimização e Revisão

Antes da entrega:
- revisar integralmente o XLSForm;
- verificar coerência lógica;
- verificar fluxos condicionais;
- verificar constraints;
- verificar cálculos;
- verificar listas de escolha;
- verificar grupos e repetições;
- **verificar se as expressões `instance()` estão corretas (nome da lista, propriedades, escaping de ${})**;
- **verificar se a planilha `entities` e `save_to` estão consistentes**;
- identificar oportunidades de simplificação;
- corrigir automaticamente problemas encontrados.

### 5. Validação Obrigatória

Antes da entrega final:
1. Execute a skill `validar-formulario-odk`.
2. Corrija todos os erros identificados.
3. Execute novamente a validação até obter:
   - zero erros críticos;
   - zero erros de sintaxe;
   - zero inconsistências estruturais.

### 6. Formato da Entrega

A resposta final deve conter:

#### Resumo Executivo
- objetivo do formulário;
- principais seções;
- **listas de entidades utilizadas/criadas/atualizadas**;
- melhorias aplicadas;
- validações implementadas.

#### Relatório Técnico
- campos criados;
- grupos;
- repetições;
- cálculos;
- relevâncias;
- constraints;
- listas de escolha;
- **entidades anexadas (`select_one_from_file`, `csv-external`)**;
- **entidades criadas/atualizadas (`entities` sheet, `save_to`)**;
- **expressões `instance()` utilizadas**;
- **filtros (`choice_filter`, `create_if`, `update_if`)**.

#### Arquivo Final
Gerar e disponibilizar o formulário completo em formato:
- XLSForm (`.xlsx`)

O arquivo entregue deve estar pronto para importação no ODK Central sem necessidade de ajustes adicionais.

## Critério de Qualidade

Considere o formulário concluído apenas quando:
- estiver tecnicamente válido;
- seguir as melhores práticas do ODK;
- possuir excelente experiência de uso em campo;
- minimizar erros de coleta;
- **as expressões `instance()` estiverem testadas e corretas**;
- **as regras de `entities` sheet (`create_if`, `update_if`, `entity_id`) estiverem logicamente consistentes**;
- estiver validado pela skill `validar-formulario-odk`;
- puder ser implantado imediatamente em produção.

## Exemplos Completos

### Exemplo 1: Formulário que USA entidades (selecionar + consultar)

**Cenário:** Selecionar um agente de campo da lista `Agentes` e exibir seus dados.

**survey:**
| type | name | label | required | appearance | calculation | relevant |
|------|------|-------|----------|------------|-------------|----------|
| `select_one_from_file Agentes.csv` | `agente` | Selecione o agente | `yes` | `autocomplete` | | |
| `calculate` | `nome_agente` | | | | `instance("Agentes")/root/item[name=${agente}]/Nome` | `${agente} != ""` |
| `note` | `dados` | **Nome:** ${nome_agente} | | | | `${agente} != ""` |

### Exemplo 2: Formulário que CRIA entidades

**Cenário:** Cadastrar novas árvores na lista `arvores`.

**survey:**
| type | name | label | save_to |
|------|------|-------|---------|
| `geopoint` | `localizacao` | Localização | `geometry` |
| `text` | `especie` | Espécie | `especie` |
| `integer` | `dap` | DAP (cm) | `dap` |

**entities:**
| list_name | label |
|-----------|-------|
| `arvores` | `concat(${especie}, " - DAP: ", ${dap})` |

### Exemplo 3: Formulário que ATUALIZA entidades

**Cenário:** Atualizar o DAP de uma árvore existente.

**survey:**
| type | name | label | save_to |
|------|------|-------|---------|
| `select_one_from_file arvores.csv` | `arvore` | Selecione a árvore | |
| `note` | `dados_atuais` | DAP atual: ${dap_atual} | |
| `integer` | `novo_dap` | Novo DAP (cm) | `dap` |

**entities:**
| list_name | entity_id |
|-----------|-----------|
| `arvores` | `${arvore}` |
