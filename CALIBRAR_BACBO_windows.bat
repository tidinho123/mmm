@echo off
REM ====================================================
REM   CALIBRAR o BOT BAC BO - acha os resultados na tela
REM   Rode ISTO UMA VEZ antes de ligar o bot, pra ele
REM   saber ONDE estao as bolinhas de resultado.
REM ====================================================

echo Instalando o que precisa (so demora na primeira vez)...
python -m pip install -r requirements.txt

echo.
echo Abrindo o Chrome pra calibrar...
echo Faca login, abra o Bac Bo e siga as instrucoes no cmd.
echo.
python calibrar_bacbo.py

pause
