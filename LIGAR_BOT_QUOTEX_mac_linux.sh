#!/bin/bash
# Botao de LIGAR o BOT QUOTEX (opcoes binarias: CALL e PUT) no Mac/Linux.

echo "Instalando o que o bot precisa (so demora na primeira vez)..."
pip3 install -r requirements.txt

echo ""
echo "Ligando o BOT QUOTEX... (para desligar, aperte Ctrl + C)"
echo ""
python3 bot.py
