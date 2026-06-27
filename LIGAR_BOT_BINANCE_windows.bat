@echo off
REM ====================================================
REM   LIGAR o BOT BINANCE (so COMPRA, com TP e SL)
REM   E so dar dois cliques neste arquivo.
REM ====================================================

echo Instalando o que o bot precisa (so demora na primeira vez)...
python -m pip install -r requirements.txt

echo.
echo Ligando o BOT BINANCE... (para desligar, feche esta janela)
echo.
python bot_binance.py

pause
