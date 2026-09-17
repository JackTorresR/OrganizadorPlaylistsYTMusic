import os
import sys
import json
import time


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


from Configs import Config


ARQUIVO_RESULTADO = os.path.join(
    Config.PASTA_RESULTADO,
    "musicas_quebradas.json"
)


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
        print()
        print(erro)
        print()
        return None


def verificar_musica(yt, item, posicao):
    video_id = item.get("videoId")

    resultado = {
        "posicao": posicao,
        "titulo": item.get(
            "title",
            "Título desconhecido"
        ),
        "artistas": [
            artista.get("name")

            for artista in (
                item.get("artists") or []
            )

            if artista.get("name")
        ],

        "album": (
            item.get("album", {}).get("name")

            if isinstance(
                item.get("album"),
                dict
            )
            else None
        ),
        "motivo": None,
        "videoId": video_id,
        "isAvailable_song": None,
        "playabilityStatus": None,
        "videoType": item.get("videoType"),
        "setVideoId": item.get("setVideoId"),
        "isAvailable_playlist": item.get("isAvailable"),
    }

    # ---------------------------------------------------------
    # SEM VIDEO ID
    # ---------------------------------------------------------

    if not video_id:
        resultado["motivo"] = ("SEM_VIDEO_ID")

        return resultado

    # ---------------------------------------------------------
    # DISPONIBILIDADE INFORMADA PELA PLAYLIST
    # ---------------------------------------------------------

    if item.get("isAvailable") is False:
        resultado["motivo"] = (
            "PLAYLIST_MARCOU_INDISPONIVEL"
        )

    # ---------------------------------------------------------
    # CONSULTA DIRETA DO VIDEO
    # ---------------------------------------------------------

    try:
        musica = yt.get_song(video_id)

        playability = (
            musica.get(
                "playabilityStatus"
            )
            or {}
        )
        status = playability.get("status")
        resultado["playabilityStatus"] = (status)

        if status:
            if status.upper() != "OK":
                resultado["isAvailable_song"] = False

                if not resultado["motivo"]:
                    resultado["motivo"] = (
                        "PLAYABILITY_STATUS_"
                        + status
                    )

            else:
                resultado["isAvailable_song"] = True

        # Alguns resultados possuem
        # isAvailable diretamente no objeto retornado.

        if musica.get("isAvailable") is False:
            resultado["isAvailable_song"] = False

            if not resultado["motivo"]:
                resultado["motivo"] = (
                    "GET_SONG_MARCOU_INDISPONIVEL"
                )

    except Exception as erro:
        resultado["erro"] = str(erro)
        resultado["isAvailable_song"] = False
        resultado["motivo"] = ("ERRO_AO_CONSULTAR_VIDEO")

    return resultado


def analisar_playlist(yt, playlist):
    tracks = playlist.get(
        "tracks"
    ) or []

    resultados = []
    print(
        f"Total de itens encontrados: "
        f"{len(tracks)}"
    )
    print()
    print("=" * 70)
    print(" VERIFICANDO MÚSICAS")
    print("=" * 70)
    print()

    for posicao, item in enumerate(
        tracks,
        start=1
    ):
        resultado = verificar_musica(
            yt,
            item,
            posicao
        )

        quebrada = (
            resultado.get("motivo")
            is not None
        )

        if quebrada:
            resultados.append(
                resultado
            )

            print(
                f"[PROBLEMA] {posicao:04d} - "
                f"{resultado['titulo']}"
            )

            if resultado.get("artistas"):
                print(
                    "           Artista: "
                    + ", ".join(
                        resultado["artistas"]
                    )
                )
            print(
                "           Motivo: "
                + str(
                    resultado["motivo"]
                )
            )
            print(
                "           videoId: "
                + str(
                    resultado["videoId"]
                )
            )
            print()

        else:
            print(
                f"[OK] {posicao:04d} - "
                f"{resultado['titulo']}"
            )

    return resultados


def salvar_resultado(
    playlist,
    problemas
):
    os.makedirs(
        Config.PASTA_RESULTADO,
        exist_ok=True
    )

    dados = {
        "playlist_id":
            Config.PLAYLIST_ID,
        "playlist_title":
            playlist.get("title"),
        "verificado_em":
            time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        "total_problemas":
            len(problemas),
        "musicas":
            problemas
    }

    with open(
        ARQUIVO_RESULTADO,
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
        "Resultado salvo em:"
    )
    print(
        f"    {ARQUIVO_RESULTADO}"
    )
    print()


def mostrar_resumo(problemas):
    print()
    print("=" * 70)
    print(" RESUMO")
    print("=" * 70)
    print()
    print(
        f"Músicas com problema: "
        f"{len(problemas)}"
    )
    print()

    if not problemas:
        print(
            "Nenhuma música quebrada foi encontrada."
        )
        print()
        return

    for musica in problemas:
        artistas = ", ".join(
            musica.get(
                "artistas"
            ) or []
        )
        print(
            f"{musica['posicao']:04d}. "
            f"{musica['titulo']}"
        )
        print(
            f"      Artista: {artistas}"
        )
        print(
            f"      Álbum: "
            f"{musica.get('album')}"
        )
        print(
            f"      videoId: "
            f"{musica.get('videoId')}"
        )
        print(
            f"      videoType: "
            f"{musica.get('videoType')}"
        )
        print(
            f"      isAvailable playlist: "
            f"{musica.get('isAvailable_playlist')}"
        )
        print(
            f"      isAvailable song: "
            f"{musica.get('isAvailable_song')}"
        )
        print(
            f"      playabilityStatus: "
            f"{musica.get('playabilityStatus')}"
        )
        print(
            f"      Motivo: "
            f"{musica.get('motivo')}"
        )
        print()


def main():
    print()
    print("=" * 70)
    print(" VERIFICADOR DE MÚSICAS QUEBRADAS")
    print("=" * 70)
    print()
    print("ATENÇÃO: este script NÃO remove nem altera")
    print("nenhuma música da playlist.")
    print()

    try:
        yt = Config.criar_ytmusic()

    except Exception as erro:
        print()
        print("ERRO AO CARREGAR AUTENTICAÇÃO:")
        print()
        print(erro)
        print()
        return

    playlist = carregar_playlist(
        yt
    )

    if playlist is None:
        return

    problemas = analisar_playlist(
        yt,
        playlist
    )
    salvar_resultado(playlist, problemas)
    mostrar_resumo(problemas)
    print()
    print("=" * 70)
    print(" CONCLUÍDO")
    print("=" * 70)
    print()


if __name__ == "__main__":

    main()