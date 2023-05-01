# nao repara na bagunça S2
import os
import time
import shutil

import cv2
# import pyautogui
from bs4 import BeautifulSoup

from utils.scraping import move_to, myLocateCenterOnScreen


############### METODOS RELACIONADOS A MATRICULA EXTRAORDINARIA ###############

def login_no_sigaa(pyautogui, matricula, senha, pasta_imagens_pyautogui):
    # PASSO: preencher o login do usuário
    # TODO: read image only once
    print('Preenchendo login...')
    usuario_login_button = cv2.imread(
        os.path.join(pasta_imagens_pyautogui, 'usuario_login.png')
    )
    usuario_login_button_width = usuario_login_button.shape[1]
    usuario_login_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'usuario_login.png'),
        xoffset=10+usuario_login_button_width
    )
    pyautogui.click()
    # TODO: my custom write() method with random delay between chars
    # type with quarter-second pause in between each key
    pyautogui.write(matricula, interval=0.25)
    # PASSO: preencher a senha do usuário
    # TODO: read image only once
    print('Preenchendo senha...')
    senha_login_button = cv2.imread(
        os.path.join(pasta_imagens_pyautogui, 'senha_login.png'),
    )
    senha_login_button_width = senha_login_button.shape[1]
    senha_login_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'senha_login.png'),
        xoffset=10+senha_login_button_width
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


############### METODOS RELACIONADOS A LISTAGEM DE DISCIPLINAS ###############

def listar_disciplinas(pyautogui,
                       pasta_imagens_pyautogui,
                       index_do_departamento_na_lista):  # index da FGA eh 
    # selecionar o departamento
    departamento_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'departamento_form.png'),
        add_randomness=False,
        xoffset=120,
        yoffset=5,
    )
    pyautogui.click()
    time.sleep(0.3)
    pyautogui.hotkey('esc')
    time.sleep(0.3)
    for _ in range(index_do_departamento_na_lista):
        time.sleep(0.01)
        pyautogui.hotkey('down')
    # listar as disciplinas
    listar_location = move_to(
        pyautogui=pyautogui,
        filename=os.path.join(pasta_imagens_pyautogui, 'listar_form.png'),
    )
    pyautogui.click()


def salvar_lista_de_turmas_e_fechar_sigaa(pyautogui,
                                          pasta_imagens_pyautogui,
                                          pasta_arquivos_html,
                                          index_do_departamento_na_lista,
                                          pasta_padrao_de_downloads_do_so):
    # esperar lista de disciplinas aparecer
    myLocateCenterOnScreen(
        pyautogui,
        os.path.join(pasta_imagens_pyautogui, 'turmas_encontradas.png'),
        timeout=15
    )
    # salvar lista de disciplinas em um arquivo .html
    nome_do_arquivo_html = 'dep' + str(index_do_departamento_na_lista) + '_' + str(time.time())
    pyautogui.hotkey('ctrl', 's')
    pyautogui.write(nome_do_arquivo_html, interval=0.02)
    pyautogui.hotkey('enter')
    time.sleep(5)
    # mover o arquivo para a pasta adequada
    shutil.move(
        os.path.join(
            pasta_padrao_de_downloads_do_so,
            nome_do_arquivo_html + '.html'
        ),
        os.path.join(
            pasta_arquivos_html,
            nome_do_arquivo_html + '.html'
        )
    )
    # fechar o SIGAA e o firefox
    # TODO: fechar o SIGAA e o firefox EM PARALELO
    time.sleep(10)
    pyautogui.hotkey('ctrl', 'w')
    pyautogui.hotkey('ctrl', 'w')
    pyautogui.hotkey('ctrl', 'w')


def dep_id_from_filename(filename):
    return int(filename.split('_')[0].split('dep')[1])


def timestamp_from_filename(filename):
    return float(filename.split('_')[1].replace('.html', ''))


# define o arquivo mais recente usando o nome do arquivo, nao a data de modificacao
def definir_arquivo_html_mais_recente(pasta_arquivos_html,
                                      index_do_departamento_na_lista):
    html_filename_list = os.listdir(pasta_arquivos_html)
    chosen_html_file = html_filename_list[0]
    for html_filename in html_filename_list[1:]:
        # se o arquivo nao for do departamento escolhido, pular
        if index_do_departamento_na_lista != dep_id_from_filename(html_filename):
            continue
        # se o arquivo for mais antigo que o escolhido, pular
        if timestamp_from_filename(chosen_html_file) > timestamp_from_filename(html_filename):
            continue
        chosen_html_file = html_filename
    return chosen_html_file


# parsing da lista gerada pelo metodo salvar_lista_de_turmas_e_fechar_sigaa
def parse_lista_de_turmas(nome_do_arquivo_html,
                          pasta_arquivos_html):
    lista_de_turmas = []

    soup = BeautifulSoup(
        open(
            os.path.join(
                pasta_arquivos_html,
                nome_do_arquivo_html,
            ),
            mode="r",
            encoding="ISO-8859-1",
        ).read()
    )

    divTurmasAbertas = soup.find("div", {"id": "turmasAbertas"})
    tableTurmasAbertas = divTurmasAbertas.find("table", {"class": "listagem"})

    nome_disciplina = ""
    nome_docente = ""
    for row in tableTurmasAbertas.tbody.find_all('tr'):
        # pegar o tipo de row
        # a row "agrupador" tem os nomes das disciplinas, embaixo dela tem as turmas dessa disciplina
        # as outras rows podem se chamar "linhaImpar" ou "linhaPar", cada uma representa uma turma de uma disciplina
        row_class = row.get('class')[0]
        if row_class == 'agrupador':
            # pegar o nome e o codigo da disciplina
            codigo_disciplina, nome_disciplina = row.find("span", {"class": "tituloDisciplina"}).getText().split(' - ')
            continue
        elif row_class == 'linhaImpar' or row_class == 'linhaPar':
            td_list = row.findAll("td")
            # pegar o nome da/do professor(a)
            nome_docente = row.find("td", {"class": "nome"}).getText()
            # pegar a quantidade de vagas ofertadas na disciplina
            vagas_ofertadas = td_list[-3].getText()
            vagas_ocupadas = td_list[-2].getText()
            # pegar horario da disciplina
            horario_codificado = str(td_list[-5]).split('<td>')[-1].split('<img')[0].strip()
            horario_decodificado = str(td_list[-5].div).partition('>')[-1].replace('<br/>', '\t').replace('</div>','').strip()
            # lidar com o caso de nao haver um numero para representar a quantidade de vagas
            if vagas_ofertadas == '' or vagas_ocupadas == '':
                vagas_ofertadas = 0
                vagas_ocupadas = 0
            else:
                # converter "quantidade de vagas" de str para int
                vagas_ofertadas = int(vagas_ofertadas)
                vagas_ocupadas = int(vagas_ocupadas)
            # print(vagas_ofertadas, "|", vagas_ocupadas, "|", nome_disciplina, "|", nome_docente, "|", horario_codificado, "|", horario_decodificado)
            quantidade_de_vagas = abs(vagas_ofertadas - vagas_ocupadas)
            # TODO: usar outra estrutura de dados para armazenar as turmas
            lista_de_turmas.append(
                {
                    'nome_disciplina': nome_disciplina,
                    'codigo_disciplina': codigo_disciplina,
                    'nome_docente': nome_docente,
                    'horario_codificado': horario_codificado,
                    'quantidade_de_vagas': quantidade_de_vagas,
                }
            )
    return lista_de_turmas
