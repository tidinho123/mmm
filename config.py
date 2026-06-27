# ============================================================
#   CONFIGURAÇÃO DO BOT QUOTEX  -  É AQUI QUE VOCÊ MEXE!
#   (Este é o bot de opções binárias: manda CALL e PUT.)
#   As linhas que começam com #  são só explicações, não mexa nelas.
# ============================================================

# 1) COLE AQUI o TOKEN do Telegram DESTE bot (o bot Quotex), entre aspas.
#    É a sequência que o @BotFather te deu (tipo  123456:ABC-DEF... ).
TELEGRAM_TOKEN = "COLE_AQUI_O_TOKEN_DO_BOT_QUOTEX"

# 2) COLE AQUI o seu CHAT ID (só números). Use aspas, tá certo assim.
TELEGRAM_CHAT_ID = "COLE_AQUI_O_SEU_CHAT_ID"

#    -------------------------------------------------------------
#    Pronto, só isso! O bot já funciona com o que você colou acima.
#    (AVANÇADO, opcional: se você preferir guardar o token num
#     arquivo à parte chamado  MEUS_DADOS.py , pode criar — se ele
#     existir, ele tem prioridade. Se NÃO existir, tudo bem, o bot
#     usa o que está aqui em cima e NÃO desliga.)
if "COLE_AQUI" in str(TELEGRAM_TOKEN):
    try:
        from MEUS_DADOS import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
    except Exception:
        pass

# ------------------------------------------------------------
#   Daqui pra baixo são ajustes do bot. Pode deixar assim
#   no começo. Depois, com calma, a gente mexe juntos.
# ------------------------------------------------------------

# 3) Quais ativos o bot vai vigiar AO MESMO TEMPO.
#    IMPORTANTE: o bot lê os preços na BINANCE, mas você vai OPERAR na
#    Quotex. Por isso deixei aqui criptos que existem NOS DOIS lugares
#    (Binance pra ler o gráfico + Quotex pra apostar).
#    ⚠️ Confira na SUA Quotex se o ativo está disponível antes de operar.
#    Pra adicionar: escreva o par entre aspas e vírgula no fim.
#    Pra tirar: apague a linha.
ATIVOS = [
    "BTCUSDT",   # Bitcoin
    "ETHUSDT",   # Ethereum
    "BNBUSDT",   # BNB
    "SOLUSDT",   # Solana
    "XRPUSDT",   # XRP
    "ADAUSDT",   # Cardano
    "DOGEUSDT",  # Dogecoin
    "AVAXUSDT",  # Avalanche
    "LINKUSDT",  # Chainlink
    "LTCUSDT",   # Litecoin
]

# 4) Tempo de cada vela do gráfico.
#    Pra opções binárias na Quotex, a sua estratégia é no M5 = "5m".
#    Exemplos: "1m", "5m", "15m", "1h"
TEMPO_GRAFICO = "5m"

# 5) De quantos em quantos segundos o bot olha os gráficos de novo.
INTERVALO_SEGUNDOS = 30

# ------------------------------------------------------------
#   AJUSTES DA SUA ESTRATÉGIA (EMA9 + EMA200 + RSI + MACD)
#   Mexa só se souber o que está fazendo.
# ------------------------------------------------------------

EMA_RAPIDA = 9      # a "EMA9 amarela" (a zona de pullback)
EMA_LENTA = 200     # a EMA200 (diz a direção da tendência)

RSI_PERIODO = 14
RSI_SOBRECOMPRA = 70   # acima disso = esticado pra cima
RSI_SOBREVENDA = 30    # abaixo disso = esticado pra baixo

# Nível mínimo de força (estrelas) pra te mandar o sinal.
#   1 = manda tudo (mais sinais, mais ruído)
#   2 = só quando tem pelo menos uma confirmação (recomendado)
#   3 = só quando os 3 gatilhos concordam (poucos sinais, mais seletivo)
FORCA_MINIMA = 2
