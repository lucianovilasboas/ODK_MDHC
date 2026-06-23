# AGENTS.md — Envelhecer / ODK Central

## Repo
Gerencia usuários e formulários ODK Central para o programa Envelhecer.
API v1: `https://odk.lucianovilasboas.com.br/v1`

## Scripts em `src/`
- `odk_users.py` — autentica (`POST /v1/sessions`) e lista (`GET /v1/users`) usuários.
  Executar: `.venv\Scripts\python src/odk_users.py`
- `odk.py` — stub. `get_users_from_api()` é chamado na linha 12 (top-level).
- `usuarios.xlsx` — exportado manualmente (57 usuários, colunas: displayName, email).

## Credenciais (⚠️ não commitar)
Email/senha hardcoded em `src/odk_users.py:13-14`.

## Ambiente
- Python 3.12 gerenciado por `uv`
- Dependências em `requirements.txt`: `requests`, `pyxform`, `pandas`, `openpyxl`, `pytest`
- Sincronizar: `uv pip sync requirements.txt`
- **Sempre usar** `.venv\Scripts\python` para executar código

## Formulários ODK
- **Editar:** `formularios/formulario_parte1.xlsx`, `formulario_parte2.xlsx` e `formulario_agentes.xlsx`
- **Compilados (não editar):** `formularios/form_parte_1.xml` e `form_parte_2.xml`
- Skills disponíveis:
  - `validar-formulario-odk` — revisar/validar formulários existentes
  - `criar-formulario-odk` — criar novos formulários a partir de descrição textual
  - `criar-formulario-odk-entidades` — criar formulários que usam, criam ou atualizam entidades

## Entity List: Agentes

O formulário `form_agentes` usa a Entity List `Agentes`. Para criar esta lista no Central:

1. Acesse o Central > Projeto > Entity Lists > New
2. Nome: `Agentes`
3. Aba Properties > New, adicione estas propriedades:
   - `Nome` (text)
   - `email` (text) — ⚠️ renomear de `e-mail` no CSV
   - `Telefone` (text)
   - `Bairro_Reside` (text)
   - `Bairros` (text)
   - `Realizou_Curso` (text)
   - `Funcao` (text)
4. Aba Entities > Upload, faça upload de `UFMS/Agentes.csv` (convertido: coluna `e-mail` renomeada para `email`)

## Entity List: Opcoes

O formulário `form_satisfacao_cantina` usa a Entity List `Opcoes`. Para criar:

1. Central > Projeto > Entity Lists > New > Nome: `Opcoes`
2. Aba Properties > New, adicione:
   - `nome` (text)
3. Aba Entities > Upload, faça upload de `formularios/opcoes.csv`

## MCP / Documentação ODK
- `odk-docs` em `opencode.jsonc` e `.vscode/mcp.json` (fonte: `https://odk-docs.mcp.kapa.ai`)
- `WebFetch` autorizado para `docs.getodk.org` (`.claude/settings.local.json`)
- Preferir estes canais para consultar API ODK.

## Estilo
- Código, comentários e commits em **português brasileiro**
- Docstrings em português

## `.gitignore`
`tutorial/`, `.venv/`, `UFMS/`

## Testes
- `pytest` instalado; até o momento não há testes no projeto.
- Executar: `.venv\Scripts\pytest`
