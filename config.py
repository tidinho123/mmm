# ============================================================
#   CONFIGURAÇÃO DO BOT  -  É AQUI QUE VOCÊ MEXE!
#   Troque os valores entre aspas pelos SEUS dados.
#   (As linhas que começam com #  são só explicações, não mexa nelas)
# ============================================================

# 1) A "senha" (token) do seu robô do Telegram.
#    Você vai pegar isso conversando com o @BotFather (eu te ensino).
TELEGRAM_TOKEN = "COLE_AQUI_O_TOKEN_DO_SEU_ROBO"

# 2) O seu "número de identificação" no Telegram (chat id).
#    Eu te ensino a descobrir esse número.
TELEGRAM_CHAT_ID = "COLE_AQUI_O_SEU_CHAT_ID"

# ------------------------------------------------------------
#   Daqui pra baixo são ajustes do bot. Pode deixar assim
#   no começo. Depois, com calma, a gente mexe juntos.
# ------------------------------------------------------------

# 3) Quais ativos o bot vai vigiar AO MESMO TEMPO.
#    Você falou "todo ativo" — mas a Binance tem MILHARES de pares.
#    Vigiar todos deixaria o bot lento e te encheria de mensagem.
#    Então deixei aqui os mais negociados (os que mais valem a pena).
#    Pra adicionar mais, é só escrever o nome do par entre aspas e
#    uma vírgula no fim. Pra tirar, apaga a linha. Simples assim.
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
    "MATICUSDT", # Polygon
]

# 4) Tempo de cada vela do gráfico.
#    Sua estratégia é no M5, então deixei "5m".
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
