import os

import sys

import time

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:

    sys.path.insert(0, BASE_DIR)

from Configs import Config


def carregar_playlist(yt):
    print("=" * 70)
    print(" LENDO PLAYLIST")
    print("=" * 70)
    print()

    try:
        playlist = yt.get_playlist(
            Config.PLAYLIST_ID,
            limit=None
        )

        return playlist

    except Exception as erro:
        print("ERRO AO LER A PLAYLIST:")
        print(erro)
        print()

        return None


def normalizar_texto(texto):
    if not texto:

        return ""

    import unicodedata

    texto = str(texto).strip().lower()
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


def encontrar_duplicadas(playlist):
    unicas = []
    vistas = {}
    duplicadas = []
    tracks = playlist.get("tracks") or []

    for posicao, item in enumerate(
        tracks,
        start=1
    ):
        video_id = item.get("videoId")

        if not video_id:
            continue

        titulo = item.get(
            "title",
            "Título desconhecido"
        )

        artistas = []

        for artista in (
            item.get("artists") or []
        ):
            nome = artista.get("name")

            if nome:
                artistas.append(
                    nome.strip()
                )

        artista = " & ".join(
            artistas
        ) if artistas else "Artista desconhecido"

        album = item.get("album")

        if isinstance(album, dict):
            album_nome = album.get(
                "name"
            )

        else:
            album_nome = None

        musica = {
            "posicao": posicao,
            "titulo": titulo,
            "artista": artista,
            "album": album_nome or
            "Álbum desconhecido",
            "videoId": video_id,
            "setVideoId": item.get(
                "setVideoId"
            )
        }

        chave = (
            normalizar_texto(artista),
            normalizar_texto(titulo)
        )

        if chave in vistas:
            musica["original"] = vistas[chave]
            duplicadas.append(
                musica
            )

        else:
            vistas[chave] = musica
            unicas.append(
                musica
            )

    return unicas, duplicadas


def mostrar_duplicadas(duplicadas):
    print()
    print("=" * 70)
    print(" DUPLICADAS ENCONTRADAS")
    print("=" * 70)
    print()

    if not duplicadas:
        print(
            "Nenhuma duplicada encontrada."
        )
        print()
        return

    for musica in duplicadas:
        original = musica.get("original")
        print(
            f"{musica['posicao']:04d}. "
            f"{musica['titulo']}"
        )
        print(
            f"      Artista: "
            f"{musica['artista']}"
        )
        print(
            f"      Álbum:   "
            f"{musica['album']}"
        )
        print(
            f"      videoId: "
            f"{musica['videoId']}"
        )
        print("      → REMOVER")

        if original:
            print()
            print(
                f"{original['posicao']:04d}. "
                f"{original['titulo']}"
            )
            print(
                f"      Artista: "
                f"{original['artista']}"
            )
            print(
                f"      Álbum:   "
                f"{original['album']}"
            )
            print(
                f"      videoId: "
                f"{original['videoId']}"
            )
            print("      → MANTER")

        print()
        print("-" * 70)
        print()

    print(
        f"Total de duplicadas: "
        f"{len(duplicadas)}"
    )

    print()


def pedir_confirmacao(duplicadas):
    print("=" * 70)
    print(" ATENÇÃO")
    print("=" * 70)
    print()
    print(
        f"Serão removidas "
        f"{len(duplicadas)} música(s) duplicada(s)."
    )
    print()
    print(
        "A PRIMEIRA ocorrência de cada música será mantida."
    )
    print(
        "Somente as ocorrências posteriores serão removidas."
    )
    print()

    resposta = input(
        "Digite REMOVER para confirmar: "
    )
    print()

    return resposta.strip().upper() == "REMOVER"


def remover_duplicadas(yt, duplicadas):
    total = len(duplicadas)

    if total == 0:
        return True

    print("=" * 70)
    print(" REMOVENDO DUPLICADAS")
    print("=" * 70)
    print()

    tamanho_lote = Config.TAMANHO_LOTE

    posicao = 0

    while posicao < total:
        fim = min(
            posicao + tamanho_lote,
            total
        )

        lote = duplicadas[
            posicao:fim
        ]

        print(
            f"[{posicao + 1}/{total} - "
            f"{fim}/{total}] "
            f"Removendo lote com "
            f"{len(lote)} música(s)..."
        )

        itens = []

        for musica in lote:
            if not musica["videoId"]:
                continue

            item = {
                "videoId": musica["videoId"]
            }

            if musica.get("setVideoId"):
                item["setVideoId"] = (
                    musica["setVideoId"]
                )

            itens.append(item)

        try:
            if itens:
                yt.remove_playlist_items(
                    Config.PLAYLIST_ID,
                    videos=itens
                )

            posicao = fim

            print(
                f"    OK - até "
                f"{posicao}/{total}"
            )
            print()
            time.sleep(
                Config.PAUSA_ENTRE_LOTES
            )

        except Exception as erro:
            print()
            print("ERRO AO REMOVER LOTE:")
            print()
            print(erro)
            print()
            return False
        
    print(
        "Todas as duplicadas foram removidas."
    )
    print()

    return True


def main():
    print()
    print("=" * 70)
    print(" REMOVER DUPLICADAS - YOUTUBE MUSIC")
    print("=" * 70)
    print()
    print("Playlist:")
    print(Config.PLAYLIST_ID)
    print()

    try:
        yt = Config.criar_ytmusic()

    except Exception as erro:
        print()
        print(
            "ERRO AO CARREGAR AUTENTICAÇÃO:"
        )
        print()
        print(erro)
        print()

        return

    playlist = carregar_playlist(
        yt
    )

    if playlist is None:
        return

    tracks = playlist.get(
        "tracks"
    ) or []
    print(
        f"Playlist: "
        f"{playlist.get('title', 'Sem título')}"
    )
    print(
        f"Total de itens: {len(tracks)}"
    )
    print()

    unicas, duplicadas = (
        encontrar_duplicadas(
            playlist
        )
    )
    print(
        f"Músicas únicas: {len(unicas)}"
    )
    print(
        f"Duplicadas:     {len(duplicadas)}"
    )

    mostrar_duplicadas(
        duplicadas
    )

    if not duplicadas:
        print("=" * 70)
        print(" NADA A FAZER")
        print("=" * 70)
        print()

        return

    if not pedir_confirmacao(
        duplicadas
    ):
        print(
            "Operação cancelada."
        )

        print()

        return

    sucesso = remover_duplicadas(
        yt,
        duplicadas
    )

    print()

    if sucesso:
        print("=" * 70)
        print(" CONCLUÍDO")
        print("=" * 70)
        print()
        print(
            f"{len(duplicadas)} "
            f"duplicada(s) removida(s)."
        )

        print(
            f"{len(unicas)} "
            f"música(s) original(is) mantida(s)."
        )

    else:
        print("=" * 70)
        print(" EXECUÇÃO INTERROMPIDA")
        print("=" * 70)
        print()
        print(
            "Algumas duplicadas podem ter "
            "sido removidas."
        )

    print()


if __name__ == "__main__":

    main()