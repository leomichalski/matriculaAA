import os
import time
from random import randint

from utils.email import send_email
from utils.sigaa import (
    dep_id_from_filename,
    timestamp_from_filename,
    definir_arquivo_html_mais_recente,
    parse_lista_de_turmas,
)
from utils.database import (
    connect_to_db,
    listar_relacao_turma_interessa_discente
)
from tasks.salva_lista_de_turmas_de_um_departamento import (
    main as salva_lista_de_turmas_de_um_departamento
)


def main(pasta_arquivos_html='arquivos_html',
         min_interval_s=150,
         max_interval_s=300,
         db_connection_timeout_s=60*5):
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

    while True:
        # connect to db if not connected, exit if timeout happens
        conn, cursor = connect_to_db(
            db_connection_timeout_s,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        turma_interessa_discente = listar_relacao_turma_interessa_discente(
            cursor
        )
        idx_departamento_previo = -1  # departamento invalido
        for codigo_disciplina, nome_disciplina, nome_docente_turma, horario_codificado_turma, id_discente, email_discente, idx_departamento in turma_interessa_discente:
            if idx_departamento != idx_departamento_previo:
                # faz o webscraping do SIGAA, e salva a pagina html da lista de turmas
                salva_lista_de_turmas_de_um_departamento(
                    url_inicial='https://sigaa.unb.br/sigaa/public/turmas/listar.jsf',
                    index_do_departamento_na_lista=idx_departamento,
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
                    index_do_departamento_na_lista=idx_departamento,
                )
                lista_de_turmas_encontradas = parse_lista_de_turmas(
                    nome_do_arquivo_html=chosen_html_file,
                    pasta_arquivos_html=pasta_arquivos_html,
                )
                # remove turmas que nao tem vagas
                lista_de_turmas_encontradas = [t for t in lista_de_turmas_encontradas if t['quantidade_de_vagas'] >= 1]
                idx_departamento_previo = idx_departamento

            # conferir se a turma desejada esta na lista de turmas encontradas
            # Obs: o tamanho maximo da lista_de_turmas_encontradas eh aprox. 400, a moda eh aprox. 20
            for turma_encontrada in lista_de_turmas_encontradas:
                if (codigo_disciplina == turma_encontrada['codigo_disciplina']) and \
                   (nome_docente_turma.upper() in turma_encontrada['nome_docente'].upper()) and \
                   (horario_codificado_turma.split()[0] == turma_encontrada['horario_codificado'].split()[0]):
                    # TODO: publish discente.id and turma.id to kafka
                    # mandar email para o discente
                    send_email(
                        body="entre no sigaa o mais rápido possível\n" + str(nome_disciplina).lower() + "\n" + str(nome_docente_turma).lower(),
                        subject="vaga em " + str(nome_disciplina).lower(),
                        sender_password="txkhauissqakizji",
                        receiver_email=email_discente,
                        sender_email='leonardomichalskim@gmail.com'
                    )
                    break
        sleep_duration = randint(min_interval_s, max_interval_s)
        print("Dormir por", str(sleep_duration), "segundos antes de conferir o SIGAA novamente.")
        time.sleep(sleep_duration)


if __name__ == '__main__':
    main()
