import os
import sys
import json
import time
import unicodedata
from collections import defaultdict

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from Configs import Config


# ============================================================
# UTILITÁRIOS
# ============================================================

def garantir_pastas():
    os.makedirs(
        Config.PASTA_RESULTADO,
        exist_ok=True
    )


def normalizar_texto(texto):
    if texto is None:
        return ""

    texto = str(texto).strip()

    if Config.IGNORAR_MAIUSCULAS:
        texto = texto.lower()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    return texto


def obter_artistas(item):
    artistas = item.get("artists") or []

    nomes = []

    for artista in artistas:
        nome = artista.get("name")

        if nome:
            nomes.append(
                nome.strip()
            )

    if not nomes:
        return ["Artista desconhecido"]

    return nomes


def obter_artista_principal(item):
    artistas = obter_artistas(item)

    return " & ".join(artistas)


def obter_album(item):
    album = item.get("album")

    if isinstance(album, dict):
        nome = album.get("name")

        if nome:
            return nome.strip()

    return "Álbum desconhecido"


def obter_titulo(item):
    titulo = item.get("title")

    if titulo:
        return titulo.strip()

    return "Título desconhecido"


def obter_set_video_id(item):
    return item.get("setVideoId")


def obter_video_id(item):
    return item.get("videoId")


# ============================================================
# PLAYLIST
# ============================================================

def carregar_playlist(yt):
    print("=" * 70)
    print(" LENDO PLAYLIST")
    print("=" * 70)
    print()

    print(
        f"Playlist ID: {Config.PLAYLIST_ID}"
    )

    print()

    try:
        playlist = yt.get_playlist(
            Config.PLAYLIST_ID,
            limit=None
        )

    except Exception as erro:
        print(
            "ERRO AO LER A PLAYLIST:"
        )

        print()
        print(erro)
        print()

        return None

    return playlist


def preparar_musicas(playlist):
    itens = playlist.get("tracks") or []

    musicas = []

    for indice, item in enumerate(itens):
        if not item:
            continue

        musica = {
            "posicao_atual": indice + 1,

            "titulo": obter_titulo(item),

            "album": obter_album(item),

            "artista": obter_artista_principal(item),

            "artistas": obter_artistas(item),

            "videoId": obter_video_id(item),

            "setVideoId": obter_set_video_id(item),

            "duration": item.get("duration"),

            "duration_seconds": item.get(
                "duration_seconds"
            )
        }

        musicas.append(musica)

    return musicas


# ============================================================
# ORDENAÇÃO
# ============================================================

def chave_ordenacao(musica):
    artista = normalizar_texto(
        musica["artista"]
    )

    album = normalizar_texto(
        musica["album"]
    )

    titulo = normalizar_texto(
        musica["titulo"]
    )

    return (
        artista,
        album,
        titulo
    )


def ordenar_musicas(musicas):
    reverse_artista = (
        Config.ORDEM_ARTISTA.upper() == "DESC"
    )

    reverse_album = (
        Config.ORDEM_ALBUM.upper() == "DESC"
    )

    reverse_musica = (
        Config.ORDEM_MUSICA.upper() == "DESC"
    )

    resultado = list(musicas)

    resultado.sort(
        key=lambda musica:
            normalizar_texto(
                musica["titulo"]
            ),
        reverse=reverse_musica
    )

    resultado.sort(
        key=lambda musica:
            normalizar_texto(
                musica["album"]
            ),
        reverse=reverse_album
    )

    resultado.sort(
        key=lambda musica:
            normalizar_texto(
                musica["artista"]
            ),
        reverse=reverse_artista
    )

    return resultado


# ============================================================
# AGRUPAMENTO / RELATÓRIO
# ============================================================

def agrupar_por_artista(musicas):
    grupos = defaultdict(list)

    for musica in musicas:
        grupos[
            musica["artista"]
        ].append(musica)

    return dict(
        sorted(
            grupos.items(),
            key=lambda item:
                normalizar_texto(item[0])
        )
    )


def mostrar_estatisticas(musicas):
    artistas = set()
    albuns = set()

    for musica in musicas:
        artistas.add(
            musica["artista"]
        )

        albuns.add(
            (
                musica["artista"],
                musica["album"]
            )
        )

    print("=" * 70)
    print(" ESTATÍSTICAS")
    print("=" * 70)
    print()

    print(
        f"Total de músicas : {len(musicas)}"
    )

    print(
        f"Artistas         : {len(artistas)}"
    )

    print(
        f"Álbuns           : {len(albuns)}"
    )

    print()


def mostrar_artistas(musicas):
    grupos = agrupar_por_artista(
        musicas
    )

    print("=" * 70)
    print(" ARTISTAS ENCONTRADOS")
    print("=" * 70)
    print()

    for numero, (artista, lista) in enumerate(
        grupos.items(),
        start=1
    ):
        print(
            f"{numero:03d}. {artista} "
            f"({len(lista)} música(s))"
        )

    print()

    print(
        f"Total: {len(grupos)} artistas"
    )

    print()


def gerar_relatorio(musicas):
    grupos = agrupar_por_artista(
        musicas
    )

    linhas = []

    linhas.append(
        "=" * 70
    )

    linhas.append(
        " RELATÓRIO DA PLAYLIST"
    )

    linhas.append(
        "=" * 70
    )

    linhas.append("")

    linhas.append(
        f"Total de músicas: {len(musicas)}"
    )

    linhas.append(
        f"Total de artistas: {len(grupos)}"
    )

    linhas.append("")

    for artista, lista in grupos.items():
        linhas.append(
            "-" * 70
        )

        linhas.append(
            f"{artista} ({len(lista)} música(s))"
        )

        linhas.append(
            "-" * 70
        )

        albuns = defaultdict(list)

        for musica in lista:
            albuns[
                musica["album"]
            ].append(musica)

        albuns_ordenados = sorted(
            albuns.items(),
            key=lambda item:
                normalizar_texto(item[0])
        )

        for album, musicas_album in albuns_ordenados:
            linhas.append(
                f"  [{album}]"
            )

            musicas_album = sorted(
                musicas_album,
                key=lambda musica:
                    normalizar_texto(
                        musica["titulo"]
                    )
            )

            for musica in musicas_album:
                linhas.append(
                    f"      - {musica['titulo']}"
                )

        linhas.append("")

    with open(
        Config.ARQUIVO_RELATORIO,
        "w",
        encoding="utf-8"
    ) as arquivo:
        arquivo.write(
            "\n".join(linhas)
        )

    print(
        "Relatório salvo em: "
        f"{Config.ARQUIVO_RELATORIO}"
    )


# ============================================================
# ORDEM CALCULADA
# ============================================================

def salvar_ordem_calculada(musicas):
    dados = {
        "playlist_id": Config.PLAYLIST_ID,

        "gerado_em": time.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "ordem_artista": Config.ORDEM_ARTISTA,

        "ordem_album": Config.ORDEM_ALBUM,

        "ordem_musica": Config.ORDEM_MUSICA,

        "total": len(musicas),

        "musicas": []
    }

    for indice, musica in enumerate(
        musicas,
        start=1
    ):
        dados["musicas"].append(
            {
                "nova_posicao": indice,

                "artista": musica["artista"],

                "album": musica["album"],

                "titulo": musica["titulo"],

                "videoId": musica["videoId"],

                "setVideoId": musica["setVideoId"]
            }
        )

    with open(
        Config.ARQUIVO_ORDEM_CALCULADA,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    print()
    print(
        "Ordem calculada salva em:"
    )

    print(
        f"    {Config.ARQUIVO_ORDEM_CALCULADA}"
    )

    print()


# ============================================================
# PREVIEW
# ============================================================

def verificar_ordem(
    musicas_atuais,
    musicas_novas
):
    if len(musicas_atuais) != len(
        musicas_novas
    ):
        return False

    for atual, nova in zip(
        musicas_atuais,
        musicas_novas
    ):
        if (
            atual["setVideoId"]
            != nova["setVideoId"]
        ):
            return False

    return True


def mostrar_preview(
    musicas_atuais,
    musicas_novas
):
    print()
    print("=" * 70)
    print(" PRÉVIA DA NOVA ORDEM")
    print("=" * 70)
    print()

    if verificar_ordem(
        musicas_atuais,
        musicas_novas
    ):
        print(
            "A playlist já está na ordem desejada."
        )

        print()

        return True

    quantidade = min(
        len(musicas_atuais),
        len(musicas_novas)
    )

    alteracoes = []

    for i in range(quantidade):
        atual = musicas_atuais[i]
        nova = musicas_novas[i]

        if (
            atual["setVideoId"]
            != nova["setVideoId"]
        ):
            alteracoes.append(
                (
                    i + 1,
                    atual,
                    nova
                )
            )

    for numero, atual, nova in alteracoes[:30]:
        print(
            f"{numero:04d}."
        )

        print(
            "    ATUAL: "
            f"{atual['artista']} - "
            f"{atual['album']} - "
            f"{atual['titulo']}"
        )

        print(
            "    NOVA : "
            f"{nova['artista']} - "
            f"{nova['album']} - "
            f"{nova['titulo']}"
        )

        print()

    restantes = len(alteracoes) - 30

    if restantes > 0:
        print(
            f"... e mais {restantes} alteração(ões)."
        )

    print(
        f"Alterações necessárias: "
        f"{len(alteracoes)}"
    )

    print()

    return False


# ============================================================
# ANÁLISE COMPLETA
# ============================================================

def analisar_playlist(yt):
    garantir_pastas()

    playlist = carregar_playlist(
        yt
    )

    if playlist is None:
        return None

    musicas = preparar_musicas(
        playlist
    )

    if not musicas:
        print(
            "Nenhuma música encontrada "
            "na playlist."
        )

        return None

    print(
        f"Playlist encontrada: "
        f"{playlist.get('title', 'Sem título')}"
    )

    print()

    mostrar_estatisticas(
        musicas
    )

    mostrar_artistas(
        musicas
    )

    musicas_ordenadas = ordenar_musicas(
        musicas
    )

    salvar_ordem_calculada(
        musicas_ordenadas
    )

    gerar_relatorio(
        musicas_ordenadas
    )

    ordem_correta = mostrar_preview(
        musicas,
        musicas_ordenadas
    )

    return {
        "musicas": musicas,
        "playlist": playlist,
        "ordem_correta": ordem_correta,
        "musicas_ordenadas": musicas_ordenadas
    }


# ============================================================
# MAIN
# ============================================================

def main():
    print()
    print("=" * 70)
    print(" ANALISADOR DE PLAYLIST - YOUTUBE MUSIC")
    print("=" * 70)
    print()

    print("Playlist:")
    print(
        Config.PLAYLIST_ID
    )

    print()

    print(
        f"Ordem artista: "
        f"{Config.ORDEM_ARTISTA}"
    )

    print(
        f"Ordem álbum:   "
        f"{Config.ORDEM_ALBUM}"
    )

    print(
        f"Ordem música:  "
        f"{Config.ORDEM_MUSICA}"
    )

    print()

    try:
        print()
        print("=" * 70)
        print(" CONECTANDO AO YOUTUBE MUSIC")
        print("=" * 70)
        print()

        yt = Config.criar_ytmusic()
        print("Autenticação carregada com sucesso.")
        print()

    except Exception as erro:
        print()
        print("ERRO AO CARREGAR AUTENTICAÇÃO:")
        print()
        print(erro)
        print()
        return

    resultado = analisar_playlist(yt)

    if resultado is None:
        return

    print("=" * 70)
    print(" ANÁLISE CONCLUÍDA")
    print("=" * 70)
    print()

    print(
        "Nenhuma alteração foi feita "
        "na playlist."
    )

    print()

    print(
        "Arquivos gerados:"
    )

    print(
        f"    {Config.ARQUIVO_ORDEM_CALCULADA}"
    )

    print(
        f"    {Config.ARQUIVO_RELATORIO}"
    )

    print()


if __name__ == "__main__":
    main()