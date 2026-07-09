# ============================================================
#   BOT BAC BO (Bantubet)  -  lê o histórico e manda o palpite
#
#   O QUE ELE FAZ, em ordem:
#     1. Abre o Chrome (controlado por ele).
#     2. ESPERA você fazer login e abrir o Bac Bo na tela.
#     3. Lê a tirinha de resultados (🔴 Banca / 🔵 Player / 🟡 Empate).
#     4. Toda vez que sai uma rodada NOVA, aplica a estratégia do
#        config_bacbo.py e te manda no Telegram o palpite da PRÓXIMA.
#     5. Vai contando quantas ele acertou/errou (placar) pra você medir.
#
#   VOCÊ NÃO PRECISA ENTENDER ESTE ARQUIVO. Pra mexer nas coisas,
#   abra o  config_bacbo.py . Pra achar os resultados na tela, rode
#   antes o  calibrar_bacbo.py  (ele te diz o que colar no config).
#
#   AVISO: dado é dado. Nenhum sinal é garantia. Estude, não confie cego.
# ============================================================

import re
import time
import requests
import config_bacbo as cfg

# O Selenium é quem controla o Chrome. Se der erro aqui, é porque falta
# instalar: rode  pip install -r requirements.txt  (ou use o LIGAR_... ).
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
except Exception:
    print("Faltou instalar o Selenium. Rode:  pip install -r requirements.txt")
    raise


# ---------- Telegram ----------

def enviar_telegram(mensagem):
    """Manda uma mensagem pro seu Telegram. Se a internet falhar,
    tenta de novo até 3 vezes antes de desistir (rede fraca acontece)."""
    url = "https://api.telegram.org/bot{}/sendMessage".format(cfg.TELEGRAM_TOKEN)
    dados = {"chat_id": cfg.TELEGRAM_CHAT_ID, "text": mensagem}
    for tentativa in range(3):
        try:
            requests.post(url, data=dados, timeout=15)
            return
        except Exception as erro:
            if tentativa < 2:
                print("Telegram falhou (rede?). Tentando de novo...")
                time.sleep(2 * (tentativa + 1))
            else:
                print("Não consegui enviar no Telegram:", erro)


def telegram_configurado():
    """True se você já colou um token e chat id de verdade no config."""
    t = str(cfg.TELEGRAM_TOKEN)
    c = str(cfg.TELEGRAM_CHAT_ID)
    return bool(t and c and "COLE_AQUI" not in t and "COLE_AQUI" not in c)


def avisar(mensagem):
    """Mostra o aviso SEMPRE no cmd (num quadro, pra destacar) e, se o
    Telegram estiver configurado, manda lá também. Assim o bot funciona
    mesmo SEM Telegram — os palpites aparecem aqui na tela."""
    print("\n" + "=" * 60)
    print(mensagem)
    print("=" * 60 + "\n")
    if telegram_configurado():
        enviar_telegram(mensagem)


# ---------- Abrir o navegador ----------

def iniciar_navegador():
    """Abre um Chrome controlado pelo bot, guardando o seu login numa
    pasta (assim você não precisa logar toda vez)."""
    import os
    opcoes = Options()

    # Guarda o login numa pasta ao lado do bot.
    pasta = os.path.abspath(cfg.PASTA_PERFIL)
    opcoes.add_argument("--user-data-dir=" + pasta)
    opcoes.add_argument("--start-maximized")
    # Deixa o Chrome menos "cara de robô".
    opcoes.add_argument("--disable-blink-features=AutomationControlled")
    opcoes.add_experimental_option("excludeSwitches", ["enable-automation"])
    opcoes.add_experimental_option("useAutomationExtension", False)
    # NÃO deixa o Chrome "congelar" a página quando a janela fica atrás
    # de outra (senão o jogo para de atualizar quando você sai da frente).
    opcoes.add_argument("--disable-background-timer-throttling")
    opcoes.add_argument("--disable-backgrounding-occluded-windows")
    opcoes.add_argument("--disable-renderer-backgrounding")

    if cfg.CAMINHO_CHROME:
        opcoes.binary_location = cfg.CAMINHO_CHROME

    # O Selenium 4 baixa/gerencia o driver do Chrome sozinho.
    driver = webdriver.Chrome(options=opcoes)
    try:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": (
                # menos "cara de robô"
                "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"
                # o site sempre acha que está VISÍVEL, mesmo minimizado —
                # senão o jogo pausa o histórico quando você troca de janela
                "Object.defineProperty(document,'visibilityState',{get:()=>'visible'});"
                "Object.defineProperty(document,'hidden',{get:()=>false});"
                "window.addEventListener('visibilitychange',"
                "e=>e.stopImmediatePropagation(),true);"
            )},
        )
    except Exception:
        pass
    return driver


def esperar_voce_abrir_o_jogo(driver):
    """Abre o site e espera VOCÊ logar e deixar o Bac Bo na tela."""
    driver.get(cfg.URL_JOGO)
    print("=" * 60)
    print(" 1) Faça LOGIN na Bantubet nesta janela do Chrome.")
    print(" 2) Abra o jogo BAC BO e deixe o histórico aparecendo.")
    print(" 3) Volte AQUI no cmd e aperte ENTER pra começar a ler.")
    print("=" * 60)
    try:
        input(">>> Quando o Bac Bo estiver na tela, aperte ENTER aqui... ")
    except EOFError:
        # Ambiente sem teclado (raro): espera um tempão e segue.
        time.sleep(30)


# ---------- Ler os resultados da tela ----------

def _bate(marcador, texto, palavras):
    """Um marcador de UMA letra (ex: 't') só vale se for uma PALAVRA
    inteira sozinha (a bolinha escrita só 'T'). Se valesse como pedaço,
    't' combinaria com qualquer texto — foi um bug que já mordeu a gente."""
    if len(marcador) == 1:
        return marcador in palavras
    return marcador in texto


def _classificar(texto):
    """Recebe um punhado de texto/classe de um elemento e devolve
    'B' (Banca), 'P' (Player), 'T' (Empate) ou None se não reconhecer."""
    t = (texto or "").lower()
    palavras = set(re.findall(r"[a-z0-9]+", t))
    # Empate primeiro (costuma ser o mais específico).
    for m in cfg.MARCADORES_EMPATE:
        if m and _bate(m, t, palavras):
            return "T"
    for m in cfg.MARCADORES_BANCA:
        if m and _bate(m, t, palavras):
            return "B"
    for m in cfg.MARCADORES_PLAYER:
        if m and _bate(m, t, palavras):
            return "P"
    return None


def _texto_do_elemento(el):
    """Junta tudo que ajuda a reconhecer a cor: classe, texto, title,
    alt e a cor de fundo — num tijolão de texto só."""
    pedacos = []
    for attr in ("class", "title", "alt", "aria-label", "data-role", "data-result"):
        try:
            v = el.get_attribute(attr)
            if v:
                pedacos.append(v)
        except Exception:
            pass
    try:
        if el.text:
            pedacos.append(el.text)
    except Exception:
        pass
    if cfg.LER_DE in ("auto", "cor"):
        try:
            cor = el.value_of_css_property("background-color") or ""
            pedacos.append(_cor_para_palavra(cor))
        except Exception:
            pass
    return " ".join(pedacos)


def _cor_para_palavra(rgb):
    """Transforma 'rgb(200, 30, 30)' em 'vermelho'/'azul'/'verde' pra
    ajudar o reconhecimento quando a cor é o único sinal."""
    try:
        nums = rgb[rgb.find("(") + 1:rgb.find(")")].split(",")
        r, g, b = (int(float(nums[0])), int(float(nums[1])), int(float(nums[2])))
    except Exception:
        return ""
    if r > g and r > b:
        return "vermelho"
    if b > r and b > g:
        return "azul"
    if g > r and g > b:
        return "verde"
    return ""


# --- Auto-detecção: o bot acha o histórico na tela SOZINHO ---
# Assim você não precisa colar seletor nenhum no config. Ele guarda aqui
# o que descobriu (em qual iframe e qual elemento) pra reusar nas leituras.
_IFRAME_ATIVO = None
_SELETOR_ATIVO = None


def markers():
    """As palavras que identificam cada cor, tudo minúsculo (pro JS usar)."""
    return {
        "banca": [m.lower() for m in cfg.MARCADORES_BANCA],
        "player": [m.lower() for m in cfg.MARCADORES_PLAYER],
        "empate": [m.lower() for m in cfg.MARCADORES_EMPATE],
    }


# JavaScript que roda DENTRO da página e procura a tirinha de resultados.
# Devolve os melhores "candidatos" (elementos cujos filhos parecem bolinhas).
JS_PROCURAR = r"""
var MARK = arguments[0];

function corPorFundo(el){
  try{
    var bg = getComputedStyle(el).backgroundColor || "";
    var m = bg.match(/\d+/g);
    if(m && m.length >= 3){
      var r=+m[0], g=+m[1], b=+m[2];
      if(r>g && r>b) return " vermelho";
      if(b>r && b>g) return " azul";
      if(g>r && g>b) return " verde";
    }
  }catch(e){}
  return "";
}
function textoDe(el){
  var s = " " + (el.className || "");
  ["title","alt","aria-label","data-role","data-result"].forEach(function(a){
    var v = el.getAttribute && el.getAttribute(a);
    if(v) s += " " + v;
  });
  if(el.textContent) s += " " + el.textContent;
  s += corPorFundo(el);
  return s.toLowerCase();
}
function bate(m, s, toks){
  // Marcador de 1 letra so vale como PALAVRA inteira (bolinha escrita "T").
  if(m.length === 1) return toks.indexOf(m) >= 0;
  return s.indexOf(m) >= 0;
}
function classifica(s){
  var toks = s.split(/[^a-z0-9]+/);
  for(var i=0;i<MARK.empate.length;i++)
    if(MARK.empate[i] && bate(MARK.empate[i], s, toks)) return "T";
  for(var i=0;i<MARK.banca.length;i++)
    if(MARK.banca[i] && bate(MARK.banca[i], s, toks)) return "B";
  for(var i=0;i<MARK.player.length;i++)
    if(MARK.player[i] && bate(MARK.player[i], s, toks)) return "P";
  return null;
}
function classificaFundo(el){
  var c = classifica(textoDe(el));
  if(c) return c;
  var kids = el.querySelectorAll("*");
  for(var i=0;i<kids.length && i<6;i++){
    c = classifica(textoDe(kids[i]));
    if(c) return c;
  }
  return null;
}
function seletorDe(el){
  if(el.id) return "#" + CSS.escape(el.id);
  var partes = [];
  while(el && el.nodeType===1 && el.tagName.toLowerCase()!=="html"){
    if(el.id){ partes.unshift("#"+CSS.escape(el.id)); break; }
    var idx=1, sib=el;
    while(sib.previousElementSibling){ sib=sib.previousElementSibling; idx++; }
    partes.unshift(el.tagName.toLowerCase()+":nth-child("+idx+")");
    el = el.parentNode;
  }
  return partes.join(" > ");
}
function profundidade(el){ var d=0; while(el){ d++; el=el.parentNode; } return d; }

var todos = document.querySelectorAll("*");
var cands = [];
for(var i=0;i<todos.length;i++){
  var el = todos[i], kids = el.children;
  if(!kids || kids.length < 6) continue;
  var seq = [], match = 0;
  for(var j=0;j<kids.length;j++){
    var c = classificaFundo(kids[j]);
    if(c){ match++; seq.push(c); }
  }
  if(match >= 6){
    var temB = seq.indexOf("B") >= 0, temP = seq.indexOf("P") >= 0;
    cands.push({sel: seletorDe(el), total: kids.length,
                match: match, prof: profundidade(el), seq: seq.join(""),
                mix: (temB && temP) ? 1 : 0});
  }
}
// Um historico REAL tem Banca E Player misturados. Candidato que so tem
// uma cor (ou so empate) quase sempre e um elemento errado da pagina.
cands.sort(function(a,b){
  if(b.mix !== a.mix) return b.mix - a.mix;
  if(b.match !== a.match) return b.match - a.match;
  return b.prof - a.prof;
});
var vistos = {}, saida = [];
for(var k=0;k<cands.length;k++){
  if(vistos[cands[k].seq]) continue;
  vistos[cands[k].seq] = 1;
  saida.push(cands[k]);
  if(saida.length >= 6) break;
}
return saida;
"""


def _melhor_candidato(driver):
    """Roda a busca no documento atual e devolve o melhor candidato (ou None)."""
    try:
        cands = driver.execute_script(JS_PROCURAR, markers())
    except Exception:
        return None
    if cands and cands[0]["match"] >= 6:
        return cands[0]
    return None


def auto_detectar(driver):
    """Procura o histórico sozinho: primeiro na página, depois em cada iframe.
    Guarda o que achou pra reusar. Devolve True se encontrou."""
    global _IFRAME_ATIVO, _SELETOR_ATIVO

    # Se você preencheu o config na mão, respeita o que está lá.
    if cfg.SELETOR_HISTORICO:
        _IFRAME_ATIVO = cfg.SELETOR_IFRAME or None
        _SELETOR_ATIVO = cfg.SELETOR_HISTORICO
        return True

    # 1) Direto na página principal.
    driver.switch_to.default_content()
    c = _melhor_candidato(driver)
    if c:
        _IFRAME_ATIVO, _SELETOR_ATIVO = None, c["sel"]
        print("Auto-detectei o histórico na página ({} resultados).".format(c["match"]))
        return True

    # 2) Dentro de cada iframe (o jogo quase sempre está num).
    driver.switch_to.default_content()
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for idx, frame in enumerate(iframes):
        fid = frame.get_attribute("id")
        sel_frame = "#" + fid if fid else "iframe:nth-of-type({})".format(idx + 1)
        driver.switch_to.default_content()
        try:
            driver.switch_to.frame(frame)
        except Exception:
            continue
        c = _melhor_candidato(driver)
        if c:
            _IFRAME_ATIVO, _SELETOR_ATIVO = sel_frame, c["sel"]
            driver.switch_to.default_content()
            print("Auto-detectei o histórico no iframe {} ({} resultados).".format(
                sel_frame, c["match"]))
            return True
    driver.switch_to.default_content()
    return False


def _iframe_alvo():
    return cfg.SELETOR_IFRAME or _IFRAME_ATIVO or ""


def _seletor_alvo():
    return cfg.SELETOR_HISTORICO or _SELETOR_ATIVO or ""


def entrar_no_iframe(driver):
    """Se o jogo estiver num iframe, entra nele. Chame sempre antes de ler."""
    driver.switch_to.default_content()
    alvo = _iframe_alvo()
    if alvo:
        try:
            frame = driver.find_element(By.CSS_SELECTOR, alvo)
            driver.switch_to.frame(frame)
        except Exception:
            pass


def ler_historico(driver):
    """Lê a tirinha de resultados e devolve uma lista tipo
    ['B','P','P','T','B', ...] NA ORDEM EM QUE APARECEM NA TELA.

    (Qual lado é o resultado mais novo, o bot descobre SOZINHO no loop
    principal, comparando uma leitura com a outra.)
    """
    entrar_no_iframe(driver)
    seletor = _seletor_alvo()
    if not seletor:
        return []
    try:
        caixa = driver.find_element(By.CSS_SELECTOR, seletor)
    except Exception:
        return []

    itens = caixa.find_elements(By.XPATH, "./*")
    seq = []
    for it in itens:
        cor = _classificar(_texto_do_elemento(it))
        if cor is None:
            # Talvez a bolinha esteja um nível mais fundo — tenta os filhos.
            for filho in it.find_elements(By.XPATH, ".//*"):
                cor = _classificar(_texto_do_elemento(filho))
                if cor:
                    break
        if cor:
            seq.append(cor)

    return seq


# Alguns sites mostram o resultado mais RECENTE na esquerda. O bot
# DESCOBRE isso sozinho comparando leituras; este valor é só o chute
# inicial (False = mais novo na direita, o mais comum).
MAIS_NOVO_PRIMEIRO = False


def _detectar_ordem(antes, agora):
    """Compara duas leituras seguidas e descobre POR QUAL LADO entram os
    resultados novos. Devolve 'fim' (direita), 'inicio' (esquerda) ou
    None quando não dá pra saber ainda."""
    if not antes or not agora or antes == agora:
        return None
    if min(len(antes), len(agora)) < 6:
        return None
    fim = inicio = False
    for k in range(1, 4):
        if len(agora) > k:
            resto = agora[:-k]
            if resto == antes[-len(resto):]:
                fim = True          # o que sobrou casa com o FINAL de antes
            resto = agora[k:]
            if resto == antes[:len(resto)]:
                inicio = True       # o que sobrou casa com o COMEÇO de antes
    if fim and not inicio:
        return "fim"
    if inicio and not fim:
        return "inicio"
    return None


# ---------- As estratégias (o palpite) ----------

def _so_cores(seq):
    """Tira os empates, deixando só B e P (pra contar sequência)."""
    if cfg.IGNORAR_EMPATE:
        return [x for x in seq if x != "T"]
    return list(seq)


def _oposto(cor):
    return "P" if cor == "B" else "B"


def _streak_fim(s):
    """Quantas vezes a ÚLTIMA cor se repetiu seguida no final."""
    if not s:
        return 0
    n = 0
    for x in reversed(s):
        if x == s[-1]:
            n += 1
        else:
            break
    return n


def _zigzag_fim(s):
    """Tamanho do zig-zag (cores alternando) no final."""
    if len(s) < 2:
        return len(s)
    n = 1
    for i in range(len(s) - 1, 0, -1):
        if s[i] != s[i - 1]:
            n += 1
        else:
            break
    return n


def estrategia_confluencia(seq):
    """A análise mais completa: combina TRÊS leituras da mesa.
      1) Sequência (uma cor emendando) ou zig-zag (alternância) = o gatilho.
      2) Domínio da janela (quem está vencendo mais) = +1 estrela.
      3) Padrão já longo = +1 estrela.
    Quanto mais análises concordam, mais estrelas o palpite ganha."""
    s = _so_cores(seq)
    if len(s) < 3:
        return None

    n = _streak_fim(s)
    z = _zigzag_fim(s)
    motivos = []
    alvo = None

    # Gatilho principal: sequência OU alternância.
    if n >= cfg.STREAK_MINIMO:
        if cfg.MODO_TENDENCIA == "contra":
            alvo = _oposto(s[-1])
            motivos.append("Saíram {}x seguidas — apostando na quebra.".format(n))
        else:
            alvo = s[-1]
            motivos.append("Saíram {}x seguidas — surfando a sequência.".format(n))
    elif z >= 4:
        alvo = _oposto(s[-1])
        motivos.append("Zig-zag de {} — continuando a alternância.".format(z))

    if alvo is None:
        return None

    forca = 1

    # Confirmação 1: o alvo está DOMINANDO a janela recente?
    jan = s[-cfg.JANELA:]
    do_alvo = jan.count(alvo)
    do_outro = len(jan) - do_alvo
    if do_alvo > do_outro:
        forca += 1
        motivos.append("{} dominando a janela ({} x {}).".format(
            "Banca" if alvo == "B" else "Player", do_alvo, do_outro))

    # Confirmação 2: o padrão já está longo?
    if n >= cfg.STREAK_MINIMO + 2 or z >= 6:
        forca += 1
        motivos.append("Padrão já longo — leitura mais firme.")

    return {"sinal": alvo, "forca": min(3, forca), "motivos": motivos}


def estrategia_tendencia(seq):
    s = _so_cores(seq)
    if len(s) < cfg.STREAK_MINIMO:
        return None
    ultima = s[-1]
    # Conta quantas iguais seguidas no fim.
    n = 0
    for x in reversed(s):
        if x == ultima:
            n += 1
        else:
            break
    if n < cfg.STREAK_MINIMO:
        return None
    if cfg.MODO_TENDENCIA == "seguir":
        alvo = ultima
        motivo = "Saíram {}x seguidas — surfando a sequência.".format(n)
    else:
        alvo = _oposto(ultima)
        motivo = "Saíram {}x seguidas — apostando na quebra.".format(n)
    forca = min(3, 1 + (n - cfg.STREAK_MINIMO) // 1 + (1 if n >= cfg.STREAK_MINIMO + 2 else 0))
    forca = max(1, min(3, forca))
    return {"sinal": alvo, "forca": forca, "motivos": [motivo]}


def estrategia_frequencia(seq):
    s = _so_cores(seq)[-cfg.JANELA:]
    if len(s) < max(6, cfg.STREAK_MINIMO):
        return None
    nb = s.count("B")
    np_ = s.count("P")
    if nb == np_:
        return None
    # Aposta na que apareceu MENOS (ideia de "volta à média").
    alvo = "B" if nb < np_ else "P"
    dif = abs(nb - np_)
    forca = 1 + (1 if dif >= 3 else 0) + (1 if dif >= 5 else 0)
    motivo = "Na janela de {}: Banca {} x {} Player. Menos frequente: {}.".format(
        len(s), nb, np_, "Banca" if alvo == "B" else "Player")
    return {"sinal": alvo, "forca": max(1, min(3, forca)), "motivos": [motivo]}


def estrategia_alternancia(seq):
    s = _so_cores(seq)
    if len(s) < 4:
        return None
    # Quantas vezes seguidas veio zig-zag no fim (A B A B ...).
    n = 1
    for i in range(len(s) - 1, 0, -1):
        if s[i] != s[i - 1]:
            n += 1
        else:
            break
    if n < 4:
        return None
    alvo = _oposto(s[-1])  # continua o zig-zag
    forca = 1 + (1 if n >= 5 else 0) + (1 if n >= 7 else 0)
    motivo = "Zig-zag de {} seguidos — sugerindo continuar a alternância.".format(n)
    return {"sinal": alvo, "forca": max(1, min(3, forca)), "motivos": [motivo]}


def palpite_de_plantao(seq):
    """Pro MODO RITMO (sinal a cada X segundos): se não há padrão forte,
    dá o melhor palpite básico — a cor que está dominando a janela."""
    r = analisar(seq)
    if r:
        return r
    s = _so_cores(seq)
    if not s:
        return None
    jan = s[-cfg.JANELA:]
    nb, np_ = jan.count("B"), jan.count("P")
    if nb == np_:
        alvo = s[-1]
        motivo = "Mesa equilibrada ({} x {}) — seguindo a última cor.".format(nb, np_)
    else:
        alvo = "B" if nb > np_ else "P"
        motivo = "Sem padrão forte — indo com quem domina a janela ({} x {}).".format(
            max(nb, np_), min(nb, np_))
    return {"sinal": alvo, "forca": 1, "motivos": [motivo]}


def analisar(seq):
    """Escolhe a estratégia do config e devolve o palpite (ou None)."""
    est = cfg.ESTRATEGIA
    if est == "so_coletar":
        return None
    if est == "confluencia":
        r = estrategia_confluencia(seq)
    elif est == "tendencia":
        r = estrategia_tendencia(seq)
    elif est == "frequencia":
        r = estrategia_frequencia(seq)
    elif est == "alternancia":
        r = estrategia_alternancia(seq)
    else:
        print("Estratégia desconhecida no config:", est, "-> usando so_coletar")
        return None
    if r and r["forca"] < cfg.FORCA_MINIMA:
        return None
    return r


# ---------- Montar a mensagem ----------

NOME = {"B": "🔴 BANCA (Banker)", "P": "🔵 PLAYER", "T": "🟡 EMPATE"}
BOLA = {"B": "🔴", "P": "🔵", "T": "🟡"}


def fita(seq, quantos=18):
    return "".join(BOLA.get(x, "⚪") for x in seq[-quantos:])


def montar_mensagem(palpite, seq, placar):
    estrelas = "⭐" * palpite["forca"]
    linhas = [
        "🎲 BAC BO — PALPITE DA PRÓXIMA RODADA",
        "",
        "Aposte em: {}".format(NOME[palpite["sinal"]]),
        "Força: {} ({} de 3)".format(estrelas, palpite["forca"]),
        "",
        "Por quê:",
    ]
    for m in palpite["motivos"]:
        linhas.append("• " + m)

    if cfg.USAR_GALE:
        linhas += ["", montar_gale(placar)]

    ult = seq[-cfg.JANELA:]
    linhas += [
        "",
        "Últimos resultados:",
        fita(seq),
        "Na janela: 🔴 {} · 🔵 {} · 🟡 {}".format(
            ult.count("B"), ult.count("P"), ult.count("T")),
        "",
        "Placar do bot: ✅ {} · ❌ {} · 🟡 {}  (aproveit. {})".format(
            placar["acertos"], placar["erros"], placar["empates"],
            _aproveitamento(placar)),
        "",
        "⚠️ Dado é sorte. Isto é estudo, não garantia. Aposte com juízo.",
    ]
    return "\n".join(linhas)


def montar_gale(placar):
    valor = cfg.APOSTA_BASE * (2 ** placar["gale_atual"])
    if placar["gale_atual"] == 0:
        return "💰 Valor sugerido: {} (entrada base)".format(valor)
    return "💰 Valor sugerido: {} (gale {} de {})".format(
        valor, placar["gale_atual"], cfg.NIVEIS_GALE)


def _aproveitamento(placar):
    total = placar["acertos"] + placar["erros"]
    if total == 0:
        return "—"
    return "{}%".format(round(100 * placar["acertos"] / total))


# ---------- O loop principal ----------

def main():
    print("Ligando o BOT BAC BO...")
    driver = iniciar_navegador()
    esperar_voce_abrir_o_jogo(driver)

    # Ele procura o histórico na tela SOZINHO (você não precisa colar nada).
    print("Procurando o histórico do Bac Bo na tela...")
    achou = False
    for tentativa in range(5):
        achou = auto_detectar(driver)
        if achou:
            teste = ler_historico(driver)
            # "Só empate" = elemento errado; não vale como sucesso.
            if teste and not all(x == "T" for x in teste):
                break
        if tentativa < 4:
            print("  ...ainda não achei. Tento de novo em 3s "
                  "(deixe o jogo aberto com o histórico na tela).")
            time.sleep(3)

    teste = ler_historico(driver) if achou else []
    if not teste:
        aviso = ("⚠️ Liguei, mas ainda NÃO achei o histórico do Bac Bo na "
                 "tela. Confira se o jogo está aberto com as bolinhas de "
                 "resultado aparecendo. Vou seguir tentando sozinho; se não "
                 "pegar, rode o  calibrar_bacbo.py  que a gente ajusta juntos.")
        avisar(aviso)
    else:
        print("Consegui ler! Últimos resultados:", fita(teste))

    if not telegram_configurado():
        print("\nℹ️  Telegram ainda não configurado — e tudo bem!")
        print("   Os palpites vão aparecer AQUI nesta janela do cmd.")
        print("   (Pra receber no celular também, cole o token e o chat id")
        print("    no arquivo config_bacbo.py. Aí ele manda nos dois.)\n")

    avisar(
        "✅ Bot BAC BO ligado!\n"
        "Estratégia: {}\n"
        "Vou te avisar o palpite da próxima rodada quando fizer sentido.\n\n"
        "⚠️ Dado é sorte. Sinal não é garantia.".format(cfg.ESTRATEGIA))

    placar = {"acertos": 0, "erros": 0, "empates": 0, "gale_atual": 0}
    assinatura_anterior = None   # "foto" do histórico pra saber quando muda
    palpite_pendente = None      # o que sugerimos pra rodada que está rolando
    vazios = 0                   # leituras seguidas sem achar nada
    ultima_mensagem = time.time()  # pra mandar o "sinal de vida" de vez em quando
    bruto_anterior = None        # leitura crua anterior (pra descobrir a ordem)
    ordem = "inicio" if MAIS_NOVO_PRIMEIRO else "fim"
    ultimo_sinal = 0.0           # hora do último palpite (pro MODO RITMO)
    avisei_desequilibrio = False  # já avisei que a leitura veio de uma cor só?

    while True:
        try:
            bruto = ler_historico(driver)
            # Leitura "só empate" é impossível num jogo real: é sinal de que
            # pegamos o elemento errado. Descarta e procura de novo.
            suspeita = len(bruto) >= 8 and all(x == "T" for x in bruto)
            if not bruto or suspeita:
                vazios += 1
                if suspeita and vazios == 1:
                    print("Hmm, li 'só empates' — isso não existe. "
                          "Vou procurar a tirinha certa de novo.")
                # Se parou de ler (a página pode ter recarregado), procura de novo.
                if vazios % 5 == 0 or suspeita:
                    print("Procurando o histórico de novo...")
                    global _SELETOR_ATIVO, _IFRAME_ATIVO
                    _SELETOR_ATIVO = None
                    _IFRAME_ATIVO = None
                    auto_detectar(driver)
                time.sleep(cfg.INTERVALO_SEGUNDOS)
                continue
            vazios = 0

            # Descobre POR QUAL LADO entra o resultado novo (compara com a
            # leitura anterior). Se perceber que estava de cabeça pra baixo,
            # vira e recomeça o placar da rodada pra não conferir errado.
            lado = _detectar_ordem(bruto_anterior, bruto)
            if lado and lado != ordem:
                ordem = lado
                print("Percebi a ordem do histórico: o resultado novo entra",
                      "na ESQUERDA." if ordem == "inicio" else "na DIREITA.")
                assinatura_anterior = None
                palpite_pendente = None
            bruto_anterior = list(bruto)

            # A partir daqui, 'seq' está SEMPRE do mais antigo -> mais novo.
            seq = bruto[::-1] if ordem == "inicio" else bruto

            # Auto-vigilância: um histórico real SEMPRE mistura as duas
            # cores. Se eu estiver lendo uma cor só, algo está errado —
            # aviso pra gente conferir juntos.
            so_bp = [x for x in seq if x != "T"]
            if (len(so_bp) >= 10 and not avisei_desequilibrio
                    and (so_bp.count("B") == 0 or so_bp.count("P") == 0)):
                avisei_desequilibrio = True
                cor_unica = "PLAYER 🔵" if so_bp.count("B") == 0 else "BANCA 🔴"
                avisar("⚠️ Atenção: estou lendo o histórico com UMA cor só "
                       "({}). Isso normalmente é leitura errada da tela.\n\n"
                       "Compara as bolinhas que eu mando com a mesa real. "
                       "Se NÃO baterem, roda o CALIBRAR_BACBO e me manda o "
                       "resultado pra eu ajustar.".format(cor_unica))

            assinatura = "".join(seq[-25:])

            # Rodada nova = a "foto" mudou desde a última leitura.
            if assinatura != assinatura_anterior:
                # Se tínhamos um palpite pendente, o resultado que acabou
                # de sair é o veredito dele: acertou ou errou?
                if palpite_pendente is not None and assinatura_anterior is not None:
                    resultado = seq[-1]
                    _conferir_placar(palpite_pendente, resultado, placar)
                    print("Saiu:", NOME[resultado],
                          "| placar", placar["acertos"], "x", placar["erros"])

                assinatura_anterior = assinatura

                # Agora calcula o palpite pra PRÓXIMA rodada.
                palpite = analisar(seq)
                if palpite:
                    avisar(montar_mensagem(palpite, seq, placar))
                    ultima_mensagem = time.time()
                    ultimo_sinal = time.time()
                    palpite_pendente = palpite["sinal"]
                    print(">>> PALPITE:", NOME[palpite["sinal"]],
                          "força", palpite["forca"])
                else:
                    palpite_pendente = None
                    if cfg.ESTRATEGIA == "so_coletar":
                        print("Coletando... últimos:", fita(seq))
                    else:
                        s = _so_cores(seq)
                        print("Sem palpite agora. Últimos:", fita(seq),
                              "| seguidas:", _streak_fim(s),
                              "| zig-zag:", _zigzag_fim(s))

            # MODO RITMO: garante um palpite a cada X segundos, mesmo sem
            # padrão forte (você escolhe o ritmo no config).
            cada = getattr(cfg, "SINAL_A_CADA_SEGUNDOS", 0)
            if cada > 0 and time.time() - ultimo_sinal >= cada:
                p = palpite_de_plantao(seq)
                if p:
                    avisar(montar_mensagem(p, seq, placar))
                    ultima_mensagem = time.time()
                    ultimo_sinal = time.time()
                    palpite_pendente = p["sinal"]
                    print(">>> PALPITE (ritmo):", NOME[p["sinal"]],
                          "força", p["forca"])

            # "Sinal de vida": se faz tempo que não mando nada no Telegram,
            # aviso que continuo ligado (pra você saber que não travei).
            minutos = getattr(cfg, "AVISO_VIVO_MINUTOS", 15)
            if minutos > 0 and time.time() - ultima_mensagem > minutos * 60:
                avisar("🤖 Continuo ligado e lendo a mesa!\n"
                       "Só não apareceu o padrão da estratégia ainda.\n\n"
                       "Últimos resultados:\n" + fita(seq) +
                       "\n\nPlacar até agora: ✅ {} · ❌ {} · 🟡 {}".format(
                           placar["acertos"], placar["erros"],
                           placar["empates"]))
                ultima_mensagem = time.time()

        except Exception as erro:
            print("Deu um errinho (vou continuar):", erro)

        time.sleep(cfg.INTERVALO_SEGUNDOS)


def _conferir_placar(palpite, resultado, placar):
    """Atualiza acertos/erros e o nível do gale."""
    if resultado == "T" and palpite != "T":
        # Empate: na maioria das mesas devolve a aposta (não conta).
        placar["empates"] += 1
        return
    if resultado == palpite:
        placar["acertos"] += 1
        placar["gale_atual"] = 0            # ganhou -> volta pra aposta base
    else:
        placar["erros"] += 1
        if cfg.USAR_GALE and placar["gale_atual"] < cfg.NIVEIS_GALE:
            placar["gale_atual"] += 1       # perdeu -> sobe um gale
        else:
            placar["gale_atual"] = 0


if __name__ == "__main__":
    main()
