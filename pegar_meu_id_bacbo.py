# ============================================================
#   AJUDANTE: descobre o seu CHAT ID do Telegram (bot BAC BO).
#
#   Como usar:
#     1. Cole o TOKEN do seu bot no  config_bacbo.py
#     2. No Telegram, mande "oi" para o seu robô.
#     3. Rode este arquivo. Ele mostra o seu número (CHAT ID).
#     4. Cole esse número no config_bacbo.py (TELEGRAM_CHAT_ID).
# ============================================================

import requests
import config_bacbo as cfg

url = "https://api.telegram.org/bot{}/getUpdates".format(cfg.TELEGRAM_TOKEN)
resposta = requests.get(url, timeout=15).json()

if not resposta.get("ok"):
    print("Algo deu errado. Confira se o TOKEN no config_bacbo.py está certo.")
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
    print("Cole esse número no config_bacbo.py, na linha TELEGRAM_CHAT_ID.")
