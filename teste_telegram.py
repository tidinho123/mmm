#!/usr/bin/env python3
# Quick test to verify Telegram bot connection

import requests
import config_binance as config

print("Testing Telegram connection...")
print(f"Token: {config.TELEGRAM_TOKEN}")
print(f"Chat ID: {config.TELEGRAM_CHAT_ID}")
print()

# Test 1: Try to get bot info
url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/getMe"
try:
    resposta = requests.get(url, timeout=10)
    print(f"Bot Info Status: {resposta.status_code}")
    print(f"Response: {resposta.json()}")
    print()
except Exception as e:
    print(f"Error getting bot info: {e}")
    print()

# Test 2: Try to send a test message
url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
parametros = {
    "chat_id": config.TELEGRAM_CHAT_ID,
    "text": "🟢 Teste de conexão - Bot Binance funcionando!"
}
try:
    resposta = requests.get(url, params=parametros, timeout=10)
    print(f"Send Message Status: {resposta.status_code}")
    print(f"Response: {resposta.json()}")
except Exception as e:
    print(f"Error sending message: {e}")
