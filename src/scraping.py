# TODO: acabar de fazer o crawler dps de acabar de fazer o banco ;)
# - pegar os departamentos no quais os usuários tem interesse do sbd
# - rodar scraping por departamento se conectando no sigaa uma vez
# - salvar output no banco de dados

import mechanicalsoup

from random import random
import time

####################################################################################################
# CONECTAR SOMENTE UMA VEZ A CADA 10 ~ 20 minutos
####################################################################################################

while True:
    # conectar ao SIGAA
    time.sleep(random()*10*60 + 10*60)  # de 10*60 segundos até 20*60 segundos
    browser = mechanicalsoup.StatefulBrowser(user_agent='MechanicalSoup')
    browser.open("https://sig.unb.br/sigaa/public/turmas/listar.jsf")  # <Response [200]>

    ####################################################################################################
    # CRAWLING E EXTRAÇÃO DE DADOS, REPETIR PARA CADA DEPARTAMENTO NO QUAL OS USUÁRIOS TEM INTERESSE
    ####################################################################################################

    # TODO: pegar departamentos do banco
    departamento_list = [673]  # 673 eh a FGA

    for departamento in departamento_list:
        # selecionar o form
        time.sleep(random()*2 + 3)  # 3 a 5 segundos
        browser.select_form('#formTurma')

        # preencher o form
        time.sleep(random()*5 + 3)  # 5 a 8
        browser["formTurma:inputDepto"] = departamento
        # browser["formTurma:inputNivel"] = 'G'  # fuck mestrando doutorando
        # browser["formTurma:inputPeriodo"] = '1'

        # submeter o form
        time.sleep(random()*2 + 4)  # 4 a 6
        response = browser.submit_selected()


        soup = browser.page  # bs4.BeautifulSoup object

        divTurmasAbertas = soup.find("div", {"id": "turmasAbertas"})
        tableTurmasAbertas = divTurmasAbertas.find("table", {"class": "listagem"})

        nome_disciplina = ""
        nome_professor = ""
        for row in tableTurmasAbertas.tbody.find_all('tr'):
            # pegar o tipo de row
            # a row "agrupador" tem os nomes das disciplinas, embaixo dela tem as turmas dessa disciplina
            # as outras rows podem se chamar "linhaImpar" ou "linhaPar", cada uma representa uma turma de uma disciplina
            row_class = row.get('class')[0]
            if row_class == 'agrupador':
                # pegar nome da disciplina
                nome_disciplina = row.find("span", {"class": "tituloDisciplina"}).getText()
                continue
            elif row_class == 'linhaImpar' or row_class == 'linhaPar':
                td_list = row.findAll("td")
                # pegar o nome da/do professor(a)
                nome_professor = row.find("td", {"class": "nome"}).getText()
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
                print(vagas_ofertadas, "|", vagas_ocupadas, "|", nome_disciplina, "|", nome_professor, "|", horario_codificado, "|", horario_decodificado)
                # TODO: salvar no banco de dados com a unique key (codigo do departamento, time.time()) (variável departamento)
            # nem precisa voltar pra página de seleção de forms, já que o form fica acima dos resultados

