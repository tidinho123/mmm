@echo off
REM ====================================================
REM   LIGAR o BOT BAC BO (Bantubet) - manda palpite no Telegram
REM   E so dar dois cliques neste arquivo.
REM ====================================================

echo Instalando o que o bot precisa (so demora na primeira vez)...
python -m pip install -r requirements.txt

echo.
echo Ligando o BOT BAC BO... (para desligar, feche esta janela)
echo Vai abrir o Chrome. Faca login, abra o Bac Bo e volte aqui.
echo.
python bot_bacbo.py

pause
