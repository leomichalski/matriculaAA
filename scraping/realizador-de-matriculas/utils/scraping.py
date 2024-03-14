from easyprocess import EasyProcess
import Xlib.display
import os
import time
import cv2
import numpy as np
# import pyautogui


# divides the rectangle dimension (width or height) into 5 sections
# TODO: parameterize section_quantity
def calc_probabilities(dimension, usual_click_percent=0.25):
    # empty array with 1 as a placeholder (instead of None)
    probs = [1 for _ in range(dimension)]
    usual_click = int(round(dimension * usual_click_percent))
    probs[usual_click] = 16
    # h ends up also being the index
    for h in range(dimension):
        distance_to_usual_click = abs(usual_click - h)
        if distance_to_usual_click == 0:
            continue
        elif             0 < distance_to_usual_click <= dimension*0.2:
             probs[h] = probs[usual_click] * 1
        elif dimension*0.2 < distance_to_usual_click <= dimension*0.4:
             probs[h] = probs[usual_click] * 1/2
        elif dimension*0.4 < distance_to_usual_click <= dimension*0.6:
             probs[h] = probs[usual_click] * 1/4
        elif dimension*0.6 < distance_to_usual_click <= dimension*0.8:
             probs[h] = probs[usual_click] * 1/8
        elif dimension*0.8 < distance_to_usual_click <= dimension*1.0:
             probs[h] = 1
    return probs


def choose_click(width,
                 height,
                 usual_click_width_percent=0.7,
                 usual_click_height_percent=0.25):
    probs_width = calc_probabilities(
        width,
        usual_click_percent=usual_click_width_percent
    )
    probs_height = calc_probabilities(
        height,
        usual_click_percent=usual_click_height_percent
    )
    # normalize probabilities
    probs_width = np.array(probs_width)
    probs_height = np.array(probs_height)
    probs_width /= probs_width.sum()
    probs_height /= probs_height.sum()
    # choose
    x_list = np.random.choice(list(range(width)), size=1, p=probs_width)
    y_list = np.random.choice(list(range(height)), size=1, p=probs_height)
    x = x_list[0]
    y = y_list[0]
    return x, y


def myLocateCenterOnScreen(pyautogui, filename, timeout=15):
    total_time = 0
    start_time = time.time()
    button_center = pyautogui.locateCenterOnScreen(filename)
    # wait a timeout until image is located
    while (button_center is None):
        time.sleep(0.05)
        button_center = pyautogui.locateCenterOnScreen(filename)
        print(time.time() - start_time, timeout)
        if ((time.time() - start_time) > timeout):
            raise Exception("Timeout error when locating '" + filename + "'")
    return button_center


def move_to(pyautogui, filename, xoffset=0, yoffset=0, timeout=15, add_randomness=True):
    button_center = myLocateCenterOnScreen(
        pyautogui=pyautogui, filename=filename, timeout=timeout
    )
    button_height, button_width, _ = cv2.imread(filename).shape
    if add_randomness:
        x_randomness, y_randomness = choose_click(button_width, button_height)
    else:
        x_randomness = 0
        y_randomness = 0
    x_position = button_center.x - button_width//2 + x_randomness + xoffset
    y_position = button_center.y - button_height//2 + y_randomness + yoffset
    # TODO(someday): move the mouse like a human would
    # a funcao moveTo do pyautogui eh blocking (bloqueia a execucao do script ate o mouse chegar no destino)
    pyautogui.moveTo(
        x=x_position,
        y=y_position,
        duration=0.05,
    )
    return (x_position, y_position)


def organizar_janelas(pyautogui, pasta_imagens_pyautogui):
    # maximizar a janela do navegador
    # maximize_window_location = move_to(
    #     pyautogui=pyautogui,
    #     filename=os.path.join(pasta_imagens_pyautogui, 'maximize_window.png'),
    #     add_randomness=False,
    # )
    # print(maximize_window_location)
    pyautogui.moveTo(
        x=1248,
        y=6,
    )
    pyautogui.click()
    # abrir 2 janelas (deixando mais 1 aberta só por garantia)
    pyautogui.hotkey('ctrl', 't')
    pyautogui.hotkey('ctrl', 't')
    # fechar as janelas iniciais do firefox
    pyautogui.hotkey('ctrl', 'tab')
    pyautogui.hotkey('ctrl', 'w')
    pyautogui.hotkey('ctrl', 'w')


def abrir_url(pyautogui, url):
    # clicar no campo de busca do firefox
    pyautogui.moveTo((
        380,
        90
    ))
    pyautogui.click()
    pyautogui.write(url, interval=0.2)
    pyautogui.hotkey('enter')


def cancelar_opcao_de_salvar_senha(pyautogui, pasta_imagens_pyautogui):
    print('Cancelando opcao do firefox de salvar senha...')
    try:
        _ = move_to(
            pyautogui=pyautogui,
            filename=os.path.join(pasta_imagens_pyautogui, 'cancel_firefox_save_password.png'),
            xoffset=60,
        )
        pyautogui.click()
    except:
        print('Opcao do firefox de salvar senha nao encontrada. Continuando...')


def cancelar_opcao_de_traduzir(pyautogui, pasta_imagens_pyautogui):
    print('Cancelando opcao do firefox de traduzir...')
    try:
        _ = move_to(
            pyautogui=pyautogui,
            filename=os.path.join(pasta_imagens_pyautogui, 'cancel_firefox_translate.png'),
            xoffset=40,
        )
        pyautogui.click()
    except:
        print('Opcao do firefox de traduzir nao encontrada. Continuando...')

def start_screen():
    from pyvirtualdisplay.display import Display
    nodes_to_stop = []
    # start xvfb
    disp = Display(visible=True, size=(1680, 1050), backend="xvfb", use_xauth=True)
    disp.start()
    nodes_to_stop.append(disp)
    print("DISPLAY STARTED")
    # start window manager
    # TODO: use GDM3 instead of lightweight fluxbox
    proc_fluxbox = EasyProcess(["fluxbox"])
    proc_fluxbox.start()
    nodes_to_stop.append(proc_fluxbox)
    print("FLUXBOX STARTED")
    # start browser
    proc_firefox = EasyProcess(["firefox"])
    proc_firefox.start()
    nodes_to_stop.append(proc_firefox)
    print("FIREFOX STARTED")
    # can't import pyautogui until after display is started
    import pyautogui
    pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])
    # probably enough time to warm up xvfb and firefox
    time.sleep(3)
    return pyautogui, nodes_to_stop


def stop_screen(nodes_to_stop):
    for node in reversed(nodes_to_stop):
        node.stop()
