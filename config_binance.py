# ============================================================
#   CONFIGURAÇÃO DO BOT BINANCE  -  É AQUI QUE VOCÊ MEXE!
#   (Este é o bot pra COMPRAR cripto de verdade na Binance Spot.)
#   Ele manda SÓ sinais de COMPRA (CALL), já com Take Profit e
#   Stop Loss prontos. As linhas com #  são explicações.
# ============================================================

# 1) COLE AQUI o TOKEN do Telegram DESTE bot (o bot Binance), entre aspas.
#    IMPORTANTE: pra os sinais virem SEPARADOS do bot Quotex, crie um
#    NOVO robô no @BotFather e cole o token DELE aqui (diferente do outro).
TELEGRAM_TOKEN = "8864915396:AAE-ApNrjFkHb1yVVdhRsITRV5igMg2AiZ8"

# 2) COLE AQUI o seu CHAT ID (só números).
TELEGRAM_CHAT_ID = 7711912413

#    -------------------------------------------------------------
#    Pronto! O bot já funciona com o que você colou acima.
#    (AVANÇADO, opcional: se existir um arquivo  MEUS_DADOS_BINANCE.py ,
#     ele tem prioridade. Se NÃO existir, o bot usa o que está aqui em
#     cima e NÃO desliga.)
if "COLE_AQUI" in str(TELEGRAM_TOKEN):
    try:
        from MEUS_DADOS_BINANCE import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
    except Exception:
        pass

# ------------------------------------------------------------
#   Ajustes do bot. Pode deixar assim no começo.
# ------------------------------------------------------------

# 3) Quais criptos o bot vai vigiar na Binance (pra COMPRAR).
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

# 4) Tempo de cada vela. Pra COMPRAR cripto de verdade, tempos maiores
#    são mais seguros (movimento maior, taxa da Binance pesa menos).
#    Deixei "15m". Pra mais calmo ainda, troque por "1h".
TEMPO_GRAFICO = "15m"

# 5) De quantos em quantos segundos o bot olha os gráficos de novo.
INTERVALO_SEGUNDOS = 30

# ------------------------------------------------------------
#   AJUSTES DA SUA ESTRATÉGIA (EMA9 + EMA200 + RSI + MACD)
# ------------------------------------------------------------

EMA_RAPIDA = 9
EMA_LENTA = 200

RSI_PERIODO = 14
RSI_SOBRECOMPRA = 70
RSI_SOBREVENDA = 30

# Nível mínimo de força (estrelas) pra te mandar o sinal.
#   2 = recomendado (pelo menos uma confirmação).
FORCA_MINIMA = 2

# ------------------------------------------------------------
#   PLANO DE COMPRA (Take Profit e Stop Loss)
#   Quando chega um sinal de COMPRA, o bot já calcula na mensagem
#   onde vender no lucro e onde sair no prejuízo.
#   Os números são em PORCENTAGEM do preço de entrada.
# ------------------------------------------------------------
TAKE_PROFIT_PCT = 1.0   # vender no LUCRO a +1% acima da compra
STOP_LOSS_PCT = 0.5     # sair no PREJUÍZO a -0.5% abaixo da compra
