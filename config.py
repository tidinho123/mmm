# ============================================================
#   CONFIGURAÇÃO DO BOT QUOTEX  -  É AQUI QUE VOCÊ MEXE!
#   (Este é o bot de opções binárias: manda CALL e PUT.)
#   As linhas que começam com #  são só explicações, não mexa nelas.
# ============================================================

# 1) e 2) O seu TOKEN e o seu CHAT ID do Telegram ficam num arquivo
#    SEPARADO, chamado  MEUS_DADOS.py , só pra eles. Isso é de
#    propósito: assim, quando você atualizar o bot, o seu token NÃO
#    some. Veja o arquivo  MEUS_DADOS_EXEMPLO.py  pra criar.
#    (Os DOIS bots, Quotex e Binance, usam esse mesmo arquivo.)
try:
    from MEUS_DADOS import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
except ImportError:
    print("=" * 56)
    print("  FALTA O ARQUIVO  MEUS_DADOS.py  !")
    print("  Faça uma cópia do  MEUS_DADOS_EXEMPLO.py  com o nome")
    print("  MEUS_DADOS.py  e cole lá dentro o seu token e chat id.")
    print("=" * 56)
    raise SystemExit(1)

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
