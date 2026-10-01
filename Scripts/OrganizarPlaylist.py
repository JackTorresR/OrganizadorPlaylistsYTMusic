import json
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
from AnalisarPlaylist import (analisar_playlist)


# ============================================================
# PASTAS
# ============================================================

def garantir_pastas():
    os.makedirs(
        Config.PASTA_RESULTADO,
        exist_ok=True
    )

    os.makedirs(
        Config.PASTA_BACKUP,
        exist_ok=True
    )


# ============================================================
# BACKUP
# ============================================================

def criar_backup(musicas):
    if not Config.CRIAR_BACKUP:
        return None

    timestamp = time.strftime(
        "%Y%m%d_%H%M%S"
    )

    caminho = os.path.join(
        Config.PASTA_BACKUP,
        f"backup_{timestamp}.json"
    )

    dados = {
        "playlist_id": Config.PLAYLIST_ID,

        "criado_em": time.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "total": len(musicas),

        "musicas": musicas
    }

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    print(
        f"Backup salvo em: {caminho}"
    )

    return caminho


# ============================================================
# PROGRESSO
# ============================================================

def salvar_progresso(
    fase,
    ultima_posicao,
    total,
    status="EM_EXECUCAO"
):
    dados = {
        "playlist_id": Config.PLAYLIST_ID,

        "fase": fase,

        "ultima_posicao_concluida":
            ultima_posicao,

        "proxima_posicao":
            ultima_posicao + 1,

        "total": total,

        "status": status,

        "atualizado_em":
            time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    }

    with open(
        Config.ARQUIVO_PROGRESSO,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def carregar_progresso():
    if not os.path.exists(
        Config.ARQUIVO_PROGRESSO
    ):
        return None

    try:
        with open(
            Config.ARQUIVO_PROGRESSO,
            "r",
            encoding="utf-8"
        ) as arquivo:
            return json.load(arquivo)

    except Exception:
        return None


def limpar_progresso():
    if os.path.exists(
        Config.ARQUIVO_PROGRESSO
    ):
        os.remove(
            Config.ARQUIVO_PROGRESSO
        )


# ============================================================
# ORDEM CALCULADA
# ============================================================

def carregar_ordem_calculada():
    if not os.path.exists(
        Config.ARQUIVO_ORDEM_CALCULADA
    ):
        return None

    try:
        with open(
            Config.ARQUIVO_ORDEM_CALCULADA,
            "r",
            encoding="utf-8"
        ) as arquivo:
            dados = json.load(arquivo)

        return dados.get("musicas") or []

    except Exception as erro:
        print(
            "ERRO AO LER ORDEM CALCULADA:"
        )

        print(erro)

        return None


# ============================================================
# CONFIRMAÇÃO
# ============================================================

def pedir_confirmacao():
    print("=" * 70)
    print(" ATENÇÃO")
    print("=" * 70)
    print()

    print(
        "A próxima etapa irá:"
    )

    print(
        "1. Remover as músicas da playlist"
    )

    print(
        "2. Adicioná-las novamente na nova ordem"
    )

    print()

    print(
        "O backup da playlist original será salvo "
        "antes da alteração."
    )

    print()

    resposta = input(
        "Digite ORGANIZAR para confirmar: "
    )

    print()

    return (
        resposta.strip().upper()
        == "ORGANIZAR"
    )


# ============================================================
# REMOVER EM LOTES
# ============================================================

def remover_em_lotes(
    yt,
    musicas_originais,
    inicio
):
    total = len(
        musicas_originais
    )

    print()
    print("=" * 70)
    print(" REMOVENDO MÚSICAS EM LOTES")
    print("=" * 70)
    print()

    posicao = inicio

    while posicao < total:
        fim = min(
            posicao + Config.TAMANHO_LOTE,
            total
        )

        lote = musicas_originais[
            posicao:fim
        ]

        print(
            f"[{posicao + 1}/{total} - "
            f"{fim}/{total}] "
            f"Removendo lote com "
            f"{len(lote)} música(s)..."
        )

        videos = []

        for musica in lote:
            videos.append(
                {
                    "videoId":
                        musica["videoId"],

                    "setVideoId":
                        musica["setVideoId"]
                }
            )

        try:
            yt.remove_playlist_items(
                Config.PLAYLIST_ID,
                videos
            )

            posicao = fim

            salvar_progresso(
                fase="REMOVENDO",
                ultima_posicao=posicao,
                total=total
            )

            print(
                f"    OK - até posição {posicao}"
            )

            print()

            time.sleep(
                Config.PAUSA_ENTRE_LOTES
            )

        except Exception as erro:
            print()
            print(
                "ERRO AO REMOVER LOTE:"
            )

            print(erro)

            print()

            print(
                "O progresso foi salvo."
            )

            print(
                f"Última posição concluída: "
                f"{posicao}"
            )

            return False

    print(
        "Todas as músicas foram removidas."
    )

    print()

    return True


# ============================================================
# ADICIONAR EM LOTES
# ============================================================

def adicionar_em_lotes(
    yt,
    musicas_desejadas,
    inicio
):
    total = len(
        musicas_desejadas
    )

    print()
    print("=" * 70)
    print(" ADICIONANDO MÚSICAS EM LOTES")
    print("=" * 70)
    print()

    posicao = total - inicio

    while posicao > 0:

        inicio_lote = max(
            0,
            posicao - Config.TAMANHO_LOTE
        )

        lote = list(
            reversed(
                musicas_desejadas[
                    inicio_lote:posicao
                ]
            )
        )

        print(
            f"[{inicio_lote + 1}/{total} - "
            f"{posicao}/{total}] "
            f"Adicionando lote com "
            f"{len(lote)} música(s)..."
        )

        video_ids = []

        for musica in lote:
            video_id = musica.get(
                "videoId"
            )

            if video_id:
                video_ids.append(
                    video_id
                )

        try:
            if video_ids:
                yt.add_playlist_items(
                    Config.PLAYLIST_ID,
                    videoIds=video_ids,
                    duplicates=False
                )

            posicao = inicio_lote

            salvar_progresso(
                fase="ADICIONANDO",
                ultima_posicao=total - posicao,
                total=total
            )

            print(
                f"    OK - até posição "
                f"{total - posicao}"
            )

            print()

            time.sleep(
                Config.PAUSA_ENTRE_LOTES
            )

        except Exception as erro:
            print()
            print(
                "ERRO AO ADICIONAR LOTE:"
            )
            print()

            print(erro)

            print()

            print(
                "O progresso foi salvo."
            )

            print(
                f"Última posição concluída: "
                f"{total - posicao}"
            )

            return False

    return True

# ============================================================
# REORGANIZAÇÃO
# ============================================================

def reorganizar_playlist(
    yt,
    musicas_originais,
    musicas_desejadas
):
    progresso = carregar_progresso()

    if progresso and progresso.get("status") == "CONCLUIDO":
        limpar_progresso()
        progresso = None

    total = len(
        musicas_desejadas
    )

    if progresso:
        fase = progresso.get(
            "fase"
        )

        ultima_posicao = progresso.get(
            "ultima_posicao_concluida",
            0
        )

        print()
        print("=" * 70)
        print(
            " CONTINUANDO EXECUÇÃO ANTERIOR"
        )
        print("=" * 70)
        print()

        print(
            f"Fase: {fase}"
        )

        print(
            f"Última posição concluída: "
            f"{ultima_posicao}"
        )

        print(
            f"Próxima posição: "
            f"{ultima_posicao + 1}"
        )

        print()

    else:
        fase = "REMOVENDO"

        ultima_posicao = 0

        salvar_progresso(
            fase=fase,
            ultima_posicao=0,
            total=total
        )

    if fase == "REMOVENDO":
        inicio = ultima_posicao

        sucesso = remover_em_lotes(
            yt,
            musicas_originais,
            inicio
        )

        if not sucesso:
            return False

        salvar_progresso(
            fase="ADICIONANDO",
            ultima_posicao=0,
            total=total
        )

        fase = "ADICIONANDO"

        ultima_posicao = 0

    if fase == "ADICIONANDO":
        inicio = ultima_posicao

        sucesso = adicionar_em_lotes(
            yt,
            musicas_desejadas,
            inicio
        )

        if not sucesso:
            return False

    salvar_progresso(
        fase="FINALIZADO",
        ultima_posicao=total,
        total=total,
        status="CONCLUIDO"
    )

    return True


# ============================================================
# EXECUÇÃO NORMAL
# ============================================================

def executar_organizacao(
    yt,
    musicas,
    musicas_ordenadas
):
    limpar_progresso()
    criar_backup(
        musicas
    )

    if Config.PEDIR_CONFIRMACAO:
        if not pedir_confirmacao():
            print(
                "Operação cancelada."
            )

            return False

    sucesso = reorganizar_playlist(
        yt,
        musicas,
        musicas_ordenadas
    )

    return sucesso


# ============================================================
# RETOMAR EXECUÇÃO
# ============================================================

def retomar_execucao(yt):
    progresso = carregar_progresso()

    if not progresso:
        return False

    if progresso.get("status") == "CONCLUIDO":
        return False

    print(
        "Foi encontrada uma execução "
        "incompleta."
    )

    print()

    musicas_salvas = (
        carregar_ordem_calculada()
    )

    if not musicas_salvas:
        print(
            "ERRO: não encontrei "
            "ordem_calculada.json."
        )

        print(
            "Não é possível continuar "
            "com segurança."
        )

        return True

    fase = progresso.get(
        "fase"
    )

    if fase == "REMOVENDO":
        print(
            "A execução estava na fase "
            "de remoção."
        )

        print()

        print(
            "Será necessário reconstruir "
            "a referência das músicas originais "
            "antes de continuar."
        )

        print()

        resultado = analisar_playlist(
            yt
        )

        if resultado is None:
            print(
                "Não foi possível analisar "
                "a playlist atual."
            )

            return True

        musicas_originais = resultado[
            "musicas"
        ]

        if len(musicas_originais) == 0:
            print(
                "A playlist já está vazia."
            )

            salvar_progresso(
                fase="ADICIONANDO",
                ultima_posicao=0,
                total=len(musicas_salvas)
            )

            sucesso = adicionar_em_lotes(
                yt,
                musicas_salvas,
                0
            )

            if sucesso:
                salvar_progresso(
                    fase="FINALIZADO",
                    ultima_posicao=len(
                        musicas_salvas
                    ),
                    total=len(
                        musicas_salvas
                    ),
                    status="CONCLUIDO"
                )

            return True

    else:
        musicas_originais = []

    print(
        "A execução será retomada "
        "do último ponto salvo."
    )

    print()

    sucesso = reorganizar_playlist(
        yt,
        musicas_originais,
        musicas_salvas
    )

    if sucesso:
        print()
        print("=" * 70)
        print(" CONCLUÍDO")
        print("=" * 70)
        print()

    else:
        print()
        print("=" * 70)
        print(" EXECUÇÃO INTERROMPIDA")
        print("=" * 70)
        print()

    return True


# ============================================================
# MAIN
# ============================================================

def main():
    print()
    print("=" * 70)
    print(" ORGANIZADOR DE PLAYLIST - YOUTUBE MUSIC")
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

    garantir_pastas()

    try:
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

    # --------------------------------------------------------
    # EXECUÇÃO ANTERIOR
    # --------------------------------------------------------

    if retomar_execucao(yt):
        return

    # --------------------------------------------------------
    # NOVA ANÁLISE
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print(" ANALISANDO PLAYLIST ANTES DA ORGANIZAÇÃO")
    print("=" * 70)
    print()

    resultado = analisar_playlist(
        yt
    )

    if resultado is None:
        return

    musicas = resultado["musicas"]
    ordem_correta = resultado["ordem_correta"]
    musicas_ordenadas = resultado["musicas_ordenadas"]

    if ordem_correta:
        print("=" * 70)
        print(" PLAYLIST JÁ ORGANIZADA")
        print("=" * 70)
        print()

        print(
            "A ordem atual da playlist "
            "já corresponde à ordem calculada."
        )
        print()
        print("Nenhuma alteração foi feita.")
        print()
        return

    sucesso = executar_organizacao(
        yt,
        musicas,
        musicas_ordenadas
    )

    print()

    if sucesso:
        print("=" * 70)
        print(" CONCLUÍDO")
        print("=" * 70)
        print()
        print(
            "A playlist foi reconstruída "
            "na nova ordem."
        )
        print()
        print(f"Progresso salvo em:")
        print(f"    {Config.ARQUIVO_PROGRESSO}")
    else:
        print("=" * 70)
        print(" EXECUÇÃO INTERROMPIDA")
        print("=" * 70)
        print()
    print()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()