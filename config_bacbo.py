# ============================================================
#   CONFIGURAÇÃO DO BOT BAC BO (Bantubet)  -  É AQUI QUE VOCÊ MEXE!
#
#   Este bot ABRE o Chrome, você faz login e abre o Bac Bo, e ele
#   fica LENDO o histórico de resultados (🔴 Banca / 🔵 Player / 🟡 Empate).
#   A cada rodada nova ele aplica a estratégia que você escolher aqui
#   embaixo e te manda no TELEGRAM o palpite pra PRÓXIMA rodada.
#
#   AVISO HONESTO: Bac Bo é jogo de DADO, cada rodada é sorteada do zero.
#   Nenhum robô adivinha o futuro. Isto é ferramenta de ESTUDO/APOIO.
#   Jogue só com o que você pode perder.
#
#   As linhas que começam com  #  são só explicação, não precisa mexer.
# ============================================================

# ------------------------------------------------------------
#   1) TELEGRAM  (pra onde chega o sinal)
# ------------------------------------------------------------

# COLE AQUI o TOKEN do seu robô do Telegram (o @BotFather te dá), entre aspas.
TELEGRAM_TOKEN = "COLE_AQUI_O_TOKEN_DO_BOT_BACBO"

# COLE AQUI o seu CHAT ID (só números). Descubra rodando  pegar_meu_id_bacbo.py
TELEGRAM_CHAT_ID = "COLE_AQUI_O_SEU_CHAT_ID"

#    (AVANÇADO, opcional: se existir um arquivo MEUS_DADOS.py com o token,
#     ele tem prioridade. Se não existir, tudo bem, usa o de cima.)
if "COLE_AQUI" in str(TELEGRAM_TOKEN):
    try:
        from MEUS_DADOS import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
    except Exception:
        pass


# ------------------------------------------------------------
#   2) O JOGO  (onde o bot vai abrir)
# ------------------------------------------------------------

# Endereço do site. O bot abre AQUI e ESPERA você logar e abrir o Bac Bo.
# Pode deixar a página inicial da Bantubet; você navega até o jogo na mão.
URL_JOGO = "https://www.bantubet.co.mz/"

# Pasta onde o Chrome guarda o SEU login (assim você não loga toda vez).
# Deixe assim; ela é criada sozinha do lado do bot.
PASTA_PERFIL = "perfil_bacbo_chrome"

# Se quiser, aponte pro seu Chrome instalado (deixe "" pra achar sozinho).
CAMINHO_CHROME = ""


# ------------------------------------------------------------
#   3) ONDE ESTÃO OS RESULTADOS NA TELA
#   (isto aqui a gente descobre JUNTOS rodando  calibrar_bacbo.py .
#    Ele te mostra o que colar nestas 3 linhas.)
# ------------------------------------------------------------

# O jogo costuma ficar dentro de um "iframe". Se a calibração achar um,
# cole o CSS dele aqui. Se não tiver, deixe "" (vazio).
SELETOR_IFRAME = ""

# CSS do quadradinho/lista que segura as bolinhas do histórico.
SELETOR_HISTORICO = ""

# Como o bot descobre a cor de cada bolinha:
#   "auto"   -> tenta tudo (classe + texto + cor). Comece com este.
#   "classe" -> pela classe do elemento (ex: class="...banker...")
#   "texto"  -> pela letra/palavra dentro (ex: "B", "P", "T")
#   "cor"    -> pela cor de fundo (vermelho/azul/verde)
LER_DE = "auto"

# Palavras/letras que identificam cada resultado. Se a calibração mostrar
# a sequência TROCADA (Banca vindo como Player, etc), ajuste estas listas.
MARCADORES_BANCA  = ["banker", "banca", "vermelh", "red", "dealer", "b"]
MARCADORES_PLAYER = ["player", "azul", "blue", "p"]
MARCADORES_EMPATE = ["tie", "empate", "verde", "green", "draw", "t"]


# ------------------------------------------------------------
#   4) A ESTRATÉGIA  (como ele decide o palpite)
#   Não sabe qual usar? Comece com "so_coletar" por um tempo,
#   veja como o jogo se comporta, depois troque.
# ------------------------------------------------------------

# Opções:
#   "so_coletar"  -> NÃO dá palpite. Só mostra o histórico e as estatísticas.
#                    (o jeito mais seguro de começar e observar)
#   "tendencia"   -> quando uma cor repete várias vezes seguidas, ele age.
#   "frequencia"  -> aposta na cor que apareceu MENOS na janela (volta à média).
#   "alternancia" -> quando vem zig-zag (🔴🔵🔴🔵...), sugere continuar o zig-zag.
ESTRATEGIA = "so_coletar"

# Só pra estratégia "tendencia":
#   "seguir" -> se deu 3x Banca, ele sugere BANCA (surfar a sequência).
#   "contra" -> se deu 3x Banca, ele sugere PLAYER (apostar na quebra).
MODO_TENDENCIA = "seguir"

# Quantas repetições seguidas contam como "sequência" (pra tendencia).
STREAK_MINIMO = 3

# Quantas rodadas o bot olha pra trás nas contas (pra frequencia/alternancia).
JANELA = 15

# Empate (🟡) atrapalha a leitura de sequência. Deixe True pra ignorá-lo
# na hora de contar sequências (ele continua sendo mostrado e contado à parte).
IGNORAR_EMPATE = True

# Força mínima (⭐ a ⭐⭐⭐) pra te mandar o sinal. 1 = manda mais, 3 = só os fortes.
FORCA_MINIMA = 1


# ------------------------------------------------------------
#   5) GALE  (opcional — sugestão de quanto apostar)
#   Isto NÃO muda a chance de ganhar. É só uma sugestão de valor.
# ------------------------------------------------------------

USAR_GALE = False        # True pra ligar a sugestão de gale
APOSTA_BASE = 10         # valor da 1ª aposta (na sua moeda)
NIVEIS_GALE = 2          # quantas vezes dobrar depois de perder


# ------------------------------------------------------------
#   6) RITMO
# ------------------------------------------------------------

# De quantos em quantos segundos ele relê a tela procurando rodada nova.
INTERVALO_SEGUNDOS = 2
