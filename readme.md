# 🎵 Organizar Playlist — YouTube Music

Ferramenta em **Python** para analisar, organizar e gerenciar playlists do **YouTube Music** automaticamente. 🚀

O projeto permite:

* 🔎 Analisar uma playlist do YouTube Music
* 🎵 Listar as músicas existentes
* 👤 Identificar artistas e álbuns
* 📊 Gerar estatísticas da playlist
* 📄 Gerar relatório detalhado
* 🔤 Calcular uma nova ordem para as músicas
* 🔄 Comparar a ordem atual com a ordem calculada
* 🗂️ Reorganizar a playlist quando necessário
* 💾 Criar backup antes da reorganização
* ⏯️ Retomar uma reorganização interrompida
* 🗑️ Remover músicas duplicadas
* 🔍 Verificar músicas que não estão funcionando
* 🎶 Buscar músicas

> ⚠️ **Importante:** este projeto utiliza autenticação da sua própria sessão do YouTube Music. Nunca compartilhe seus dados de autenticação ou envie o arquivo `.env` para o Git.

---

## 📋 Requisitos

Antes de começar, você precisa ter:

* 🪟 Windows
* 🐍 Python 3
* 📦 pip
* 🌐 Um navegador com acesso ao YouTube Music
* 🔐 Uma conta do YouTube Music com acesso à playlist

---

# 🐍 1. Instalar o Python

Se você ainda não possui o Python instalado, uma forma simples no Windows é através da **Microsoft Store**.

### 📥 Instalação pela Microsoft Store

1. Abra o menu **Iniciar** do Windows.
2. Pesquise por:

```
Python
```

3. Abra a **Microsoft Store**.
4. Procure por uma versão recente do **Python 3**.
5. Clique em **Obter** ou **Instalar**.
6. Aguarde a instalação.

Depois da instalação, abra o **Prompt de Comando (CMD)** e execute:

```
python --version
```

Se aparecer algo parecido com:

```
Python 3.x.x
```

o Python foi instalado corretamente. ✅

Também pode testar:

```
py --version
```

Se `python` não funcionar, tente utilizar `py` nos comandos apresentados neste README.

---

# 📦 2. Verificar o pip

O `pip` é o gerenciador de pacotes do Python e será utilizado para instalar as dependências do projeto.

No CMD:

```
pip --version
```

Ou:

```
python -m pip --version
```

Se aparecer a versão do pip, está tudo certo. ✅

### 🔧 Caso o pip não esteja instalado

Execute:

```
python -m ensurepip --upgrade
```

Depois:

```
python -m pip install --upgrade pip
```

Teste novamente:

```
python -m pip --version
```

---

# 📥 3. Baixar o projeto

Clone o projeto utilizando Git:

```
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```
cd "Organizar playlist youtube"
```

---

# 📦 4. Instalar as dependências

O projeto possui um arquivo `requirements.txt` com as dependências necessárias.

Execute:

```
python -m pip install -r requirements.txt
```

Aguarde a instalação terminar.

Depois disso, as bibliotecas necessárias estarão disponíveis. ✅

---

# 📁 5. Estrutura do projeto

A estrutura esperada é:

```
Organizar playlist youtube/
│
├── Bats/
│   ├── BuscarMusicas.bat
│   ├── AnalisarPlaylist.bat
│   ├── OrganizarPlaylist.bat
│   ├── RemoverDuplicadas.bat
│   └── VerificarMusicasQuebradas.bat
│
├── Scripts/
│   ├── BuscarMusicas.py
│   ├── AnalisarPlaylist.py
│   ├── OrganizarPlaylist.py
│   ├── RemoverDuplicadas.py
│   ├── VerificarMusicasQuebradas.py
│   │
│   ├── Resultado/
│   └── Backups/
│
├── Configs/
│   ├── Config.py
│   ├── .env
│   ├── .env.example
│   └── browser.json
│
├── README.md
└── .gitignore
├── requirements.txt
```

---

# 🔐 6. Configurar a autenticação

O projeto precisa utilizar a autenticação da sua sessão do YouTube Music.

Para isso serão utilizados:

* `Cookie`
* `Authorization`
* `x-goog-visitor-id`

⚠️ **Esses dados são privados.**

Não envie esses valores para outras pessoas, não publique em Issues, Pull Requests, Discord, WhatsApp, GitHub ou qualquer outro local público.

Também **não suba o `.env` para o Git**.

---

# 📝 7. Criar o arquivo `.env`

Dentro da pasta:

```
Configs/
```

existe o arquivo:

```
.env.example
```

Faça uma cópia dele e renomeie para:

```
.env
```

Por exemplo:

```
Configs/
├── .env
└── .env.example
```

O `.env` será utilizado para armazenar os dados privados da sua sessão.

---

# 🌐 8. Abrir o YouTube Music

Abra o navegador e entre no:

**YouTube Music**

```
https://music.youtube.com
```

Faça login normalmente na sua conta.

Depois disso, abra a playlist que deseja utilizar.

---

# 🛠️ 9. Abrir o DevTools

Com o YouTube Music aberto:

### No Windows

Pressione:

**F12**

ou:

**Ctrl + Shift + I**

Isso abrirá as ferramentas de desenvolvedor do navegador.

Depois:

1. Clique na aba **Network** / **Rede**.
2. Atualize a página do YouTube Music com `F5`.
3. Aguarde as requisições aparecerem.

---

# 🔎 10. Encontrar a requisição correta

Na aba **Network**, procure por uma requisição relacionada à API do YouTube Music.

Uma maneira simples é utilizar o filtro:

```
browse
```

ou:

```
playlist
```

Também é possível procurar requisições que utilizem:

```
youtubei
```

Clique em uma requisição que tenha sido feita para o YouTube Music.

---

# 🔑 11. Encontrar o Authorization

Com a requisição selecionada:

1. Abra **Headers**.
2. Procure por **Request Headers**.
3. Localize:

```
authorization
```

O valor será parecido com:

```
Bearer ...
```

ou outro valor fornecido pelo navegador.

Copie **o valor completo**.

⚠️ Não publique esse valor.

No `.env`:

```
YTMUSIC_AUTHORIZATION=COLE_O_VALOR_AQUI
```

---

# 🍪 12. Encontrar o Cookie

Na mesma requisição:

1. Continue em **Headers**.
2. Procure por **Request Headers**.
3. Localize:

```
cookie
```

O conteúdo será uma sequência grande de cookies.

Copie o valor completo.

No `.env`:

```
YTMUSIC_COOKIE=COLE_O_VALOR_AQUI
```

⚠️ O Cookie pode permitir que uma sessão autenticada seja reutilizada. **Nunca compartilhe esse valor.**

---

# 🆔 13. Encontrar o x-goog-visitor-id

Ainda nos **Request Headers**, procure:

```
x-goog-visitor-id
```

Você encontrará algo parecido com:

```
x-goog-visitor-id: VALOR
```

Copie apenas o valor.

No `.env`:

```
YTMUSIC_VISITOR_ID=COLE_O_VALOR_AQUI
```

---

# 📝 14. Exemplo do `.env`

Depois de preencher os valores, seu arquivo poderá ficar parecido com:

```
YTMUSIC_COOKIE=SEU_COOKIE
YTMUSIC_VISITOR_ID=SEU_VISITOR_ID
YTMUSIC_AUTHORIZATION=SEU_AUTHORIZATION
```

⚠️ **Não copie os valores deste exemplo.**

Os valores devem ser obtidos da sua própria sessão no navegador.

---

# 🔒 15. Proteção do `.env`

O arquivo `.env` contém informações privadas.

Por isso ele deve estar no `.gitignore`.

Exemplo:

```
Configs/.env
```

O arquivo:

```
Configs/.env.example
```

pode ser enviado para o Git porque deve conter apenas a estrutura das configurações, sem dados reais.

Exemplo:

```
YTMUSIC_COOKIE=
YTMUSIC_VISITOR_ID=
YTMUSIC_AUTHORIZATION=
```

---

# ⚙️ 16. Configurar a playlist

A playlist utilizada pelo projeto é configurada em:

```
Configs/Config.py
```

Procure por:

```
PLAYLIST_ID = "..."
```

Substitua pelo ID da playlist que deseja utilizar.

Por exemplo, uma URL:

```
https://music.youtube.com/playlist?list=PLXXXXXXXXXXXX
```

possui como ID:

```
PLXXXXXXXXXXXX
```

Então:

```
PLAYLIST_ID = "PLXXXXXXXXXXXX"
```

---

# 🔤 17. Configurar a ordem das músicas

Também é possível configurar a ordem desejada:

```
ORDEM_ALBUM = "ASC"
ORDEM_MUSICA = "ASC"
ORDEM_ARTISTA = "ASC"
```

Onde:

* `ASC` → crescente 🔼
* `DESC` → decrescente 🔽

Por exemplo:

```
ORDEM_ALBUM = "ASC"
ORDEM_MUSICA = "ASC"
ORDEM_ARTISTA = "ASC"
```

resulta em:

**Artista → Álbum → Música**

em ordem crescente.

---

# 💾 18. Backup

Por segurança, o organizador pode criar um backup antes de alterar a playlist.

Configuração:

```
CRIAR_BACKUP = True
```

Os backups ficam em:

```
Scripts/Backups/
```

Cada execução cria um arquivo de backup separado.

---

# 🔄 19. Organização em lotes

A reorganização é realizada em lotes para evitar enviar todas as músicas de uma vez.

Configuração:

```
TAMANHO_LOTE = 50
```

Também é possível configurar uma pausa entre os lotes:

```
PAUSA_ENTRE_LOTES = 1.0
```

O valor representa segundos.

---

# ▶️ 20. Analisar a playlist

Para analisar a playlist sem modificá-la, execute:

```
Bats\AnalisarPlaylist.bat
```

A análise irá:

* 🎵 Ler as músicas
* 👤 Identificar artistas
* 💿 Identificar álbuns
* 📊 Mostrar estatísticas
* 🔤 Calcular a ordem
* 🔎 Comparar a ordem atual com a ordem calculada
* 📄 Gerar o relatório

Nenhuma alteração será feita na playlist.

---

# 🔄 21. Organizar a playlist

Para organizar a playlist:

```
Bats\OrganizarPlaylist.bat
```

O programa irá primeiro analisar a playlist.

### ✅ Se a playlist já estiver organizada

O programa informará que:

```
A playlist já está na ordem desejada.

Nenhuma alteração foi feita.
```

Nesse caso:

* ❌ Não cria backup
* ❌ Não pede confirmação
* ❌ Não remove músicas
* ❌ Não adiciona músicas novamente

### 🔀 Se a playlist estiver fora de ordem

Será exibida uma prévia das alterações.

Depois será solicitada confirmação:

```
Digite ORGANIZAR para confirmar:
```

Digite:

```
ORGANIZAR
```

para iniciar a reorganização.

---

# ⏯️ 22. Retomar uma execução interrompida

O organizador salva o progresso da operação em:

```
Scripts/Resultado/progresso.json
```

Caso o processo seja interrompido durante a remoção ou adição das músicas, o programa pode utilizar esse arquivo para continuar a operação.

Isso evita precisar começar toda a reorganização novamente.

---

# 🗂️ 23. Ordem calculada

A ordem calculada é salva em:

```
Scripts/Resultado/ordem_calculada.json
```

Esse arquivo contém informações como:

* posição
* artista
* álbum
* título
* `videoId`
* `setVideoId`

---

# 📄 24. Relatório

O relatório completo da playlist é salvo em:

```
Scripts/Resultado/relatorio_playlist.txt
```

Ele organiza as músicas por:

**Artista → Álbum → Música**

---

# 🗑️ 25. Remover músicas duplicadas

Para verificar/remover músicas duplicadas:

```
Bats\RemoverDuplicadas.bat
```

⚠️ Antes de remover músicas, confira o que será considerado duplicado.

---

# 🔍 26. Verificar músicas quebradas

Para verificar músicas que não estão funcionando corretamente:

```
Bats\VerificarMusicasQuebradas.bat
```

Esse processo pode ajudar a identificar músicas removidas, indisponíveis ou que apresentam problemas no YouTube Music.

---

# 🎵 27. Buscar músicas

Para utilizar o script de busca:

```
Bats\BuscarMusicas.bat
```

Esse script permite localizar músicas no YouTube Music.

---

# 🛡️ 28. Segurança

### 🚨 NUNCA envie para o Git:

```
.env
```

E principalmente nunca publique:

* 🔴 `authorization`
* 🔴 `cookie`
* 🟠 `x-goog-visitor-id`

Esses dados pertencem à sua sessão do YouTube Music.

### ❌ Não faça:

```
git add .
git commit -m "configuração"
git push
```

sem conferir se `.env` está protegidos pelo `.gitignore`.

### ✅ Antes de fazer commit:

```
git status
```

Verifique se o arquivo:

```
Configs/.env
```

não aparecem entre os arquivos que serão enviados.

---

# 🧹 29. Caso a autenticação pare de funcionar

Os dados obtidos pelo navegador podem deixar de funcionar caso a sessão seja alterada, os cookies sejam renovados ou o YouTube Music altere seus mecanismos de autenticação.

Nesse caso:

1. Abra o YouTube Music.
2. Abra o DevTools com `F12`.
3. Entre em **Network**.
4. Atualize a página.
5. Localize novamente a requisição do YouTube Music.
6. Copie novamente:

   * `authorization`
   * `cookie`
   * `x-goog-visitor-id`
7. Atualize o `.env`.
8. Execute novamente o programa.

---

# 🚀 30. Execução rápida

Depois de tudo configurado:

### Analisar

```
Bats\AnalisarPlaylist.bat
```

### Organizar

```
Bats\OrganizarPlaylist.bat
```

### Remover duplicadas

```
Bats\RemoverDuplicadas.bat
```

### Verificar músicas quebradas

```
Bats\VerificarMusicasQuebradas.bat
```

### Buscar músicas

```
Bats\BuscarMusicas.bat
```

---

# 📌 Resumo

| Etapa | Ação                                    |
| ----- | --------------------------------------- |
| 1️⃣   | Instalar Python                         |
| 2️⃣   | Verificar `pip`                         |
| 3️⃣   | Clonar o projeto                        |
| 4️⃣   | Instalar `requirements.txt`             |
| 5️⃣   | Criar `.env` a partir do `.env.example` |
| 6️⃣   | Obter autenticação pelo Network         |
| 7️⃣   | Configurar `PLAYLIST_ID`                |
| 8️⃣   | Executar análise                        |
| 9️⃣   | Organizar playlist                      |

---

## ❤️ Projeto

Feito para facilitar a organização de playlists do YouTube Music de forma automatizada.

**Python + ytmusicapi + YouTube Music** 🎵🐍🚀
