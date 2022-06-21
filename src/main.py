####################################################################################################
# DOWNLOAD
####################################################################################################

import mechanicalsoup

# conectar ao SIGAA
browser = mechanicalsoup.StatefulBrowser(user_agent='MechanicalSoup')
browser.open("https://sig.unb.br/sigaa/public/turmas/listar.jsf")  # <Response [200]>

# selecionar o form
browser.select_form('#formTurma')

# preencher o form
browser["formTurma:inputDepto"] = 673  # 673 eh a FGA
# browser["formTurma:inputNivel"] = 'G'
# browser["formTurma:inputPeriodo"] = '1'

response = browser.submit_selected()

####################################################################################################
# PARSE
####################################################################################################

from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, "html.parser")

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
        nome_professor = row.find("td", {"class": "nome"}).getText()
        # TODO: pegar horario da disciplina e traduzir o codigo do SIGAA ("3T45" para "terca de 16h a 18h")
        # TODO: separar o parser da analise de dados
        # pegar a quantidade de vagas ofertadas na disciplina
        td_list = row.findAll("td")
        vagas_ofertadas = td_list[-3].getText()
        vagas_ocupadas = td_list[-2].getText()
        # lidar com o caso de nao haver um numero para representar a quantidade de vagas
        if vagas_ofertadas == '' or vagas_ocupadas == '':
            vagas_ofertadas = 0
            vagas_ocupadas = 0
        else:
            # converter "quantidade de vagas" de str para int
            vagas_ofertadas = int(vagas_ofertadas)
            vagas_ocupadas = int(vagas_ocupadas)
        vagas_disponiveis = vagas_ofertadas - vagas_ocupadas
        print(vagas_disponiveis, "|", nome_disciplina, "|", nome_professor)
