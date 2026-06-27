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
#    Pra COMPRAR cripto de verdade na Binance, tempos maiores são mais
#    seguros (o movimento é maior e a taxa da Binance pesa menos).
#    Por isso deixei "15m". Se quiser ainda mais calmo, troque por "1h".
#    Exemplos: "5m", "15m", "1h", "4h"
TEMPO_GRAFICO = "15m"

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

# ------------------------------------------------------------
#   MODO BINANCE (comprar cripto de verdade no Spot)
# ------------------------------------------------------------

# Na Binance Spot você só GANHA quando o preço SOBE (compra barato,
# vende mais caro). Não dá pra ganhar na queda. Por isso, com isto
# ligado (True), o bot só te manda os sinais 🟢 CALL (de COMPRA) e
# ignora os 🔴 PUT (que na Binance servem só como "não compre agora").
#   True  = só manda sinais de COMPRA (recomendado pra Binance Spot)
#   False = manda CALL e PUT (use só se for operar em outro lugar)
SO_COMPRA = True

# Quando chega um sinal de COMPRA, o bot já sugere na mensagem onde
# vender no lucro (Take Profit) e onde sair no prejuízo (Stop Loss).
# Os números abaixo são em PORCENTAGEM do preço de entrada.
#   Exemplo: 1.0 = 1% acima/abaixo do preço da compra.
TAKE_PROFIT_PCT = 1.0   # vender no lucro a +1% acima da compra
STOP_LOSS_PCT = 0.5     # sair no prejuízo a -0.5% abaixo da compra
