# ============================================================
#   CALIBRAR o BOT BAC BO  -  acha os resultados na tela pra você
#
#   PROBLEMA: cada site coloca as bolinhas de resultado num lugar
#   diferente do HTML. Este ajudante ABRE o Chrome, você deixa o
#   Bac Bo na tela, e ele VARRE a página procurando a tirinha de
#   resultados. No fim, ele te mostra as linhas exatas pra colar no
#   config_bacbo.py (SELETOR_IFRAME e SELETOR_HISTORICO).
#
#   Como usar:
#     1. Rode este arquivo (ou o LIGAR_..._CALIBRAR).
#     2. Faça login e abra o Bac Bo, com o histórico aparecendo.
#     3. Volte no cmd e aperte ENTER.
#     4. Copie as linhas que ele sugerir pro config_bacbo.py.
# ============================================================

import time
import config_bacbo as cfg
from bot_bacbo import iniciar_navegador

from selenium.webdriver.common.by import By


BOLA = {"B": "🔴", "P": "🔵", "T": "🟡"}


# JavaScript que roda DENTRO da página e procura a tirinha de resultados.
# Ele devolve os melhores "candidatos": elementos cujos filhos parecem ser
# bolinhas de Banca/Player/Empate.
JS_PROCURAR = r"""
var MARK = arguments[0];  // {banca:[...], player:[...], empate:[...]}

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

function classifica(s){
  for(var i=0;i<MARK.empate.length;i++)
    if(MARK.empate[i] && s.indexOf(MARK.empate[i])>=0) return "T";
  for(var i=0;i<MARK.banca.length;i++)
    if(MARK.banca[i] && s.indexOf(MARK.banca[i])>=0) return "B";
  for(var i=0;i<MARK.player.length;i++)
    if(MARK.player[i] && s.indexOf(MARK.player[i])>=0) return "P";
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

function profundidade(el){
  var d=0; while(el){ d++; el=el.parentNode; } return d;
}

var todos = document.querySelectorAll("*");
var cands = [];
for(var i=0;i<todos.length;i++){
  var el = todos[i];
  var kids = el.children;
  if(!kids || kids.length < 6) continue;
  var seq = [], match = 0;
  for(var j=0;j<kids.length;j++){
    var c = classificaFundo(kids[j]);
    if(c){ match++; seq.push(c); }
  }
  if(match >= 6){
    cands.push({sel: seletorDe(el), total: kids.length,
                match: match, prof: profundidade(el),
                seq: seq.join("")});
  }
}
// Melhor = mais bolinhas reconhecidas; empate: o mais "fundo" (específico).
cands.sort(function(a,b){
  if(b.match !== a.match) return b.match - a.match;
  return b.prof - a.prof;
});
// Tira repetidos com a mesma sequência.
var vistos = {}, saida = [];
for(var k=0;k<cands.length;k++){
  if(vistos[cands[k].seq]) continue;
  vistos[cands[k].seq] = 1;
  saida.push(cands[k]);
  if(saida.length >= 6) break;
}
return saida;
"""


def markers():
    return {
        "banca": [m.lower() for m in cfg.MARCADORES_BANCA],
        "player": [m.lower() for m in cfg.MARCADORES_PLAYER],
        "empate": [m.lower() for m in cfg.MARCADORES_EMPATE],
    }


def preview(seq_str):
    return "".join(BOLA.get(x, "?") for x in seq_str)


def varrer(driver, nome_frame, seletor_iframe):
    """Roda a busca no documento atual e imprime os candidatos."""
    try:
        cands = driver.execute_script(JS_PROCURAR, markers())
    except Exception as erro:
        print("   (não deu pra varrer aqui:", erro, ")")
        return

    if not cands:
        print("   nada reconhecido aqui.")
        return

    print("   ACHEI {} candidato(s) em {}:".format(len(cands), nome_frame))
    for i, c in enumerate(cands, 1):
        print("   " + "-" * 54)
        print("   #{}  reconheci {} de {} bolinhas".format(
            i, c["match"], c["total"]))
        print("   sequência lida: " + preview(c["seq"]))
        print("   >>> COLE NO config_bacbo.py:")
        if seletor_iframe:
            print('       SELETOR_IFRAME   = "{}"'.format(seletor_iframe))
        else:
            print('       SELETOR_IFRAME   = ""')
        print('       SELETOR_HISTORICO = "{}"'.format(c["sel"]))


def main():
    print("Abrindo o Chrome pra calibrar...")
    driver = iniciar_navegador()
    driver.get(cfg.URL_JOGO)

    print("=" * 60)
    print(" 1) Faça login e deixe o BAC BO na tela (com o histórico).")
    print(" 2) Volte aqui e aperte ENTER pra eu procurar os resultados.")
    print("=" * 60)
    try:
        input(">>> Pronto? Aperte ENTER... ")
    except EOFError:
        time.sleep(20)

    print("\nProcurando a tirinha de resultados...\n")

    # 1) Procura direto na página.
    driver.switch_to.default_content()
    print("[ Página principal ]")
    varrer(driver, "página principal", "")

    # 2) Procura dentro de cada iframe (o jogo quase sempre está num).
    driver.switch_to.default_content()
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print("\nEncontrei {} iframe(s) na página.".format(len(iframes)))
    for idx, frame in enumerate(iframes):
        # Monta um seletor simples pro iframe pra você colar no config.
        fid = frame.get_attribute("id")
        if fid:
            sel_frame = "#" + fid
        else:
            sel_frame = "iframe:nth-of-type({})".format(idx + 1)
        driver.switch_to.default_content()
        try:
            driver.switch_to.frame(frame)
        except Exception:
            continue
        print("\n[ iframe {} -> {} ]".format(idx + 1, sel_frame))
        varrer(driver, "iframe " + sel_frame, sel_frame)

    driver.switch_to.default_content()
    print("\n" + "=" * 60)
    print("Pronto! Escolha o candidato cuja 'sequência lida' bate com as")
    print("bolinhas REAIS da tela e cole as 2 linhas dele no config_bacbo.py.")
    print("Depois é só ligar o bot normal (LIGAR_BOT_BACBO...).")
    print("Se NADA bateu, me chame que a gente ajusta os marcadores juntos.")
    print("=" * 60)
    try:
        input("Aperte ENTER pra fechar o navegador... ")
    except EOFError:
        time.sleep(3)
    driver.quit()


if __name__ == "__main__":
    main()
