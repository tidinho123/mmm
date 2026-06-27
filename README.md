# 🤖 Bots de Sinais (Telegram)

Aqui tem **DOIS bots**, cada um pra um jeito de operar. Os dois leem os
preços reais da **Binance**, aplicam a **mesma estratégia** (EMA9 + EMA200
+ RSI + MACD) e te **avisam no Telegram**.

| Bot | Pra quê serve | Manda | Arquivo pra ligar |
|-----|---------------|-------|-------------------|
| **Quotex** | Opções binárias (Quotex) | CALL **e** PUT, com sugestão de expiração | `LIGAR_BOT_QUOTEX_windows.bat` |
| **Binance** | Comprar cripto de verdade (Spot) | **só** COMPRA (CALL), com Take Profit e Stop Loss | `LIGAR_BOT_BINANCE_windows.bat` |

> Você pode ligar **um** ou **os dois** ao mesmo tempo. Os dois usam o
> mesmo Telegram (mesmo arquivo `MEUS_DADOS.py`).

## 📈 A estratégia que está dentro dos bots

> **A EMA200 diz a DIREÇÃO · a EMA9 diz a ZONA · a vela diz o SINAL.**

- **Sinal principal — Pullback:** quando o preço está acima da EMA200,
  recua, toca a EMA9 e fecha uma vela **verde** acima dela → **CALL**.
  (e o inverso, abaixo da EMA200 com vela **vermelha** → **PUT**).
- **Confirmação 1 — RSI:** o RSI virando a favor da tendência (saindo de
  70/30) dá mais força ao sinal.
- **Confirmação 2 — MACD:** a linha do MACD cruzando o sinal dá mais força.

Cada sinal vem com uma **força de ⭐ a ⭐⭐⭐**: quanto mais confirmações
batem juntas, mais estrelas.

> ⚠️ **Aviso honesto:** sinal **NÃO** é garantia de lucro. Use isto como
> ferramenta de **estudo e apoio**, com dinheiro que você pode perder.
> Nenhum bot prevê o futuro.

---

## Passo a passo (bem devagar)

### 1. Criar o robô no Telegram
- No Telegram, procure por **@BotFather**.
- Mande `/newbot` e siga as perguntas (nome do bot).
- Ele te dá um **TOKEN** (uma sequência tipo `123456:ABC-DEF...`).
- Faça uma cópia do **`MEUS_DADOS_EXEMPLO.py`** com o nome
  **`MEUS_DADOS.py`** e cole esse token na linha `TELEGRAM_TOKEN`.

### 2. Instalar o Python
- Baixe em **python.org/downloads**.
- No Windows, na instalação, **marque a caixinha "Add Python to PATH"**.

### 3. Descobrir o seu Chat ID
- No Telegram, mande "oi" para o seu robô.
- Rode o arquivo **`pegar_meu_id.py`**.
- Ele mostra o seu número. Cole no `MEUS_DADOS.py`, em `TELEGRAM_CHAT_ID`.

### 4. Ligar o bot que você quer
- **Bot Quotex (CALL e PUT):** dois cliques em
  **`LIGAR_BOT_QUOTEX_windows.bat`**.
- **Bot Binance (só compra, com TP/SL):** dois cliques em
  **`LIGAR_BOT_BINANCE_windows.bat`**.

Pronto! O bot manda "✅ Bot ligado!" no Telegram e começa a vigiar.

---

## Onde eu mexo as coisas?

- **Bot Quotex** → arquivo **`config.py`**
- **Bot Binance** → arquivo **`config_binance.py`**

Em cada um você escolhe:
- **`ATIVOS`** → a lista de pares que o bot vigia (adicione ou remova).
  No Quotex, confira se o ativo existe na **sua** Quotex.
- **`TEMPO_GRAFICO`** → o tempo do gráfico (Quotex usa `"5m"`,
  Binance usa `"15m"`).
- **`FORCA_MINIMA`** → de quantas estrelas pra cima você quer ser avisado
  (`2` é o recomendado).

Só no bot Binance (`config_binance.py`) você ainda tem:
- **`TAKE_PROFIT_PCT`** → onde vender no lucro (ex: `1.0` = +1%).
- **`STOP_LOSS_PCT`** → onde sair no prejuízo (ex: `0.5` = -0.5%).
