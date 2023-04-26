import os

from bs4 import BeautifulSoup

from salva_lista import main as salvar_nova_lista
from email_utils import send_email


class Turma:
    def __init__(self,
                 nome_disciplina,
                 codigo_disciplina,
                 nome_docente,
                 horario_codificado,
                 quantidade_de_vagas,
                 departamento=78):
        self.nome_disciplina = nome_disciplina
        self.codigo_disciplina = codigo_disciplina
        self.nome_docente = nome_docente
        self.horario_codificado = horario_codificado
        self.quantidade_de_vagas = quantidade_de_vagas
        self.departamento = departamento


def dep_id_from_filename(filename):
    return int(filename.split('_')[0].split('dep')[1])


def timestamp_from_filename(filename):
    return float(filename.split('_')[1].replace('.html', ''))


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
            lista_de_turmas.append(
                Turma(
                    nome_disciplina=nome_disciplina,
                    codigo_disciplina=codigo_disciplina,
                    nome_docente=nome_docente,
                    horario_codificado=horario_codificado,
                    quantidade_de_vagas=quantidade_de_vagas,
                    departamento=78,
                )
            )
    return lista_de_turmas


def main(pasta_arquivos_html='arquivos_html'):
    # TODO: run the following code periodically
    # TODO: armazenar e recuperar a apropriadamente a lista de disciplinas interessantes
    # TODO: tambem eh interessante armazenar quem esta interessadx em que disciplina
    turma_interessante_list = [
        Turma(
            nome_disciplina='ESTRUTURAS DE DADOS 2',
            codigo_disciplina='FGA0030',
            nome_docente='BRUNO CESAR RIBAS',
            horario_codificado='35T6 35N1',
            quantidade_de_vagas=None,
            departamento=78,
        )
    ]

    # agrupar turmas por departamento
    departamentos_unicos = {}
    for turma_interessante in turma_interessante_list:
        if departamentos_unicos.get(turma_interessante.departamento) is None:
            departamentos_unicos[turma_interessante.departamento] = []
        departamentos_unicos[turma_interessante.departamento].append(turma_interessante)

    for dep in departamentos_unicos:
        # faz o webscraping do SIGAA, e salva a pagina html da lista de turmas
        salvar_nova_lista(
            url_inicial='https://sigaa.unb.br/sigaa/public/turmas/listar.jsf',
            index_do_departamento_na_lista=dep,
            measure_time=True,
            take_screenshots=False,
            pasta_destino_screenshots='',
            pasta_imagens_pyautogui='elementos_das_telas_da_listagem_de_vagas',
            pasta_arquivos_html=pasta_arquivos_html,
            run_number=None,
            pasta_padrao_de_downloads_do_so='/root/Downloads/',
        )

        # vai na pasta de arquivos html, e pega o mais recente do departamento escolhido
        chosen_html_file = definir_arquivo_html_mais_recente(
            pasta_arquivos_html=pasta_arquivos_html,
            index_do_departamento_na_lista=dep,
        )
        print(chosen_html_file)
        lista_de_turmas = parse_lista_de_turmas(
            nome_do_arquivo_html=chosen_html_file,
            pasta_arquivos_html=pasta_arquivos_html,
        )

        # TODO: otimizar essa busca neh
        for turma in lista_de_turmas:
            if (turma.quantidade_de_vagas < 1):
                continue
            for turma_interessante in departamentos_unicos[dep]:
                if (turma_interessante.codigo_disciplina == turma.codigo_disciplina) and \
                   (turma_interessante.nome_docente.upper() in turma.nome_docente.upper()) and \
                   (turma_interessante.horario_codificado.split()[0] == turma.horario_codificado.split()[0]):
                    # TODO: publish as disciplinas com vagas abertas no kafka
                    send_email(
                        body="entre no sigaa o mais rápido possível\n" + str(turma.nome_disciplina).lower() + "\n" + str(turma.nome_docente).lower(),
                        subject="vaga em " + str(turma.nome_disciplina).lower(),
                        sender_password="txkhauissqakizji",
                        receiver_email='leonardomichalskim@gmail.com',
                        sender_email='leonardomichalskim@gmail.com'
                    )


if __name__ == '__main__':
    main()
