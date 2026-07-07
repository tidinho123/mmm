# 🤖 Bots de Sinais (Telegram)

Aqui tem **TRÊS bots**. Os dois primeiros leem os preços reais da
**Binance** (estratégia EMA9 + EMA200 + RSI + MACD). O terceiro é
diferente: ele **abre o Chrome**, lê o histórico do **Bac Bo (Bantubet)**
em tempo real e manda o **palpite da próxima rodada**. Todos avisam no
**Telegram**.

| Bot | Pra quê serve | Manda | Arquivo pra ligar |
|-----|---------------|-------|-------------------|
| **Quotex** | Opções binárias (Quotex) | CALL **e** PUT, com sugestão de expiração | `LIGAR_BOT_QUOTEX_windows.bat` |
| **Binance** | Comprar cripto de verdade (Spot) | **só** COMPRA (CALL), com Take Profit e Stop Loss | `LIGAR_BOT_BINANCE_windows.bat` |
| **Bac Bo** | Cassino ao vivo (Bantubet) | Palpite 🔴 Banca / 🔵 Player da **próxima rodada** | `LIGAR_BOT_BACBO_windows.bat` |

> Você pode ligar **um** ou **os dois** ao mesmo tempo. Cada bot tem o
> **seu próprio** Telegram: o token do Quotex vai no `config.py` e o do
> Binance vai no `config_binance.py`. Assim os sinais chegam separados.

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
- Para ter os sinais **separados**, crie **dois** robôs: um pro Quotex
  e outro pro Binance (cada um com seu token).

### 2. Instalar o Python
- Baixe em **python.org/downloads**.
- No Windows, na instalação, **marque a caixinha "Add Python to PATH"**.

### 3. Descobrir o seu Chat ID
- No Telegram, mande "oi" para o seu robô.
- Rode o arquivo **`pegar_meu_id.py`**.
- Ele mostra o seu número.

### 3.1. Colar o token e o chat id
- **Bot Quotex:** abra o **`config.py`** e cole o token e o chat id nas
  duas primeiras linhas (`TELEGRAM_TOKEN` e `TELEGRAM_CHAT_ID`).
- **Bot Binance:** abra o **`config_binance.py`** e faça o mesmo (de
  preferência com o token do **segundo** robô, pra ficar separado).
- **Não precisa criar nenhum arquivo novo.** Só editar esses que já existem.

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

---

## 🎲 Bot Bac Bo (Bantubet) — o que lê a tela

Este bot é **diferente** dos outros dois. Em vez de ler preços de cripto,
ele **abre um Chrome controlado por ele**, você faz login e abre o Bac Bo,
e ele fica **lendo o histórico de resultados** (🔴 Banca · 🔵 Player ·
🟡 Empate). A cada rodada nova ele aplica a estratégia que você escolher e
te manda no Telegram o **palpite da próxima rodada** — junto com um
**placar** de quantas ele acertou e errou, pra você medir na prática.

> ⚠️ **A verdade, sem enrolação:** Bac Bo é jogo de **dado**. Cada rodada é
> sorteada do zero e **não depende das anteriores**. Nenhum robô, padrão ou
> estratégia consegue prever o próximo resultado — isso é matemática, não
> opinião. Use este bot como **ferramenta de estudo e observação**, com
> dinheiro que você pode perder. Sinal **não** é garantia de lucro.

### Passo a passo do Bac Bo

**1. Python instalado** (mesmo do passo lá em cima). Ao ligar, ele instala
o Chrome-controlado (Selenium) sozinho.

**2. Crie um robô no Telegram** (via `@BotFather`) e pegue o **TOKEN**.
Cole no arquivo **`config_bacbo.py`** (linha `TELEGRAM_TOKEN`).

**3. Descubra seu Chat ID:** mande "oi" pro seu robô no Telegram e rode
**`pegar_meu_id_bacbo.py`**. Cole o número no `config_bacbo.py`.

**4. CALIBRAR (faça UMA vez):** dois cliques em **`CALIBRAR_BACBO_windows.bat`**
(ou `.sh` no Mac/Linux). Vai abrir o Chrome:
   - Faça **login** na Bantubet e abra o **Bac Bo**, com o histórico na tela.
   - Volte no cmd e aperte **ENTER**.
   - Ele varre a página e mostra **candidatos** com a "sequência lida"
     (🔴🔵🟡...). Escolha o que **bate com a tela** e cole as 2 linhas que
     ele sugere (`SELETOR_IFRAME` e `SELETOR_HISTORICO`) no `config_bacbo.py`.

**5. LIGAR:** dois cliques em **`LIGAR_BOT_BACBO_windows.bat`**. Faça login,
deixe o Bac Bo na tela, aperte ENTER no cmd e pronto — ele começa a mandar
os palpites no Telegram.

### O que você escolhe no `config_bacbo.py`

- **`ESTRATEGIA`** → como ele decide o palpite:
  - `"so_coletar"` → **não** dá palpite, só mostra o histórico (comece por aqui).
  - `"tendencia"` → quando uma cor repete muito, ele age (veja `MODO_TENDENCIA`
    = `"seguir"` a sequência ou apostar `"contra"` a quebra).
  - `"frequencia"` → aposta na cor que apareceu **menos** na janela.
  - `"alternancia"` → quando vem zig-zag (🔴🔵🔴🔵), sugere continuar.
- **`STREAK_MINIMO`** → quantas repetições contam como "sequência".
- **`FORCA_MINIMA`** → de quantas ⭐ pra cima ele te avisa (1 a 3).
- **`USAR_GALE`** → sugestão de valor da aposta (não muda a chance de ganhar!).

> 💡 Se ao ligar ele avisar que **não consegue ler o histórico**, é só rodar
> o **calibrar** de novo e conferir os seletores. Se a "sequência lida"
> aparecer com as cores **trocadas**, ajuste as listas `MARCADORES_...`.
