#!/bin/bash
# Este e o botao de LIGAR o bot no Mac/Linux.

echo "Instalando o que o bot precisa (so demora na primeira vez)..."
pip3 install -r requirements.txt

echo ""
echo "Ligando o bot... (para desligar, aperte Ctrl + C)"
echo ""
python3 bot.py
