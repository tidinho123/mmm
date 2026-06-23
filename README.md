# 🤖 Bot de Sinais (Telegram)

Bot simples que analisa o gráfico de um ativo (cripto, com dados reais da
Binance), calcula indicadores técnicos e te **avisa no Telegram** quando
aparece um sinal de alta ou de baixa.

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
Só no arquivo **`config.py`**. Os outros não precisa tocar.
