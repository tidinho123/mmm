#!/bin/bash
# Botao de LIGAR o BOT BINANCE (so COMPRA, com TP e SL) no Mac/Linux.

echo "Instalando o que o bot precisa (so demora na primeira vez)..."
pip3 install -r requirements.txt

echo ""
echo "Ligando o BOT BINANCE... (para desligar, aperte Ctrl + C)"
echo ""
python3 bot_binance.py
