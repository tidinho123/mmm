# ============================================================
#   BOT DE SINAIS  -  Sua estratégia + alertas no Telegram
#
#   VOCÊ NÃO PRECISA ENTENDER ESTE ARQUIVO.
#   Ele é o "cérebro" do bot. É só deixar ele aqui e rodar.
#   (Pra mexer nas configurações, abra o arquivo  config.py )
#
#   SUA ESTRATÉGIA, do seu jeito:
#     "A EMA200 diz a DIREÇÃO, a EMA9 diz a ZONA, a vela diz o SINAL."
#
#   Ela tem 3 gatilhos:
#     A) PULLBACK: preço acima da EMA200, recua, toca a EMA9 e
#        fecha uma vela VERDE acima da EMA9  -> CALL (compra).
#        (e o inverso, abaixo da EMA200, vela vermelha -> PUT)
#     B) RSI: na direção da tendência, o RSI chega no extremo
#        (70 ou 30) e VIRA, com vela confirmando -> confirma o sinal.
#     C) MACD: a linha do MACD cruza a linha de sinal -> confirma.
#
#   O gatilho A é o sinal PRINCIPAL. B e C entram como CONFIRMAÇÃO
#   e viram "estrelas de força" (⭐ a ⭐⭐⭐).
#
#   AVISO IMPORTANTE: nenhum sinal é garantia de lucro.
#   Isto é uma ferramenta de ESTUDO e APOIO, não dinheiro fácil.
# ============================================================

import time
import requests
import config


# ---------- Funções que conversam com a internet ----------

def pegar_velas(ativo, tempo, quantidade=300):
    """Busca o histórico de velas (OHLC) na Binance.

    Retorna uma lista de velas, cada uma assim:
      {"abertura":.., "maxima":.., "minima":.., "fechamento":.., "hora":..}
    """
    url = "https://api.binance.com/api/v3/klines"
    parametros = {"symbol": ativo, "interval": tempo, "limit": quantidade}
    resposta = requests.get(url, params=parametros, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()
    velas = []
    for v in dados:
        velas.append({
            "hora": v[0],                 # horário de abertura da vela
            "abertura": float(v[1]),
            "maxima": float(v[2]),
            "minima": float(v[3]),
            "fechamento": float(v[4]),
        })
    # A última vela ainda está "se formando" (não fechou). Pra estratégia
    # valer, a gente trabalha sempre com a ÚLTIMA VELA JÁ FECHADA.
    # Por isso descartamos a última (incompleta).
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
    """Calcula a EMA passo a passo e devolve a LISTA inteira
    (um valor de EMA pra cada preço). Assim dá pra ver se a EMA
    está subindo ou descendo comparando o último com o anterior."""
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
    """MACD clássico (12, 26, 9).
    Retorna (macd_agora, sinal_agora, macd_antes, sinal_antes)
    pra dar pra ver o cruzamento entre a vela atual e a anterior."""
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
    """
    Aplica a sua estratégia na última vela fechada.
    Retorna um dicionário com o resultado, ou None se faltar dado.
    """
    if len(velas) < config.EMA_LENTA + 5:
        return None

    fechamentos = [v["fechamento"] for v in velas]

    ema9 = ema_serie(fechamentos, config.EMA_RAPIDA)
    ema200 = ema_serie(fechamentos, config.EMA_LENTA)
    macd_agora, sinal_agora, macd_antes, sinal_antes = calcular_macd(fechamentos)

    rsi_agora = calcular_rsi(fechamentos, config.RSI_PERIODO)
    rsi_antes = calcular_rsi(fechamentos[:-1], config.RSI_PERIODO)

    # A vela que vamos avaliar é a última fechada.
    vela = velas[-1]
    e9 = ema9[-1]
    e200 = ema200[-1]
    e9_antes = ema9[-2]

    verde = vela["fechamento"] > vela["abertura"]
    vermelha = vela["fechamento"] < vela["abertura"]

    # Tocou a EMA9? (a sombra/preço da vela passou pela EMA9)
    tocou_ema9 = vela["minima"] <= e9 <= vela["maxima"]

    direcao = None        # "CALL" ou "PUT"
    confirmacoes = []     # lista de textos das confirmações que bateram

    # ---------------- GATILHO A: PULLBACK (sinal principal) ----------
    # CALL: acima da EMA200, recuou e tocou a EMA9, fechou VERDE acima da EMA9
    if (vela["fechamento"] > e200 and tocou_ema9
            and vela["fechamento"] > e9 and verde):
        direcao = "CALL"
    # PUT: abaixo da EMA200, subiu e tocou a EMA9, fechou VERMELHO abaixo da EMA9
    elif (vela["fechamento"] < e200 and tocou_ema9
            and vela["fechamento"] < e9 and vermelha):
        direcao = "PUT"

    # Sem o gatilho principal, não há sinal.
    if direcao is None:
        return {
            "sinal": None,
            "preco": vela["fechamento"],
            "rsi": rsi_agora,
            "ema9": e9, "ema200": e200,
            "hora": vela["hora"],
        }

    # ---------------- GATILHO B: RSI a favor da tendência ------------
    # CALL: RSI saindo da sobrevenda (estava esticado pra baixo e virou pra cima)
    if direcao == "CALL":
        if rsi_antes <= config.RSI_SOBREVENDA and rsi_agora > rsi_antes:
            confirmacoes.append("RSI saindo da sobrevenda (virou pra cima)")
        elif rsi_agora > 50:
            confirmacoes.append("RSI a favor (acima de 50)")
    else:  # PUT
        if rsi_antes >= config.RSI_SOBRECOMPRA and rsi_agora < rsi_antes:
            confirmacoes.append("RSI saindo da sobrecompra (virou pra baixo)")
        elif rsi_agora < 50:
            confirmacoes.append("RSI a favor (abaixo de 50)")

    # ---------------- GATILHO C: cruzamento do MACD ------------------
    cruzou_cima = macd_antes <= sinal_antes and macd_agora > sinal_agora
    cruzou_baixo = macd_antes >= sinal_antes and macd_agora < sinal_agora
    if direcao == "CALL":
        if cruzou_cima:
            confirmacoes.append("MACD cruzou pra cima")
        elif macd_agora > sinal_agora:
            confirmacoes.append("MACD a favor (acima do sinal)")
    else:  # PUT
        if cruzou_baixo:
            confirmacoes.append("MACD cruzou pra baixo")
        elif macd_agora < sinal_agora:
            confirmacoes.append("MACD a favor (abaixo do sinal)")

    # Confirmação extra: a EMA9 está apontando na direção certa?
    if direcao == "CALL" and e9 > e9_antes:
        confirmacoes.append("EMA9 subindo")
    if direcao == "PUT" and e9 < e9_antes:
        confirmacoes.append("EMA9 descendo")

    # Força = 1 estrela pelo gatilho principal + 1 por confirmação (máx 3).
    forca = 1 + len([c for c in confirmacoes
                     if "RSI" in c or "MACD cruzou" in c])
    forca = min(forca, 3)

    return {
        "sinal": direcao,
        "forca": forca,
        "confirmacoes": confirmacoes,
        "preco": vela["fechamento"],
        "rsi": rsi_agora,
        "ema9": e9, "ema200": e200,
        "hora": vela["hora"],
    }


# ---------- Montagem da mensagem ----------

def montar_mensagem(ativo, r):
    direcao = r["sinal"]
    estrelas = "⭐" * r["forca"]
    preco = r["preco"]

    if direcao == "CALL":
        topo = "🟢 SINAL DE COMPRA (CALL)"
    else:
        topo = "🔴 SINAL DE VENDA (PUT)"

    linhas = [
        topo,
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

    linhas += ["", "RSI: {:.0f}".format(r["rsi"])]

    # --- Plano de operação na Binance Spot (só faz sentido na COMPRA) ---
    if direcao == "CALL":
        take_profit = preco * (1 + config.TAKE_PROFIT_PCT / 100)
        stop_loss = preco * (1 - config.STOP_LOSS_PCT / 100)
        linhas += [
            "",
            "📋 PLANO (Binance Spot):",
            "1) COMPRAR perto de {:.6g}".format(preco),
            "2) 🎯 Vender no LUCRO (Take Profit): {:.6g}  (+{:.1f}%)".format(
                take_profit, config.TAKE_PROFIT_PCT),
            "3) 🛑 Sair no PREJUÍZO (Stop Loss): {:.6g}  (-{:.1f}%)".format(
                stop_loss, config.STOP_LOSS_PCT),
            "(Dica: use uma ordem OCO pra deixar o TP e o SL automáticos.)",
        ]
    else:
        linhas += [
            "",
            "⚠️ Sinal de QUEDA. Na Binance Spot NÃO dá pra ganhar na queda.",
            "Serve só como aviso: NÃO é hora de comprar.",
            "(Se você já tem esse ativo, pode ser hora de vender.)",
        ]

    linhas.append(
        "⚠️ Confira no seu gráfico antes de operar. Sinal não é garantia.")
    return "\n".join(linhas)


# ---------- O "loop" principal: roda pra sempre ----------

def main():
    print("Bot ligado! Vigiando", len(config.ATIVOS),
          "ativos no tempo", config.TEMPO_GRAFICO)
    if config.SO_COMPRA:
        modo = ("Modo Binance Spot: só vou te avisar de sinais de COMPRA "
                "(🟢 CALL), já com sugestão de Take Profit e Stop Loss.")
    else:
        modo = "Vou te avisar de sinais de COMPRA (CALL) e VENDA (PUT)."
    enviar_telegram(
        "✅ Bot ligado!\nVou vigiar {} ativos no gráfico de {}.\n{}\n\n"
        "Estratégia: EMA9 + EMA200 + RSI + MACD.\n\n⚠️ Lembre-se: sinal "
        "NÃO é garantia. Opere com responsabilidade.".format(
            len(config.ATIVOS), config.TEMPO_GRAFICO, modo)
    )

    # Pra não repetir o mesmo aviso: guardamos, por ativo, qual foi a
    # última vela (hora) e direção que já avisamos.
    ja_avisado = {}

    while True:
        for ativo in config.ATIVOS:
            try:
                velas = pegar_velas(ativo, config.TEMPO_GRAFICO)
                r = analisar(velas)
                if r is None:
                    print(ativo, "- sem dados suficientes ainda")
                    continue

                # No "modo Binance" (SO_COMPRA), ignoramos os sinais de
                # PUT, porque no Spot não dá pra lucrar na queda.
                if (config.SO_COMPRA and r["sinal"] == "PUT"):
                    print(ativo, "- sinal PUT ignorado (modo Binance/só compra)")
                    continue

                if r["sinal"] and r["forca"] >= config.FORCA_MINIMA:
                    chave = (r["hora"], r["sinal"])
                    if ja_avisado.get(ativo) != chave:
                        enviar_telegram(montar_mensagem(ativo, r))
                        ja_avisado[ativo] = chave
                        print(">>> SINAL", r["sinal"], ativo,
                              "força", r["forca"])
                    else:
                        print(ativo, "- sinal repetido (já avisei)")
                else:
                    print(ativo, "- sem sinal. Preço:", r["preco"],
                          "RSI:", round(r["rsi"]))

            except Exception as erro:
                print("Erro em", ativo, "(vou tentar de novo):", erro)

            # pausinha entre um ativo e outro pra não sobrecarregar a Binance
            time.sleep(1)

        time.sleep(config.INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    main()
