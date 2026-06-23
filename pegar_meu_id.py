# ============================================================
#   AJUDANTE: descobre o seu CHAT ID do Telegram.
#
#   Como usar (eu te explico no passo a passo):
#     1. Já tenha colado seu TOKEN no arquivo config.py
#     2. No Telegram, mande qualquer mensagem (ex: "oi") para o
#        seu robô.
#     3. Rode este arquivo. Ele vai te mostrar o seu número.
# ============================================================

import requests
import config

url = "https://api.telegram.org/bot{}/getUpdates".format(config.TELEGRAM_TOKEN)
resposta = requests.get(url, timeout=15).json()

if not resposta.get("ok"):
    print("Algo deu errado. Confira se o TOKEN no config.py está certo.")
    print("Resposta:", resposta)
elif not resposta.get("result"):
    print("Não achei nenhuma mensagem.")
    print("=> Abra o Telegram, mande 'oi' para o seu robô e rode de novo.")
else:
    ultima = resposta["result"][-1]
    chat = ultima.get("message", {}).get("chat", {})
    chat_id = chat.get("id")
    nome = chat.get("first_name", "")
    print("---------------------------------------------")
    print("Achei! Olá,", nome)
    print("O SEU CHAT ID é:", chat_id)
    print("---------------------------------------------")
    print("Agora copie esse número e cole no arquivo config.py,")
    print("na linha do TELEGRAM_CHAT_ID (entre as aspas).")
