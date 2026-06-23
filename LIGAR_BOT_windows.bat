@echo off
REM Este e o botao de LIGAR o bot no Windows.
REM E so dar dois cliques neste arquivo.

echo Instalando o que o bot precisa (so demora na primeira vez)...
python -m pip install -r requirements.txt

echo.
echo Ligando o bot... (para desligar, feche esta janela)
echo.
python bot.py

pause
