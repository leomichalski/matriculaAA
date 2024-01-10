# nao repara na bagunça S2
import os
import time

import cv2
# import pyautogui

from utils.scraping import move_to, myLocateCenterOnScreen


def login_no_sigaa(pyautogui, matricula, senha, pasta_imagens_pyautogui):
    # PASSO: preencher o login do usuário
    # TODO: read image only once
    print('Preenchendo login...')
    usuario_login_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'usuario_login.png'),
    )
    pyautogui.click()
    # TODO: my custom write() method with random delay between chars
    # type with quarter-second pause in between each key
    pyautogui.write(matricula, interval=0.25)
    # PASSO: preencher a senha do usuário
    # TODO: read image only once
    print('Preenchendo senha...')
    senha_login_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'senha_login.png'),
    )
    pyautogui.click()
    pyautogui.write(senha, interval=0.25)
    # PASSO: clicar no botao de login
    print('Logando...')
    entrar_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'entrar_login.png'),
    )
    pyautogui.click()
    # PASSO: garantir que a pagina está no menu discente
    print('Indo para o menu discente...')
    menu_discente_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'menu_discente.png'),
    )
    pyautogui.click()
    time.sleep(2)


def preencher_campo_chatinho(pyautogui, valor, pasta_imagens_pyautogui):
    # cobrir o caso de o campo chatinho nao existir
    if valor is None:
        return
    # caso de o campo ser o CPF, a data de nascimento ou a matricula
    senha_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'senha_matricula.png'),
        xoffset=60,
        yoffset=-25,
    )
    pyautogui.click()
    pyautogui.write(valor, interval=0.25)


def descobrir_qual_eh_o_campo_chatinho(pyautogui, cpf,
                                       data_de_nascimento,
                                       matricula,
                                       pasta_imagens_pyautogui):
    pyautogui.hotkey('ctrl', 'f')
    # o campo eh o CPF
    pyautogui.write('CPF:', interval=0.02)
    time.sleep(0.3)
    if pyautogui.locateCenterOnScreen(os.path.join(pasta_imagens_pyautogui, 'ctrl_f_achou.png')) is not None:
        # escrever CPF
        return cpf
    # o campo eh a data de nascimento
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.write('Data de Nascimento:', interval=0.02)
    time.sleep(0.3)
    if pyautogui.locateCenterOnScreen(os.path.join(pasta_imagens_pyautogui, 'ctrl_f_achou.png')) is not None:
        return data_de_nascimento
    # o campo eh o numero de matricula
    # TODO: descobrir se o SIGAA usa "matricula" ou "usuario"
    # obs: o ctrl+f nao se importa com acentuacao
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.write('Matricula:', interval=0.02)
    time.sleep(0.3)
    if pyautogui.locateCenterOnScreen(os.path.join(pasta_imagens_pyautogui, 'ctrl_f_achou.png')) is not None:
        return matricula
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.write('Usuario:', interval=0.02)
    time.sleep(0.3)
    if pyautogui.locateCenterOnScreen(os.path.join(pasta_imagens_pyautogui, 'ctrl_f_achou.png')) is not None:
        return matricula
    # nao tem campo extra, somente precisa preencher a senha
    return None


def ir_pra_matricula_extraordinaria(pyautogui, pasta_imagens_pyautogui):
    # PASSO: abrir a seção da matricula extraordinaria
    ensino_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'ensino_navbar.png')
    )
    matricula_online_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'matricula_online_navbar.png'),
    )
    realizar_matricula_extraordinaria_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'realizar_matricula_extraordinaria_navbar.png'),
    )
    pyautogui.click()


def concordar_com_cookies(pyautogui, pasta_imagens_pyautogui):
    _ = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'ciente_dos_cookies.png'),
    )
    pyautogui.click()


def buscar_disciplina_matricula_extraordinaria(pyautogui, codigo_disciplina,
                                               nome_docente,
                                               horario_codificado,
                                               pasta_imagens_pyautogui):
    # PASSO: buscar disciplina desejada
    # "SUBPASSO": preencher codigo da disciplina
    print('Preenchendo codigo da disciplina...')
    codigo_disciplina_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'codigo_disciplina_form.png'),
        xoffset=186,
    )
    pyautogui.click()
    pyautogui.write(codigo_disciplina, interval=0.25)
    # "SUBPASSO": preencher nome do docentev
    print('Preenchendo nome do docente...')
    nome_docente_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'nome_docente_form.png'),
        xoffset=250,
    )
    pyautogui.click()
    pyautogui.write(nome_docente, interval=0.25)
    # "SUBPASSO": preencher horario da disciplina
    print('Preenchendo horario da disciplina...')
    horario_codificado_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'horario_codificado_form.png'),
        xoffset=203,
    )
    pyautogui.click()
    pyautogui.write(horario_codificado, interval=0.25)
    # "SUBPASSO": clicar no botao de "buscar"
    print('Buscando disciplina...')
    buscar_disciplina_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'buscar_disciplina_form.png'),
    )
    pyautogui.click()
    # PASSO: clicar no botao para se matricular na disciplina
    # obs: eh importante que somente haja uma unica disciplina na lista
    print('Indo para a pagina de confirmar matricula...')
    # pyautogui.hotkey('ctrl', 'end')
    # pyautogui.moveTo(
    #     x=ref_center.x+100,
    #     y=ref_center.y+200,
    # )
    # pyautogui.click()

    ref_center = myLocateCenterOnScreen(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'turmas_encontradas_ref.png'),
    )
    pyautogui.moveTo(
        x=ref_center.x+478,
        y=ref_center.y+65,
    )
    pyautogui.click()


def confirmar_dados_matricula_extraordinaria(pyautogui, cpf,
                                             data_de_nascimento,
                                             matricula,
                                             senha,
                                             pasta_imagens_pyautogui):
    # PASSO: colocar a senha e preencher o campo chatinho
    # campo chatinho: campo que pode ser o CPF, a data de nascimento, a matricula ou simplesmente nao existir
    print('Preenchendo senha...')
    senha_matricula_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'senha_matricula.png'),
        xoffset=60
    )
    pyautogui.click()
    pyautogui.write(senha, interval=0.25)
    #
    print('Preenchendo campo extra (cpf, data de nascimento, matricula ou nada)...')
    valor_do_campo_chatinho = descobrir_qual_eh_o_campo_chatinho(
        pyautogui=pyautogui,
        cpf=cpf,
        data_de_nascimento=data_de_nascimento,
        matricula=matricula,
        pasta_imagens_pyautogui=pasta_imagens_pyautogui,
    )
    preencher_campo_chatinho(
        pyautogui=pyautogui,
        valor=valor_do_campo_chatinho,
        pasta_imagens_pyautogui=pasta_imagens_pyautogui,
    )
    # PASSO: clicar no botao de "matricular"
    pyautogui.hotkey('enter')
    pyautogui.hotkey('enter')
    pyautogui.hotkey('enter')
    # PASSO: esperar 20 segundos pra ter certeza de que deu certo
    # TODO: em vez de esperar 20 segundos, esperar ate que algum
    # elemento especifico apareca na tela.
    time.sleep(20)
