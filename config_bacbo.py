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
#
#   NÃO PRECISA MEXER AQUI! Ao ligar, o bot PROCURA sozinho o
#   histórico na tela. Deixe as duas linhas abaixo VAZIAS ("").
#
#   Só preencha se você quiser TRAVAR num lugar específico (o
#   calibrar_bacbo.py mostra exatamente o que colar).
# ------------------------------------------------------------

# (opcional) CSS do "iframe" do jogo. Vazio = o bot descobre sozinho.
SELETOR_IFRAME = ""

# (opcional) CSS da lista de bolinhas. Vazio = o bot descobre sozinho.
SELETOR_HISTORICO = ""

# Como o bot descobre a cor de cada bolinha:
#   "auto"   -> tenta tudo (classe + texto + cor). Comece com este.
#   "classe" -> pela classe do elemento (ex: class="...banker...")
#   "texto"  -> pela letra/palavra dentro (ex: "B", "P", "T")
#   "cor"    -> pela cor de fundo (vermelho/azul/verde)
LER_DE = "auto"

# Palavras/letras que identificam cada resultado. Se a calibração mostrar
# a sequência TROCADA (Banca vindo como Player, etc), ajuste estas listas.
# (Marcador de UMA letra só vale quando a bolinha é SÓ aquela letra.)
MARCADORES_BANCA  = ["banker", "banca", "banco", "vermelh", "red", "b"]
MARCADORES_PLAYER = ["player", "jogador", "azul", "blue", "p", "j"]
MARCADORES_EMPATE = ["tie", "empate", "verde", "green", "draw", "t"]


# ------------------------------------------------------------
#   4) A ESTRATÉGIA  (como ele decide o palpite)
#   Não sabe qual usar? Comece com "so_coletar" por um tempo,
#   veja como o jogo se comporta, depois troque.
# ------------------------------------------------------------

# Opções:
#   "confluencia" -> A MAIS COMPLETA (padrão): combina 3 análises ao mesmo
#                    tempo — sequência/zig-zag + domínio da janela + tamanho
#                    do padrão. As estrelas mostram QUANTAS análises
#                    concordaram (⭐ = 1, ⭐⭐⭐ = todas).
#   "so_coletar"  -> NÃO dá palpite. Só mostra o histórico e as estatísticas.
#   "tendencia"   -> só sequência: quando uma cor repete, ele age.
#   "frequencia"  -> aposta na cor que apareceu MENOS na janela (volta à média).
#   "alternancia" -> quando vem zig-zag (🔴🔵🔴🔵...), sugere continuar o zig-zag.
ESTRATEGIA = "confluencia"

# Só pra estratégia "tendencia":
#   "seguir" -> se deu 3x Banca, ele sugere BANCA (surfar a sequência).
#   "contra" -> se deu 3x Banca, ele sugere PLAYER (apostar na quebra).
MODO_TENDENCIA = "seguir"

# Quantas repetições seguidas contam como "sequência" (pra tendencia).
#   2 = manda MAIS sinais (avisa já na 2ª repetição seguida)
#   3 = mais seletivo (menos sinais, esperas maiores)
STREAK_MINIMO = 2

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

# "Sinal de vida": se ficar este tempo (em minutos) sem te mandar nada,
# ele avisa que continua ligado. Coloque 0 pra desligar esse aviso.
AVISO_VIVO_MINUTOS = 15

# RITMO das mensagens (segundos).
#   0   = manda a CADA RODADA nova (RECOMENDADO). Assim o "saiu X" da
#         auditoria bate certinho com o que você vê na tela, e o placar
#         confere a rodada certa. Você recebe mais mensagens, mas tudo alinha.
#   120 = uma a cada 2 min (menos mensagens, mas a auditoria fica confusa
#         porque ele confere uma rodada de minutos atrás).
SINAL_A_CADA_SEGUNDOS = 0

# ------------------------------------------------------------
#   ANTI-INATIVIDADE (pra a demo não encerrar sozinha)
# ------------------------------------------------------------

# De tantos em tantos segundos o bot "mexe" na página pra o site não
# encerrar a sessão por inatividade. 0 = desligado.
ANTI_INATIVIDADE_SEGUNDOS = 90

# Se aparecer um popup de "continuar jogando?", o bot clica sozinho.
CLICAR_CONTINUAR = True

# SÓ clica em botões cujo texto contenha uma destas palavras. Deixei
# palavras seguras (ligadas a "continuar/sessão"), longe de botões de
# aposta. Se o teu site usar outra frase, adicione aqui.
PALAVRAS_CONTINUAR = ["continuar", "continue", "ainda estou", "estou aqui",
                      "still here", "still playing", "resume", "reconectar"]
