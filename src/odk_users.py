"""Lista os usuários de uma instância do ODK Central.

Fluxo da API (ODK Central v1):
1. POST /v1/sessions  -> autentica com email/senha e devolve um token de sessão.
2. GET  /v1/users     -> lista todos os usuários (requer Authorization: Bearer <token>).
"""

import requests

ODK_URL_BASE = "https://odk.lucianovilasboas.com.br/v1"
# ODK_URL_BASE = "https://odk.verifica.fun/v1"

ODK_EMAIL = "lucianovilasboas@gmail.com"
ODK_PASSWORD = "9419131773"


def autenticar(url_base=ODK_URL_BASE, email=ODK_EMAIL, password=ODK_PASSWORD):
    """Autentica no ODK Central e retorna o token de sessão (Bearer)."""
    resp = requests.post(
        f"{url_base}/sessions",
        json={"email": email, "password": password},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["token"]


def listar_usuarios(url_base=ODK_URL_BASE, email=ODK_EMAIL, password=ODK_PASSWORD):
    """Lista todos os usuários da instância do ODK Central.

    Retorna uma lista de dicionários, cada um representando um usuário com
    campos como id, displayName, email, createdAt, lastLoginAt, etc.
    """
    token = autenticar(url_base, email, password)
    resp = requests.get(
        f"{url_base}/users",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    usuarios = listar_usuarios()
    print(f"Total de usuários: {len(usuarios)}\n")
    for u in usuarios:
        print(f"  [{u['id']}] {u.get('displayName', '-')} <{u['email']}> "
              f"| último login: {u.get('lastLoginAt') or 'nunca'}")
