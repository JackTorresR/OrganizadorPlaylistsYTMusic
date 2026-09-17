import json
import os
import sys
import unicodedata

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from Configs import Config


ARQUIVO_INDICE = os.path.join(
    Config.PASTA_RESULTADO,
    "indice_playlist.json"
)


def normalizar_texto(texto):
    if texto is None:
        return ""

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

def carregar_playlist(yt):

    print("=" * 70)
    print(" BAIXANDO PLAYLIST")
    print("=" * 70)
    print()

    print("Aguarde...")

    print()

    try:

        playlist = yt.get_playlist(
            Config.PLAYLIST_ID,
            limit=None
        )

        return playlist

    except Exception as erro:

        print()
        print("ERRO AO LER A PLAYLIST:")
        print()
        print(erro)
        print()

        return None


def criar_indice(playlist):

    tracks = playlist.get("tracks") or []

    musicas = []

    for posicao, item in enumerate(
        tracks,
        start=1
    ):

        if not item:
            continue

        artistas = []

        for artista in (
            item.get("artists") or []
        ):

            nome = artista.get("name")

            if nome:
                artistas.append(
                    nome.strip()
                )

        album = item.get("album")

        if isinstance(album, dict):

            album_nome = album.get(
                "name"
            )

        else:

            album_nome = None

        musica = {

            "posicao": posicao,

            "titulo": item.get(
                "title",
                "Título desconhecido"
            ),

            "artista": " & ".join(
                artistas
            ) if artistas else
            "Artista desconhecido",

            "album": album_nome or
            "Álbum desconhecido",

            "videoId": item.get(
                "videoId"
            ),

            "setVideoId": item.get(
                "setVideoId"
            ),

            "isAvailable": item.get(
                "isAvailable"
            ),

            "videoType": item.get(
                "videoType"
            )
        }

        # Campos normalizados para busca rápida

        musica["_titulo_busca"] = (
            normalizar_texto(
                musica["titulo"]
            )
        )

        musica["_artista_busca"] = (
            normalizar_texto(
                musica["artista"]
            )
        )

        musica["_album_busca"] = (
            normalizar_texto(
                musica["album"]
            )
        )

        musicas.append(musica)

    return musicas


def salvar_indice(
    playlist,
    musicas
):

    os.makedirs(
        Config.PASTA_RESULTADO,
        exist_ok=True
    )

    dados = {

        "playlist_id":
            Config.PLAYLIST_ID,

        "playlist_title":
            playlist.get(
                "title",
                "Sem título"
            ),

        "total":
            len(musicas),

        "musicas":
            musicas
    }

    with open(
        ARQUIVO_INDICE,
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
    print("Índice salvo em:")
    print()
    print(
        f"    {ARQUIVO_INDICE}"
    )
    print()


def carregar_indice():

    if not os.path.exists(
        ARQUIVO_INDICE
    ):
        return None

    try:

        with open(
            ARQUIVO_INDICE,
            "r",
            encoding="utf-8"
        ) as arquivo:

            dados = json.load(
                arquivo
            )

        return dados

    except Exception as erro:

        print()
        print("ERRO AO CARREGAR ÍNDICE:")
        print()
        print(erro)
        print()

        return None


def buscar_musicas(
    musicas,
    termo
):

    termo_normalizado = normalizar_texto(
        termo
    )

    resultados = []

    for musica in musicas:

        encontrou = (

            termo_normalizado
            in musica["_titulo_busca"]

            or

            termo_normalizado
            in musica["_artista_busca"]

            or

            termo_normalizado
            in musica["_album_busca"]

        )

        if encontrou:

            resultados.append(
                musica
            )

    return resultados


def mostrar_resultados(
    resultados,
    termo
):

    print()
    print("=" * 70)
    print(" RESULTADOS")
    print("=" * 70)
    print()

    if not resultados:

        print(
            f'Nenhuma música encontrada para: "{termo}"'
        )

        print()

        return

    print(
        f'Busca: "{termo}"'
    )

    print(
        f"Encontradas: {len(resultados)}"
    )

    print()

    for musica in resultados:

        disponibilidade = ""

        if musica.get(
            "isAvailable"
        ) is False:

            disponibilidade = " [INDISPONÍVEL]"

        print(
            f"{musica['posicao']:04d}. "
            f"{musica['titulo']}"
            f"{disponibilidade}"
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
            f"{musica.get('videoId')}"
        )

        print()


def mostrar_musica(
    musica
):

    disponibilidade = ""

    if musica.get(
        "isAvailable"
    ) is False:

        disponibilidade = " [INDISPONÍVEL]"

    print(
        f"{musica['posicao']:04d}. "
        f"{musica['titulo']}"
        f"{disponibilidade}"
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
        f"{musica.get('videoId')}"
    )

    print()


def musicas_sao_iguais(
    musica_a,
    musica_b
):

    if musica_a is None or musica_b is None:
        return False

    video_id_a = musica_a.get(
        "videoId"
    )

    video_id_b = musica_b.get(
        "videoId"
    )

    if video_id_a and video_id_b:

        return video_id_a == video_id_b

    return (
        normalizar_texto(
            musica_a.get("titulo")
        )
        ==
        normalizar_texto(
            musica_b.get("titulo")
        )
        and
        normalizar_texto(
            musica_a.get("artista")
        )
        ==
        normalizar_texto(
            musica_b.get("artista")
        )
    )


def atualizar_indice(yt):

    playlist = carregar_playlist(
        yt
    )

    if playlist is None:
        return None

    musicas = criar_indice(
        playlist
    )

    salvar_indice(
        playlist,
        musicas
    )

    print(
        f"Total de músicas indexadas: "
        f"{len(musicas)}"
    )

    return {
        "playlist_id":
            Config.PLAYLIST_ID,

        "playlist_title":
            playlist.get(
                "title",
                "Sem título"
            ),

        "total":
            len(musicas),

        "musicas":
            musicas
    }


def remover_musica_por_posicao(
    yt,
    posicao,
    indice_anterior
):

    print()
    print("=" * 70)
    print(" ATUALIZANDO PLAYLIST ANTES DA REMOÇÃO")
    print("=" * 70)
    print()

    # ---------------------------------------------------------
    # GUARDA O QUE O ÍNDICE LOCAL DIZIA
    # ---------------------------------------------------------

    musicas_anteriores = (
        indice_anterior.get("musicas")
        or []
    )

    musica_anterior = None

    if (
        posicao >= 1
        and posicao <= len(musicas_anteriores)
    ):

        musica_anterior = (
            musicas_anteriores[posicao - 1]
        )

    # ---------------------------------------------------------
    # BAIXA A PLAYLIST ATUAL
    # ---------------------------------------------------------

    playlist = carregar_playlist(
        yt
    )

    if playlist is None:
        return None

    musicas_atualizadas = criar_indice(
        playlist
    )

    # ---------------------------------------------------------
    # ATUALIZA O JSON IMEDIATAMENTE
    # ---------------------------------------------------------

    salvar_indice(
        playlist,
        musicas_atualizadas
    )

    print(
        f"Total de músicas indexadas: "
        f"{len(musicas_atualizadas)}"
    )

    print()

    # ---------------------------------------------------------
    # VERIFICA SE A POSIÇÃO EXISTE
    # ---------------------------------------------------------

    if (
        posicao < 1
        or posicao > len(musicas_atualizadas)
    ):

        print("=" * 70)
        print(" POSIÇÃO INVÁLIDA")
        print("=" * 70)
        print()

        print(
            f"ERRO: a posição {posicao:04d} "
            f"não existe na playlist atual."
        )

        print(
            f"A playlist possui "
            f"{len(musicas_atualizadas)} música(s)."
        )

        print()

        return False

    # ---------------------------------------------------------
    # PEGA A MÚSICA ATUAL
    # ---------------------------------------------------------

    musica_atual = (
        musicas_atualizadas[posicao - 1]
    )

    # ---------------------------------------------------------
    # VERIFICA SE A MÚSICA MUDOU
    # ---------------------------------------------------------

    mudou = not musicas_sao_iguais(
        musica_anterior,
        musica_atual
    )

    if mudou and musica_anterior is not None:

        print("=" * 70)
        print(" ATENÇÃO: A POSIÇÃO MUDOU")
        print("=" * 70)
        print()

        print(
            f"A posição {posicao:04d} "
            "não corresponde mais à mesma música."
        )

        print()

        print("NO ÍNDICE ANTERIOR:")

        print()

        mostrar_musica(
            musica_anterior
        )

        print("NA PLAYLIST ATUAL:")

        print()

        mostrar_musica(
            musica_atual
        )

        print(
            "O índice foi atualizado com a "
            "playlist atual."
        )

        print()

        resposta = input(
            "Deseja remover a música que está "
            "AGORA nessa posição? [s/N]: "
        ).strip()

    else:

        print("=" * 70)
        print(" MÚSICA ENCONTRADA")
        print("=" * 70)
        print()

        mostrar_musica(
            musica_atual
        )

        resposta = input(
            "Confirmar remoção? [s/N]: "
        ).strip()

    # ---------------------------------------------------------
    # CONFIRMAÇÃO
    # ---------------------------------------------------------

    if normalizar_texto(
        resposta
    ) != "s":

        print()
        print("Remoção cancelada.")
        print()

        return False

    # ---------------------------------------------------------
    # DADOS PARA REMOÇÃO
    # ---------------------------------------------------------

    video_id = musica_atual.get(
        "videoId"
    )

    set_video_id = musica_atual.get(
        "setVideoId"
    )

    if not video_id:

        print()
        print(
            "ERRO: a música não possui videoId."
        )
        print()

        return False

    item_remover = {
        "videoId": video_id
    }

    if set_video_id:

        item_remover[
            "setVideoId"
        ] = set_video_id

    # ---------------------------------------------------------
    # REMOVE
    # ---------------------------------------------------------

    print()
    print("Removendo música...")
    print()

    try:

        yt.remove_playlist_items(
            Config.PLAYLIST_ID,
            videos=[item_remover]
        )

        print(
            "Música removida com sucesso."
        )

        print()

    except Exception as erro:

        print()
        print(
            "ERRO AO REMOVER A MÚSICA:"
        )
        print()
        print(erro)
        print()

        return False

    # ---------------------------------------------------------
    # ATUALIZA O ÍNDICE NOVAMENTE APÓS A REMOÇÃO
    # ---------------------------------------------------------

    print("=" * 70)
    print(" ATUALIZANDO ÍNDICE APÓS A REMOÇÃO")
    print("=" * 70)
    print()

    novo_indice = atualizar_indice(
        yt
    )

    if novo_indice is None:

        print()
        print(
            "A música foi removida, mas não foi possível "
            "atualizar o índice local."
        )

        print()

        return True

    print()
    print(
        "Índice atualizado com sucesso."
    )
    print()

    return True


def mostrar_menu():

    print()
    print("=" * 70)
    print(" BUSCAR MÚSICAS")
    print("=" * 70)
    print()

    print(
        "Digite parte do título, artista ou álbum."
    )

    print()

    print(
        "Exemplos:"
    )

    print(
        "  zezo"
    )

    print(
        "  mania"
    )

    print(
        "  bossa nova"
    )

    print(
        "  marcinho"
    )

    print()

    print(
        "Comandos:"
    )

    print(
        "  atualizar       -> baixa a playlist novamente"
    )

    print(
        "  remover 0094    -> atualiza e remove a posição 0094"
    )

    print(
        "  sair             -> encerra o programa"
    )

    print()


def main():

    print()
    print("=" * 70)
    print(" PESQUISADOR DE PLAYLIST - YOUTUBE MUSIC")
    print("=" * 70)
    print()

    indice = carregar_indice()

    yt = None

    # ---------------------------------------------------------
    # SE JÁ EXISTE ÍNDICE
    # ---------------------------------------------------------

    if indice:

        musicas = indice.get(
            "musicas"
        ) or []

        print(
            f"Índice encontrado: "
            f"{len(musicas)} música(s)"
        )

        print()

        print(
            "Não será necessário baixar "
            "a playlist novamente."
        )

        print()

    else:

        print(
            "Nenhum índice encontrado."
        )

        print(
            "Será necessário baixar "
            "a playlist uma vez."
        )

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

        indice = atualizar_indice(
            yt
        )

        if indice is None:
            return

        musicas = indice.get(
            "musicas"
        ) or []

    # ---------------------------------------------------------
    # LOOP DE BUSCA
    # ---------------------------------------------------------

    while True:

        mostrar_menu()

        termo = input(
            "Buscar: "
        ).strip()

        print()

        if not termo:
            continue

        comando = normalizar_texto(
            termo
        )

        # -----------------------------------------------------
        # SAIR
        # -----------------------------------------------------

        if comando == "sair":

            print(
                "Encerrando..."
            )

            break

        # -----------------------------------------------------
        # REMOVER POR POSIÇÃO
        # -----------------------------------------------------

        if comando.startswith(
            "remover "
        ):

            partes = comando.split()

            if len(partes) != 2:

                print()
                print(
                    "Uso correto: remover 0094"
                )
                print()

                continue

            try:

                posicao = int(
                    partes[1]
                )

            except ValueError:

                print()
                print(
                    "ERRO: a posição deve ser um número."
                )
                print()

                continue

            if yt is None:
                try:
                    yt = Config.criar_ytmusic()

                except Exception as erro:
                    print()
                    print("ERRO AO CARREGAR AUTENTICAÇÃO:")
                    print()
                    print(erro)
                    print()

                    continue

            resultado = remover_musica_por_posicao(
                yt,
                posicao,
                indice
            )

            # -------------------------------------------------
            # SEMPRE RECARREGA O ÍNDICE LOCAL
            # -------------------------------------------------

            indice_atualizado = (
                carregar_indice()
            )

            if indice_atualizado:

                indice = indice_atualizado

                musicas = (
                    indice.get(
                        "musicas"
                    )
                    or []
                )

            continue

        # -----------------------------------------------------
        # ATUALIZAR
        # -----------------------------------------------------

        if comando == "atualizar":

            print(
                "Atualizando índice..."
            )

            print()

            if yt is None:
                try:
                    yt = Config.criar_ytmusic()

                except Exception as erro:
                    print()
                    print("ERRO AO CARREGAR AUTENTICAÇÃO:")
                    print()
                    print(erro)
                    print()

                    continue

            novo_indice = atualizar_indice(
                yt
            )

            if novo_indice is not None:

                indice = novo_indice

                musicas = (
                    indice.get(
                        "musicas"
                    )
                    or []
                )

                print()
                print(
                    "Índice atualizado com sucesso."
                )

            continue

        # -----------------------------------------------------
        # BUSCA NORMAL
        # -----------------------------------------------------

        resultados = buscar_musicas(
            musicas,
            termo
        )

        mostrar_resultados(
            resultados,
            termo
        )


if __name__ == "__main__":
    main()