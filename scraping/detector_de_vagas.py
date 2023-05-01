import os
import time
from random import randint

from bs4 import BeautifulSoup

from tasks.salva_lista_de_turmas_de_um_departamento import main as salva_lista_de_turmas_de_um_departamento
from utils.email import send_email
from utils.sigaa import (
    dep_id_from_filename,
    timestamp_from_filename,
    definir_arquivo_html_mais_recente,
    parse_lista_de_turmas,
)


# TODO: move to utils.database
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


# TODO: move to utils.database
class Discente:
    def __init__(self,
                 turma_desejada_list,
                 matricula,
                 senha,  # senha do sigaa
                 cpf,
                 data_de_nascimento,
                 email):
        self.turma_desejada_list = turma_desejada_list
        self.matricula = matricula
        self.senha = senha
        self.cpf = cpf
        self.data_de_nascimento = data_de_nascimento
        self.email = email


def main(pasta_arquivos_html='arquivos_html',
         min_interval_s=150,
         max_interval_s=300):
    # TODO: armazenar e recuperar a apropriadamente a lista de disciplinas interessantes e a lista de discentes
    while True:
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
        discente_list = [
            Discente(
                turma_desejada_list=[
                    turma_interessante_list[0],
                ],
                matricula=998877777,
                senha=12345678,
                cpf=11122233344,
                data_de_nascimento='ddmmyyyy',
                email='leonardomichalskim@gmail.com',
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
            salva_lista_de_turmas_de_um_departamento(
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
                        for discente in discente_list:
                            if turma_interessante not in discente.turma_desejada_list:
                                continue
                            # TODO: publish somente_o_ID_(nao a senha)_do_discente_interessado e o id_da_turma_desejada_com_vaga_aberta para o kafka consumer de realizar matricula
                            send_email(
                                body="entre no sigaa o mais rápido possível\n" + str(turma.nome_disciplina).lower() + "\n" + str(turma.nome_docente).lower(),
                                subject="vaga em " + str(turma.nome_disciplina).lower(),
                                sender_password="txkhauissqakizji",
                                receiver_email=discente.email,
                                sender_email='leonardomichalskim@gmail.com'
                            )
        time.sleep(randint(min_interval_s, max_interval_s))


if __name__ == '__main__':
    main()
