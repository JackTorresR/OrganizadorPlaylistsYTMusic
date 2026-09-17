import json
import os

from dotenv import load_dotenv
from ytmusicapi import YTMusic


CONFIG_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

BASE_DIR = os.path.dirname(
    CONFIG_DIR
)

load_dotenv(
    os.path.join(
        CONFIG_DIR,
        ".env"
    )
)


# ============================================================
# PLAYLIST
# ============================================================

PLAYLIST_ID = "PLREPTQ1EhZn6_iUgoqksUdfVKUI1-cKa3"


# ============================================================
# ORGANIZAÇÃO
# ============================================================

ORDEM_ALBUM = "ASC"
ORDEM_MUSICA = "ASC"
ORDEM_ARTISTA = "ASC"

TAMANHO_LOTE = 50
CRIAR_BACKUP = True
PAUSA_ENTRE_LOTES = 1.0
PEDIR_CONFIRMACAO = True
IGNORAR_MAIUSCULAS = True


# ============================================================
# PASTAS
# ============================================================

PASTA_SCRIPTS = os.path.join(
    BASE_DIR,
    "Scripts"
)

PASTA_BACKUP = os.path.join(
    PASTA_SCRIPTS,
    "Backups"
)

PASTA_RESULTADO = os.path.join(
    PASTA_SCRIPTS,
    "Resultado"
)


# ============================================================
# AUTENTICAÇÃO
# ============================================================

AUTH_FILE = os.path.join(
    CONFIG_DIR,
    "browser.json"
)

YTMUSIC_AUTHORIZATION = os.getenv(
    "YTMUSIC_AUTHORIZATION"
)

YTMUSIC_COOKIE = os.getenv(
    "YTMUSIC_COOKIE"
)

YTMUSIC_X_GOOG_VISITOR_ID = os.getenv(
    "YTMUSIC_X_GOOG_VISITOR_ID"
)


def carregar_browser_auth():
    if not os.path.exists(AUTH_FILE):
        raise FileNotFoundError(
            f"Arquivo não encontrado: {AUTH_FILE}"
        )

    if not YTMUSIC_AUTHORIZATION:
        raise ValueError(
            "YTMUSIC_AUTHORIZATION não foi "
            "encontrado no arquivo .env."
        )

    if not YTMUSIC_COOKIE:
        raise ValueError(
            "YTMUSIC_COOKIE não foi "
            "encontrado no arquivo .env."
        )

    if not YTMUSIC_X_GOOG_VISITOR_ID:
        raise ValueError(
            "YTMUSIC_X_GOOG_VISITOR_ID não foi "
            "encontrado no arquivo .env."
        )

    with open(
        AUTH_FILE,
        "r",
        encoding="utf-8"
    ) as arquivo:

        headers = json.load(
            arquivo
        )

    headers["Authorization"] = (
        YTMUSIC_AUTHORIZATION
    )

    headers["Cookie"] = (
        YTMUSIC_COOKIE
    )

    headers["x-goog-visitor-id"] = (
        YTMUSIC_X_GOOG_VISITOR_ID
    )

    return headers


def criar_ytmusic():
    headers = carregar_browser_auth()

    return YTMusic(
        headers
    )


# ============================================================
# ARQUIVOS GERADOS
# ============================================================

ARQUIVO_ORDEM_CALCULADA = os.path.join(
    PASTA_RESULTADO,
    "ordem_calculada.json"
)

ARQUIVO_PROGRESSO = os.path.join(
    PASTA_RESULTADO,
    "progresso.json"
)

ARQUIVO_RELATORIO = os.path.join(
    PASTA_RESULTADO,
    "relatorio_playlist.txt"
)