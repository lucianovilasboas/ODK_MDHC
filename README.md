# ODK MDHC — Envelhecer

Gerencia usuários e formulários do **ODK Central** para o programa **Envelhecer** (MDHC).

Servidor: `https://odk.lucianovilasboas.com.br`

## Estrutura

```
src/                          # Scripts Python
  odk_users.py                # Autentica e lista usuários da API
  odk.py                      # Stub para get_users_from_api()
  usuarios.xlsx               # Exportação manual de usuários (57)
formularios/                  # Formulários ODK (XLSForm e XForm)
  formulario_parte1.xlsx      # XLSForm editável
  formulario_parte2.xlsx      # XLSForm editável
  formulario_agentes.xlsx     # XLSForm com entidade Agentes
  formulario_intencao_voto.xlsx
  formulario_satisfacao_cantina.xlsx  # XLSForm com entidade Opcoes
  form_parte_1.xml            # XForm compilado (não editar)
  form_parte_2.xml            # XForm compilado (não editar)
  form_parte_intencao_voto.xml
  Agentes.csv                 # Dados da Entity List Agentes
  opcoes.csv                  # Dados da Entity List Opcoes
```

## Requisitos

- Python 3.12
- [`uv`](https://docs.astral.sh/uv/) (gerenciador de ambiente)

Instale as dependências:

```powershell
uv pip sync requirements.txt
```

## Uso

Listar usuários do ODK Central:

```powershell
.venv\Scripts\python src/odk_users.py
```

## Entity Lists

### Agentes

Propriedades: `Nome`, `email`, `Telefone`, `Bairro_Reside`, `Bairros`, `Realizou_Curso`, `Funcao`.

### Opcoes

Propriedades: `nome`.
