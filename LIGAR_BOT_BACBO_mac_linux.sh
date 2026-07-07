#!/bin/bash
# Botao de LIGAR o BOT BAC BO (Bantubet) no Mac/Linux.

echo "Instalando o que o bot precisa (so demora na primeira vez)..."
pip3 install -r requirements.txt

echo ""
echo "Ligando o BOT BAC BO... (para desligar, aperte Ctrl + C)"
echo "Vai abrir o Chrome. Faca login, abra o Bac Bo e volte aqui."
echo ""
python3 bot_bacbo.py
