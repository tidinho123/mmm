# 🤖 Bot de Sinais (Telegram)

Bot que vigia **vários ativos ao mesmo tempo** (cripto, com dados reais da
Binance), aplica a **sua estratégia** e te **avisa no Telegram** quando
aparece um sinal de compra (CALL) ou de venda (PUT).

## 📈 A estratégia que está dentro do bot

> **A EMA200 diz a DIREÇÃO · a EMA9 diz a ZONA · a vela diz o SINAL.**

- **Sinal principal — Pullback:** quando o preço está acima da EMA200,
  recua, toca a EMA9 e fecha uma vela **verde** acima dela → **CALL**.
  (e o inverso, abaixo da EMA200 com vela **vermelha** → **PUT**).
- **Confirmação 1 — RSI:** o RSI virando a favor da tendência (saindo de
  70/30) dá mais força ao sinal.
- **Confirmação 2 — MACD:** a linha do MACD cruzando o sinal dá mais força.

Cada sinal vem com uma **força de ⭐ a ⭐⭐⭐**: quanto mais confirmações
batem juntas, mais estrelas. No `config.py` dá pra escolher só receber
sinais a partir de uma certa força.

> ⚠️ **Aviso honesto:** sinal **NÃO** é garantia de lucro. Opções binárias
> têm o jogo matematicamente contra o apostador. Use isto como ferramenta
> de **estudo e apoio**, com dinheiro que você pode perder. Nenhum bot
> prevê o futuro.

---

## Passo a passo (bem devagar)

### 1. Criar o robô no Telegram
- No Telegram, procure por **@BotFather**.
- Mande `/newbot` e siga as perguntas (nome do bot).
- Ele te dá um **TOKEN** (uma sequência tipo `123456:ABC-DEF...`).
- Cole esse token no arquivo **`config.py`**, na linha `TELEGRAM_TOKEN`.

### 2. Instalar o Python
- Baixe em **python.org/downloads**.
- No Windows, na instalação, **marque a caixinha "Add Python to PATH"**.

### 3. Descobrir o seu Chat ID
- No Telegram, mande "oi" para o seu robô.
- Rode o arquivo **`pegar_meu_id.py`**.
- Ele mostra o seu número. Cole no `config.py`, em `TELEGRAM_CHAT_ID`.

### 4. Ligar o bot
- **Windows:** dois cliques em **`LIGAR_BOT_windows.bat`**.
- **Mac/Linux:** rode **`LIGAR_BOT_mac_linux.sh`**.

Pronto! O bot manda "✅ Bot ligado!" no Telegram e começa a vigiar o gráfico.

---

## Onde eu mexo as coisas?
Só no arquivo **`config.py`**. Os outros não precisa tocar. Lá você
escolhe:
- **`ATIVOS`** → a lista de pares que o bot vigia (adicione ou remova).
- **`TEMPO_GRAFICO`** → o tempo do gráfico (sua estratégia é `"5m"`).
- **`FORCA_MINIMA`** → de quantas estrelas pra cima você quer ser avisado
  (`2` é o recomendado).
