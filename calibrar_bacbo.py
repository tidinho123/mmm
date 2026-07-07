# ============================================================
#   CALIBRAR o BOT BAC BO  -  só pra CONFERIR / casos difíceis
#
#   VOCÊ NORMALMENTE NÃO PRECISA DISTO. O bot já procura os
#   resultados na tela SOZINHO quando você liga ele.
#
#   Use este ajudante só se:
#     - o bot avisar que não achou o histórico, ou
#     - você quiser CONFERIR o que ele está lendo, ou
#     - as cores vierem trocadas e a gente precisar ajustar.
#
#   Ele abre o Chrome, você deixa o Bac Bo na tela, aperta ENTER,
#   e ele mostra os candidatos com a "sequência lida" (🔴🔵🟡...) e
#   as 2 linhas que você PODE (se quiser) fixar no config_bacbo.py.
# ============================================================

import time
import config_bacbo as cfg
from bot_bacbo import iniciar_navegador, JS_PROCURAR, markers

from selenium.webdriver.common.by import By


BOLA = {"B": "🔴", "P": "🔵", "T": "🟡"}


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
        print("   >>> (opcional) pra FIXAR no config_bacbo.py:")
        if seletor_iframe:
            print('       SELETOR_IFRAME    = "{}"'.format(seletor_iframe))
        else:
            print('       SELETOR_IFRAME    = ""')
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
    print("Se a 'sequência lida' de algum candidato bate com as bolinhas")
    print("REAIS da tela, ótimo: o bot vai achar isso sozinho ao ligar.")
    print("Se quiser travar nesse elemento, cole as 2 linhas dele no config.")
    print("Se as cores vierem TROCADAS, me mande este resultado que eu")
    print("ajusto os MARCADORES_... contigo.")
    print("=" * 60)
    try:
        input("Aperte ENTER pra fechar o navegador... ")
    except EOFError:
        time.sleep(3)
    driver.quit()


if __name__ == "__main__":
    main()
