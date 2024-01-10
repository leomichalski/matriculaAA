import os
import time

import requests
from bs4 import BeautifulSoup


def criar_sessao():
    return requests.Session()


def fechar_sessao(session):
    session.close()


def parse_j_id(text):
    return text.split('<input type="hidden" name="javax.faces.ViewState" id="javax.faces.ViewState" value="j_id')[1].split('"')[0]


def abrir_tela_inicial(session):
    # it's important to get the JSESSIONID cookie
    # also important because JSF is a stateful framework
    headers = {
        'Content-Type': 'text/html;charset=utf-8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }
    response = session.get('https://sigaa.unb.br/sigaa/public/turmas/listar.jsf', headers=headers)
    j_id = parse_j_id(response.text)
    return response, j_id


def requisitar_lista_de_turmas(session, nivel='G', departamento_id='653', ano='2023', periodo='4', j_id='1'):
    # session.cookies['JSESSIONID'] is necessary
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://sigaa.unb.br',
        'Referer': 'https://sigaa.unb.br/sigaa/public/turmas/listar.jsf',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }
    data = {
        'formTurma': 'formTurma',
        'formTurma:inputNivel': nivel,
        'formTurma:inputDepto': departamento_id,
        'formTurma:inputAno': ano,
        'formTurma:inputPeriodo': periodo,
        'formTurma:j_id_jsp_1370969402_11': 'Buscar',
        'javax.faces.ViewState': 'j_id' + j_id,
    }
    response = session.post('https://sigaa.unb.br/sigaa/public/turmas/listar.jsf', headers=headers, data=data)
    j_id = parse_j_id(response.text)
    return response, j_id


def salvar_lista_de_turmas(response_text,
                           pasta_arquivos_html,
                           departamento_id):
    # salvar lista de disciplinas em um arquivo .html
    nome_do_arquivo_html = 'dep' + str(departamento_id) + '_' + str(time.time())
    f = open(os.path.join(pasta_arquivos_html, nome_do_arquivo_html), 'w')
    f.write(response_text)
    f.close()
    return nome_do_arquivo_html


def dep_id_from_filename(filename):
    return int(filename.split('_')[0].split('dep')[1])


def timestamp_from_filename(filename):
    return float(filename.split('_')[1].replace('.html', ''))


# parsing da lista gerada pelo metodo salvar_lista_de_turmas
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
        ).read(),
        "html.parser",
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
