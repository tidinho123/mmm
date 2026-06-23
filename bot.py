# ============================================================
#   BOT DE SINAIS  -  Análise técnica + alertas no Telegram
#
#   VOCÊ NÃO PRECISA ENTENDER ESTE ARQUIVO.
#   Ele é o "cérebro" do bot. É só deixar ele aqui e rodar.
#
#   O que ele faz, em palavras simples:
#     1. Pega o preço real do ativo na Binance.
#     2. Calcula dois indicadores técnicos (médias móveis + RSI).
#     3. Quando aparece um sinal de ALTA ou de BAIXA,
#        ele te manda um aviso no Telegram.
#
#   AVISO IMPORTANTE: nenhum sinal é garantia de lucro.
#   Isto é uma ferramenta de ESTUDO e APOIO, não dinheiro fácil.
# ============================================================

import time
import requests
import config


# ---------- Funções que conversam com a internet ----------

def pegar_velas(ativo, tempo, quantidade=100):
    """Busca o histórico de preços (velas) na Binance."""
    url = "https://api.binance.com/api/v3/klines"
    parametros = {"symbol": ativo, "interval": tempo, "limit": quantidade}
    resposta = requests.get(url, params=parametros, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()
    # O preço de fechamento de cada vela fica na posição 4.
    fechamentos = [float(vela[4]) for vela in dados]
    return fechamentos


def enviar_telegram(mensagem):
    """Envia uma mensagem para o seu Telegram."""
    url = "https://api.telegram.org/bot{}/sendMessage".format(config.TELEGRAM_TOKEN)
    parametros = {"chat_id": config.TELEGRAM_CHAT_ID, "text": mensagem}
    try:
        requests.get(url, params=parametros, timeout=15)
    except Exception as erro:
        print("Não consegui enviar no Telegram:", erro)


# ---------- Contas dos indicadores técnicos ----------

def media_movel_exponencial(valores, periodo):
    """Calcula a EMA (média móvel exponencial)."""
    k = 2 / (periodo + 1)
    ema = valores[0]
    for preco in valores[1:]:
        ema = preco * k + ema * (1 - k)
    return ema


def calcular_rsi(valores, periodo=14):
    """Calcula o RSI (força do movimento, de 0 a 100)."""
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


# ---------- A estratégia (quando dar o sinal) ----------

def analisar(fechamentos):
    """
    Decide se há sinal. Regra simples e clássica:
      - Média curta (9) acima da longa (21) + força (RSI) > 50  -> ALTA (CALL)
      - Média curta (9) abaixo da longa (21) + RSI < 50         -> BAIXA (PUT)
    Retorna "ALTA", "BAIXA" ou None (sem sinal).
    """
    ema_curta = media_movel_exponencial(fechamentos[-30:], 9)
    ema_longa = media_movel_exponencial(fechamentos[-30:], 21)
    rsi = calcular_rsi(fechamentos, 14)

    if ema_curta > ema_longa and rsi > 50:
        return "ALTA", rsi
    if ema_curta < ema_longa and rsi < 50:
        return "BAIXA", rsi
    return None, rsi


# ---------- O "loop" principal: roda pra sempre ----------

def main():
    print("Bot ligado! Analisando", config.ATIVO, "no tempo", config.TEMPO_GRAFICO)
    enviar_telegram(
        "✅ Bot ligado! Vou analisar {} ({}) e te avisar quando "
        "aparecer um sinal.\n\n⚠️ Lembre-se: sinal NÃO é garantia. "
        "Opere com responsabilidade.".format(config.ATIVO, config.TEMPO_GRAFICO)
    )

    ultimo_sinal = None  # pra não repetir o mesmo aviso toda hora

    while True:
        try:
            fechamentos = pegar_velas(config.ATIVO, config.TEMPO_GRAFICO)
            sinal, rsi = analisar(fechamentos)
            preco_atual = fechamentos[-1]

            if sinal and sinal != ultimo_sinal:
                if sinal == "ALTA":
                    texto = (
                        "🟢 SINAL DE ALTA (COMPRA / CALL)\n"
                        "Ativo: {}\n"
                        "Tempo do gráfico: {}\n"
                        "Preço agora: {}\n"
                        "RSI: {:.0f}\n\n"
                        "👉 Sugestão de expiração: 1 vela ({})\n"
                        "⚠️ Confira no seu gráfico antes de operar."
                    ).format(config.ATIVO, config.TEMPO_GRAFICO,
                             preco_atual, rsi, config.TEMPO_GRAFICO)
                else:
                    texto = (
                        "🔴 SINAL DE BAIXA (VENDA / PUT)\n"
                        "Ativo: {}\n"
                        "Tempo do gráfico: {}\n"
                        "Preço agora: {}\n"
                        "RSI: {:.0f}\n\n"
                        "👉 Sugestão de expiração: 1 vela ({})\n"
                        "⚠️ Confira no seu gráfico antes de operar."
                    ).format(config.ATIVO, config.TEMPO_GRAFICO,
                             preco_atual, rsi, config.TEMPO_GRAFICO)

                enviar_telegram(texto)
                print("Sinal enviado:", sinal)
                ultimo_sinal = sinal
            else:
                print("Sem sinal novo. Preço:", preco_atual, "RSI:", round(rsi))

        except Exception as erro:
            print("Deu um erro nesta rodada (vou tentar de novo):", erro)

        time.sleep(config.INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    main()
