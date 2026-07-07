#!/bin/bash
# CALIBRAR o BOT BAC BO no Mac/Linux (rode UMA VEZ antes de ligar o bot).

echo "Instalando o que precisa (so demora na primeira vez)..."
pip3 install -r requirements.txt

echo ""
echo "Abrindo o Chrome pra calibrar..."
echo "Faca login, abra o Bac Bo e siga as instrucoes no cmd."
echo ""
python3 calibrar_bacbo.py
