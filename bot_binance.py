# ============================================================
#   BOT BINANCE  -  Sinais de COMPRA (CALL) pra cripto de verdade
#
#   Este bot é pra COMPRAR cripto no SPOT da Binance.
#   Na Binance Spot você só GANHA quando o preço SOBE, então este
#   bot manda SÓ sinais de COMPRA (🟢 CALL) e ignora os de queda.
#   Cada sinal já vem com o PLANO pronto: onde comprar, onde vender
#   no lucro (Take Profit) e onde sair no prejuízo (Stop Loss).
#
#   (Se você quer operar OPÇÕES BINÁRIAS na Quotex, com CALL e PUT,
#    use o outro bot:  bot.py )
#
#   VOCÊ NÃO PRECISA ENTENDER ESTE ARQUIVO.
#   (Pra mexer nas configurações, abra o arquivo  config_binance.py )
#
#   AVISO IMPORTANTE: nenhum sinal é garantia de lucro.
#   Isto é uma ferramenta de ESTUDO e APOIO, não dinheiro fácil.
# ============================================================

import time
import requests
import config_binance as config


# ---------- Funções que conversam com a internet ----------

def pegar_velas(ativo, tempo, quantidade=300):
    """Busca o histórico de velas (OHLC) na Binance."""
    url = "https://api.binance.com/api/v3/klines"
    parametros = {"symbol": ativo, "interval": tempo, "limit": quantidade}
    resposta = requests.get(url, params=parametros, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()
    velas = []
    for v in dados:
        velas.append({
            "hora": v[0],
            "abertura": float(v[1]),
            "maxima": float(v[2]),
            "minima": float(v[3]),
            "fechamento": float(v[4]),
        })
    # Trabalhamos sempre com a ÚLTIMA VELA JÁ FECHADA (descarta a atual).
    return velas[:-1]


def enviar_telegram(mensagem):
    """Envia uma mensagem para o seu Telegram."""
    url = "https://api.telegram.org/bot{}/sendMessage".format(config.TELEGRAM_TOKEN)
    parametros = {"chat_id": config.TELEGRAM_CHAT_ID, "text": mensagem}
    try:
        requests.get(url, params=parametros, timeout=15)
    except Exception as erro:
        print("Não consegui enviar no Telegram:", erro)


# ---------- Contas dos indicadores técnicos ----------

def ema_serie(valores, periodo):
    """Calcula a EMA passo a passo e devolve a LISTA inteira."""
    k = 2 / (periodo + 1)
    ema = valores[0]
    saida = [ema]
    for preco in valores[1:]:
        ema = preco * k + ema * (1 - k)
        saida.append(ema)
    return saida


def calcular_rsi(valores, periodo=14):
    """Calcula o RSI (força do movimento, de 0 a 100) no último ponto."""
    if len(valores) < periodo + 1:
        return 50.0
    ganhos = 0.0
    perdas = 0.0
    for i in range(1, periodo + 1):
        diferenca = valores[-i] - valores[-i - 1]
        if diferenca >= 0:
            ganhos += diferenca
        else:
            perdas += -diferenca
    if perdas == 0:
        return 100.0
    forca = (ganhos / periodo) / (perdas / periodo)
    return 100 - (100 / (1 + forca))


def calcular_macd(fechamentos):
    """MACD clássico (12, 26, 9)."""
    if len(fechamentos) < 35:
        return 0.0, 0.0, 0.0, 0.0
    ema12 = ema_serie(fechamentos, 12)
    ema26 = ema_serie(fechamentos, 26)
    linha_macd = [a - b for a, b in zip(ema12, ema26)]
    linha_sinal = ema_serie(linha_macd, 9)
    return (linha_macd[-1], linha_sinal[-1],
            linha_macd[-2], linha_sinal[-2])


# ---------- A SUA ESTRATÉGIA (quando dar o sinal) ----------

def analisar(velas):
    """Aplica a estratégia na última vela fechada.
    Aqui só nos interessa o sinal de COMPRA (CALL)."""
    if len(velas) < config.EMA_LENTA + 5:
        return None

    fechamentos = [v["fechamento"] for v in velas]

    ema9 = ema_serie(fechamentos, config.EMA_RAPIDA)
    ema200 = ema_serie(fechamentos, config.EMA_LENTA)
    macd_agora, sinal_agora, macd_antes, sinal_antes = calcular_macd(fechamentos)

    rsi_agora = calcular_rsi(fechamentos, config.RSI_PERIODO)
    rsi_antes = calcular_rsi(fechamentos[:-1], config.RSI_PERIODO)

    vela = velas[-1]
    e9 = ema9[-1]
    e200 = ema200[-1]
    e9_antes = ema9[-2]

    verde = vela["fechamento"] > vela["abertura"]
    tocou_ema9 = vela["minima"] <= e9 <= vela["maxima"]

    confirmacoes = []

    # GATILHO A (só COMPRA): acima da EMA200, recuou e tocou a EMA9,
    # fechou VERDE acima da EMA9.
    eh_compra = (vela["fechamento"] > e200 and tocou_ema9
                 and vela["fechamento"] > e9 and verde)

    if not eh_compra:
        return {
            "sinal": None,
            "preco": vela["fechamento"],
            "rsi": rsi_agora,
            "ema9": e9, "ema200": e200,
            "hora": vela["hora"],
        }

    # GATILHO B: RSI a favor da subida.
    if rsi_antes <= config.RSI_SOBREVENDA and rsi_agora > rsi_antes:
        confirmacoes.append("RSI saindo da sobrevenda (virou pra cima)")
    elif rsi_agora > 50:
        confirmacoes.append("RSI a favor (acima de 50)")

    # GATILHO C: cruzamento do MACD pra cima.
    cruzou_cima = macd_antes <= sinal_antes and macd_agora > sinal_agora
    if cruzou_cima:
        confirmacoes.append("MACD cruzou pra cima")
    elif macd_agora > sinal_agora:
        confirmacoes.append("MACD a favor (acima do sinal)")

    # Confirmação extra: a EMA9 está subindo?
    if e9 > e9_antes:
        confirmacoes.append("EMA9 subindo")

    # Força = 1 (gatilho principal) + 1 por confirmação forte (máx 3).
    forca = 1 + len([c for c in confirmacoes
                     if "RSI" in c or "MACD cruzou" in c])
    forca = min(forca, 3)

    return {
        "sinal": "CALL",
        "forca": forca,
        "confirmacoes": confirmacoes,
        "preco": vela["fechamento"],
        "rsi": rsi_agora,
        "ema9": e9, "ema200": e200,
        "hora": vela["hora"],
    }


# ---------- Montagem da mensagem ----------

def montar_mensagem(ativo, r):
    estrelas = "⭐" * r["forca"]
    preco = r["preco"]
    take_profit = preco * (1 + config.TAKE_PROFIT_PCT / 100)
    stop_loss = preco * (1 - config.STOP_LOSS_PCT / 100)

    linhas = [
        "🟢 SINAL DE COMPRA (Binance Spot)",
        "Ativo: {}".format(ativo),
        "Tempo do gráfico: {}".format(config.TEMPO_GRAFICO),
        "Preço agora: {:.6g}".format(preco),
        "Força: {} ({} de 3)".format(estrelas, r["forca"]),
        "",
        "Por quê:",
        "• Pullback na EMA9 a favor da EMA200 (sinal principal)",
    ]
    for c in r["confirmacoes"]:
        linhas.append("• " + c)

    linhas += [
        "",
        "RSI: {:.0f}".format(r["rsi"]),
        "",
        "📋 PLANO (Binance Spot):",
        "1) COMPRAR perto de {:.6g}".format(preco),
        "2) 🎯 Vender no LUCRO (Take Profit): {:.6g}  (+{:.1f}%)".format(
            take_profit, config.TAKE_PROFIT_PCT),
        "3) 🛑 Sair no PREJUÍZO (Stop Loss): {:.6g}  (-{:.1f}%)".format(
            stop_loss, config.STOP_LOSS_PCT),
        "(Dica: use uma ordem OCO pra deixar o TP e o SL automáticos.)",
        "",
        "⚠️ Confira no seu gráfico antes de operar. Sinal não é garantia.",
    ]
    return "\n".join(linhas)


# ---------- O "loop" principal: roda pra sempre ----------

def main():
    print("Bot BINANCE ligado! Vigiando", len(config.ATIVOS),
          "ativos no tempo", config.TEMPO_GRAFICO)
    enviar_telegram(
        "✅ Bot BINANCE ligado!\nVou vigiar {} criptos no gráfico de {} e "
        "te avisar SÓ quando aparecer um sinal de COMPRA (🟢 CALL), já com "
        "Take Profit e Stop Loss prontos.\n\nEstratégia: EMA9 + EMA200 + "
        "RSI + MACD.\n\n⚠️ Lembre-se: sinal NÃO é garantia. Opere com "
        "responsabilidade.".format(
            len(config.ATIVOS), config.TEMPO_GRAFICO)
    )

    ja_avisado = {}

    while True:
        for ativo in config.ATIVOS:
            try:
                velas = pegar_velas(ativo, config.TEMPO_GRAFICO)
                r = analisar(velas)
                if r is None:
                    print(ativo, "- sem dados suficientes ainda")
                    continue

                if r["sinal"] == "CALL" and r["forca"] >= config.FORCA_MINIMA:
                    chave = (r["hora"], r["sinal"])
                    if ja_avisado.get(ativo) != chave:
                        enviar_telegram(montar_mensagem(ativo, r))
                        ja_avisado[ativo] = chave
                        print(">>> COMPRA", ativo, "força", r["forca"])
                    else:
                        print(ativo, "- sinal repetido (já avisei)")
                else:
                    print(ativo, "- sem sinal de compra. Preço:", r["preco"],
                          "RSI:", round(r["rsi"]))

            except Exception as erro:
                print("Erro em", ativo, "(vou tentar de novo):", erro)

            time.sleep(1)

        time.sleep(config.INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    main()
