import os
import time
import json
from random import randint

from kafka import KafkaProducer

from utils.email import send_email
from utils.sigaa import (
    dep_id_from_filename,
    timestamp_from_filename,
    definir_arquivo_html_mais_recente,
    parse_lista_de_turmas,
)

from database import (
    connect_to_db,
    listar_relacao_turma_interessa_discente
)
from salva_lista_de_turmas_de_um_departamento import (
    main as salva_lista_de_turmas_de_um_departamento
)


def main(pasta_arquivos_html='arquivos_html',
         min_interval_s=150,
         max_interval_s=300,
         db_connection_timeout_s=10):
    KAFKA_TOPIC_VAGA_DISPONIVEL = os.getenv('KAFKA_TOPIC_VAGA_DISPONIVEL')
    KAFKA_SERVER = os.getenv('KAFKA_SERVER')
    KAFKA_PORT = os.getenv('KAFKA_PORT')

    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

    print("Inicializando produtor kafka...")
    producer = KafkaProducer(
        bootstrap_servers=[f'{KAFKA_SERVER}:{KAFKA_PORT}'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    while True:
        # quantidade de segundos que o programa vai esperar entre uma execucao e outra
        # tambem utilizado para calcular o tempo de validade de cada mensagem do topico VAGA_DISPONIVEL
        sleep_duration = randint(min_interval_s, max_interval_s)
        # connect to db if not connected, exit if timeout happens
        print("Conectando ao banco de dados...")
        conn, cursor = connect_to_db(
            db_connection_timeout_s,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        print("Recuperando (do banco de dados) informacoes sobre as turmas que interessam aos discentes...")
        turma_interessa_discente = listar_relacao_turma_interessa_discente(
            cursor
        )
        idx_departamento_previo = -1  # departamento invalido
        for codigo_disciplina, nome_disciplina, nome_docente_turma, horario_codificado_turma, id_discente, email_discente, idx_departamento in turma_interessa_discente:
            if idx_departamento != idx_departamento_previo:
                # faz o webscraping do SIGAA, e salva a pagina html da lista de turmas
                print("Salvando lista do departamento " + str(idx_departamento) + "...")
                salva_lista_de_turmas_de_um_departamento(
                    url_inicial='https://sigaa.unb.br/sigaa/public/turmas/listar.jsf',
                    index_do_departamento_na_lista=idx_departamento,
                    measure_time=True,
                    take_screenshots=False,
                    pasta_destino_screenshots='',
                    pasta_imagens_pyautogui='elementos_das_telas',
                    pasta_arquivos_html=pasta_arquivos_html,
                    run_number=None,
                    pasta_padrao_de_downloads_do_so='/root/Downloads/',
                )
                # vai na pasta de arquivos html, e pega o mais recente do departamento escolhido
                chosen_html_file = definir_arquivo_html_mais_recente(
                    pasta_arquivos_html=pasta_arquivos_html,
                    index_do_departamento_na_lista=idx_departamento,
                )
                print('Arquivo html a ser analisado:', chosen_html_file)
                lista_de_turmas_encontradas = parse_lista_de_turmas(
                    nome_do_arquivo_html=chosen_html_file,
                    pasta_arquivos_html=pasta_arquivos_html,
                )
                # remove turmas que nao tem vagas
                lista_de_turmas_encontradas = [t for t in lista_de_turmas_encontradas if t['quantidade_de_vagas'] >= 1]
                idx_departamento_previo = idx_departamento

            # conferir se a turma desejada esta na lista de turmas encontradas
            # Obs: o tamanho maximo da lista_de_turmas_encontradas eh aprox. 400, a moda eh aprox. 20
            # TODO: somente publicar os IDs das turmas interessantes com vagas disponiveis a fim de diminuir a quantidade de mensagens
            # TODO: criar um node separado para enviar emails
            for turma_encontrada in lista_de_turmas_encontradas:
                if (codigo_disciplina == turma_encontrada['codigo_disciplina']) and \
                   (nome_docente_turma.upper() in turma_encontrada['nome_docente'].upper()) and \
                   (horario_codificado_turma.split()[0] == turma_encontrada['horario_codificado'].split()[0]):
                    print("Encontrou a seguinte turma interessante:", turma_encontrada)
                    producer.send(
                        KAFKA_TOPIC_VAGA_DISPONIVEL,
                        value={
                            'codigo_disciplina': codigo_disciplina,
                            'nome_docente': nome_docente_turma,
                            'horario_codificado': horario_codificado_turma,
                            'id_discente': id_discente,
                            'expire_time': time.time() + sleep_duration,
                        },
                    )
                    # mandar email para o discente
                    send_email(
                        body=f"Entre no sigaa o mais rápido possível\n" \
                             + str(nome_disciplina).lower() + "\n" \
                             + str(nome_docente_turma).lower() + "\n" \
                             + "Quantidade de vagas: " + str(turma_encontrada['quantidade_de_vagas']),
                        subject="Vaga em " + str(nome_disciplina).lower() + "!",
                        receiver_email=email_discente,
                        sender_email=SENDER_EMAIL,
                        sender_password=SENDER_PASSWORD,
                    )
                    break

        print("Dormir por", str(sleep_duration), "segundos antes de conferir o SIGAA novamente.")
        time.sleep(sleep_duration)


if __name__ == '__main__':
    main()
