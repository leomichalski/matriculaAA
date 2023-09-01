import os
import time
import json
import traceback

from kafka import KafkaConsumer

from utils.database import (
    connect_to_db,
    recupera_discente_por_id,
)
from realiza_uma_matricula import (
    main as realiza_uma_matricula
)


def main(db_connection_timeout_s=60*5,
         message_processing_timeout_s=100):
    KAFKA_TOPIC_VAGA_DISPONIVEL = os.getenv('KAFKA_TOPIC_VAGA_DISPONIVEL')
    KAFKA_SERVER = os.getenv('KAFKA_SERVER')
    KAFKA_PORT = os.getenv('KAFKA_PORT')

    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

    message_consumer = KafkaConsumer(
        KAFKA_TOPIC_VAGA_DISPONIVEL,
        bootstrap_servers=f'{KAFKA_SERVER}:{KAFKA_PORT}',
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        group_id="00",
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for msg in message_consumer:
        # connect to db if not connected, exit if timeout happens
        print('Conectando ao banco de dados...')
        conn, cursor = connect_to_db(
            db_connection_timeout_s,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        processing_msg = True
        start_processing_time = time.time()
        # while ((the message is not expired) and (the message processing timeout isn't reached))
        while processing_msg:
            try:
                if (time.time() >= msg.value['expire_time']):
                    print('Mensagem expirada.')
                    processing_msg = False
                    continue
                if (time.time() - start_processing_time > message_processing_timeout_s):
                    print('Limite de tempo para processar mensagem foi atingido.')
                    processing_msg = False
                    continue
                # busca as informacoes do discente no banco de dados
                print("Recuperando informacoes do discente do banco de dados...")
                info_discente = recupera_discente_por_id(
                    cursor, id_discente=msg.value['id_discente']
                )
                if info_discente is None:
                    print('Discente nao encontrado no banco de dados.')
                    processing_msg = False
                    continue
                matricula, senha, cpf, data_de_nascimento, _ = info_discente
                # faz matricula do discente na turma
                realiza_uma_matricula(
                    url_do_login='https://sigaa.unb.br',
                    matricula=matricula,
                    senha=senha,
                    cpf=cpf,
                    data_de_nascimento=data_de_nascimento.strftime("%d%m%Y"),
                    codigo_disciplina=msg.value['codigo_disciplina'],
                    nome_docente=msg.value['nome_docente'],
                    horario_codificado=msg.value['horario_codificado'],
                    measure_time=True,
                    take_screenshots=False,
                    pasta_imagens_pyautogui='elementos_das_telas',
                    pasta_destino_screenshots='',
                    run_number=None,
                )
                # message processed successfully
                message_consumer.commit()
                break
            except:
                traceback.print_exc()
                time.sleep(0.1)
        else:
            # quit processing the message, go to the next one
            message_consumer.commit()


if __name__ == '__main__':
    main()
