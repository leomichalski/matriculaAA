# USAGE:
"""
docker run --rm -it -v ${PWD}:/curr -w /curr leommiranda/pyautogui \
  python3 realiza_matricula.py --measure-time --take-screenshots \
  --matricula="190012345" --senha="XXXXXXXX" --cpf="XXXYYYZZZKK" \
  --data-de-nascimento="DDMMAAAA" \
  --codigo-disciplina="FGA0030" --nome-docente="BRUNO CESAR RIBAS" \
  --horario-codificado="35T6 35N1" \
  --pasta-destino-screenshots="screenshots" \
  --pasta-imagens-pyautogui="images_to_locate"
"""

# nao repara na bagunça :3
import time
import argparse
import os

from bot_utils import (
    organizar_janelas,
    abrir_url,
    start_screen,
    stop_screen,
)
from sigaa_utils import (
    login_no_sigaa,
    ir_pra_matricula_extraordinaria,
    buscar_disciplina_matricula_extraordinaria,
    confirmar_dados_matricula_extraordinaria,
)


def parse_args():
    ap = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # informacoes sobre o site SIGAA
    ap.add_argument(
        "--url-do-login",
        type=str, default="https://sigaa.unb.br/sigaa/verTelaLogin.do",
        help="Numero da matricula do/da discente."
    )
    # informacoes sobre a/o discente
    ap.add_argument(
        "--matricula",
        type=str, required=True,
        help="Numero da matricula do/da discente."
    )
    ap.add_argument(
        "--senha",
        type=str, required=True,
        help="Senha da conta do SIGAA do/da discente."
    )
    ap.add_argument(
        "--cpf",
        type=str, required=True,
        help="CPF do/da discente."
    )
    ap.add_argument(
        "--data-de-nascimento",
        type=str, required=True,
        help="Data de nascimento do/da discente."
    )
    # informacoes sobre a/o disciplina desejada
    ap.add_argument(
        "--codigo-disciplina",
        type=str, required=True,
        help="Codigo da disciplina desejada. Por exemplo, \"FGA0030\""
    )
    ap.add_argument(
        "--nome-docente",
        type=str, required=True,
        help="Nome do docente que ministra a disciplina desejada. Por exemplo, \"BRUNO CESAR RIBAS\""
    )
    ap.add_argument(
        "--horario-codificado",
        type=str, required=True,
        help="Horario codificado da disciplina desejada. Por exemplo, \"35T6 35N1\""
    )
    # funcionalidades adicionais
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
    # informacoes relacionadas a imagens e a screenshots
    ap.add_argument(
        "--pasta-imagens-pyautogui",
        type=str, default="images_to_locate",
        help="Pasta onde estão as imagens usadas para localizar elementos na tela."
    )
    ap.add_argument(
        "--pasta-destino-screenshots",
        type=str, default="screenshots",
        help="Pasta onde as screenshots serão salvas."
    )
    ap.add_argument(
        "--run-number",
        type=int, default=0,
        help="Run number. Used only for screenshot versioning. Optional."
    )
    # outros argumentos
    ap.add_argument(
        "-t", "--time-out",
        type=int, default=5,
        help="Time out in seconds. Used to wait for elements to load."
    )
    args = ap.parse_args()
    # preprocessamento dos argumentos
    args.horario_codificado = args.horario_codificado.split()[0]
    return args


def take_screenshot(pasta_destino_screenshots, run_number):
    img = pyautogui.screenshot(
        os.path.join(
            pasta_destino_screenshots,
            "run_%02d.png" % (run_number,)
        )
    )


args = parse_args()

if args.measure_time:
    start_time = time.time()

# esta funcao tambem retorna o pyautogui com o objetivo de
# ser compatível com pyvirtualdisplay (Xvfb) e com Docker
pyautogui, nodes_to_stop = start_screen()

if args.take_screenshots:
    take_screenshot(
        pasta_destino_screenshots=args.pasta_destino_screenshots,
        run_number=args.run_number
    )

organizar_janelas(
    pyautogui=pyautogui,
    pasta_imagens_pyautogui=args.pasta_imagens_pyautogui,
)

if args.take_screenshots:
    take_screenshot(
        pasta_destino_screenshots=args.pasta_destino_screenshots,
        run_number=args.run_number
    )

abrir_url(
    pyautogui=pyautogui,
    url=args.url_do_login,
)

if args.take_screenshots:
    take_screenshot(
        pasta_destino_screenshots=args.pasta_destino_screenshots,
        run_number=args.run_number
    )

login_no_sigaa(
    pyautogui=pyautogui,
    matricula=args.matricula,
    senha=args.senha,
    pasta_imagens_pyautogui=args.pasta_imagens_pyautogui,
)

if args.take_screenshots:
    take_screenshot(
        pasta_destino_screenshots=args.pasta_destino_screenshots,
        run_number=args.run_number
    )

ir_pra_matricula_extraordinaria(
    pyautogui=pyautogui,
    pasta_imagens_pyautogui=args.pasta_imagens_pyautogui,
)

if args.take_screenshots:
    take_screenshot(
        pasta_destino_screenshots=args.pasta_destino_screenshots,
        run_number=args.run_number
    )

buscar_disciplina_matricula_extraordinaria(
    pyautogui=pyautogui,
    codigo_disciplina=args.codigo_disciplina,
    nome_docente=args.nome_docente,
    horario_codificado=args.horario_codificado,
    pasta_imagens_pyautogui=args.pasta_imagens_pyautogui,
)

if args.take_screenshots:
    take_screenshot(
        pasta_destino_screenshots=args.pasta_destino_screenshots,
        run_number=args.run_number
    )

confirmar_dados_matricula_extraordinaria(
    pyautogui=pyautogui,
    cpf=args.cpf,
    data_de_nascimento=args.data_de_nascimento,
    matricula=args.matricula,
    senha=args.senha,
    pasta_imagens_pyautogui=args.pasta_imagens_pyautogui,
)

if args.take_screenshots:
    take_screenshot(
        pasta_destino_screenshots=args.pasta_destino_screenshots,
        run_number=args.run_number
    )

if args.measure_time:
    print("elapsed time:", time.time() - start_time)

pyautogui.hotkey('ctrl', 'w')

stop_screen(nodes_to_stop)
