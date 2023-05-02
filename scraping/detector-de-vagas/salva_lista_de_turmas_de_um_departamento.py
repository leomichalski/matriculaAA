import os
import time
import shutil
import argparse

from utils.scraping import *
from utils.sigaa import (
    listar_disciplinas,
    salvar_lista_de_turmas_e_fechar_sigaa,
)


def take_screenshot(pasta_destino_screenshots, run_number):
    img = pyautogui.screenshot(
        os.path.join(
            pasta_destino_screenshots,
            "run_%02d.png" % (run_number,)
        )
    )


def parse_args():
    ap = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    ap.add_argument(
        "--url-inicial",
        type=str, default='https://sigaa.unb.br/sigaa/public/turmas/listar.jsf',
        help="URL da pagina do SIGAA que lista as disciplinas e suas turmas."
    )
    ap.add_argument(
        "--index-do-departamento-na-lista",
        type=int, default=78,  # eh a FGA
        help="Na URL inicial, existe uma lista de departamentos. A FGA esta na posicao 78 dessa lista."
    )

    ap.add_argument(
        "--measure-time",
        action='store_true', default=False,
        help="Measure the elapsed time for the whole script."
    )
    ap.add_argument(
        "--take-screenshots",
        action='store_true', default=False,
        help="Take a screenshot for each main step of the script."
    )

    ap.add_argument(
        "--pasta-destino-screenshots",
        type=str, default="screenshots01",
        help="Pasta onde as screenshots serão salvas."
    )
    ap.add_argument(
        "--pasta-imagens-pyautogui",
        type=str, default="elementos_das_telas",
        help="Pasta onde estão as imagens usadas para localizar elementos na tela."
    )
    ap.add_argument(
        "--pasta-arquivos-html",
        type=str, default="arquivos_html",
        help="Pasta de arquivos HTML que foram baixados por este script."
    )
    ap.add_argument(
        "--pasta-padrao-de-downloads-do-so",
        type=str, default='/root/Downloads/',
        help="Pasta padrao do sistema operacional para salvar paginas baixadas da web."
    )
    ap.add_argument(
        "--run-number",
        type=int, default=0,
        help="Run number. Used only for screenshot versioning. Optional."
    )

    args = ap.parse_args()
    return args


def main(url_inicial,
         index_do_departamento_na_lista,
         measure_time,
         take_screenshots,
         pasta_destino_screenshots,
         pasta_imagens_pyautogui,
         pasta_arquivos_html,
         run_number,
         pasta_padrao_de_downloads_do_so):
    if measure_time:
        start_time = time.time()

    pyautogui, nodes_to_stop = start_screen()
    if take_screenshots:
        take_screenshot(
            pasta_destino_screenshots=pasta_destino_screenshots,
            run_number=run_number
        )

    organizar_janelas(
        pyautogui=pyautogui,
        pasta_imagens_pyautogui=pasta_imagens_pyautogui,
    )
    if take_screenshots:
        take_screenshot(
            pasta_destino_screenshots=pasta_destino_screenshots,
            run_number=run_number
        )

    abrir_url(
        pyautogui=pyautogui,
        url=url_inicial,
    )
    if take_screenshots:
        take_screenshot(
            pasta_destino_screenshots=pasta_destino_screenshots,
            run_number=run_number
        )

    listar_disciplinas(
        pyautogui=pyautogui,
        pasta_imagens_pyautogui=pasta_imagens_pyautogui,
        index_do_departamento_na_lista=index_do_departamento_na_lista,
    )
    if take_screenshots:
        take_screenshot(
            pasta_destino_screenshots=pasta_destino_screenshots,
            run_number=run_number
        )

    salvar_lista_de_turmas_e_fechar_sigaa(
        pyautogui=pyautogui,
        pasta_imagens_pyautogui=pasta_imagens_pyautogui,
        pasta_arquivos_html=pasta_arquivos_html,
        index_do_departamento_na_lista=index_do_departamento_na_lista,
        pasta_padrao_de_downloads_do_so=pasta_padrao_de_downloads_do_so
    )
    if take_screenshots:
        take_screenshot(
            pasta_destino_screenshots=pasta_destino_screenshots,
            run_number=run_number
        )

    if measure_time:
        print("elapsed time:", time.time() - start_time)

    stop_screen(nodes_to_stop)


if __name__ == '__main__':
    args = parse_args()
    main(**vars(args))
