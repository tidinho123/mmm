@echo off
REM ====================================================
REM   LIGAR o BOT QUOTEX (opcoes binarias: CALL e PUT)
REM   E so dar dois cliques neste arquivo.
REM ====================================================

echo Instalando o que o bot precisa (so demora na primeira vez)...
python -m pip install -r requirements.txt

echo.
echo Ligando o BOT QUOTEX... (para desligar, feche esta janela)
echo.
python bot.py

pause
