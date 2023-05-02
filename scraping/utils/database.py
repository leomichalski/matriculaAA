import os
import sys
import time
import psycopg2


def connect_to_db(db_connection_timeout_s, **kwargs):
    start_db_connection_time = time.time()
    while True:
        try:
            conn = psycopg2.connect(**kwargs)
            # is connected
            if (conn.closed == 0):
                print('Connected to database.')
                break
            # time limit reached
            if (time.time() - start_db_connection_time > db_connection_timeout_s):
                print('Failed to connect to database.')
                sys.exit(os.EX_TEMPFAIL)
        except:
            time.sleep(1)
    return conn, conn.cursor()


# lista da relacao turma_interessa_discente
def listar_relacao_turma_interessa_discente(cursor):
    cursor.execute("""
        SELECT codigo_disciplina,
               nome_disciplina,
               nome_docente,
               horario_codificado,
               discente_id,
               email,
               departamento_id
        FROM   turmas_turma AS turma,
               discentes_discente_turmas_desejadas AS interessa,
               discentes_discente AS discente
        WHERE  ( interessa.turma_id = turma.id )
               AND ( interessa.discente_id = discente.id )
        ORDER  BY departamento_id;
    """)
    return cursor.fetchall()


# todos os departamentos com turmas que interessam a algum discente
def listar_departamentos_interessantes(cursor):
    cursor.execute("""
        SELECT DISTINCT( departamento_id )
        FROM   discentes_discente_turmas_desejadas AS interessa,
               turmas_turma AS turmas
        WHERE  ( interessa.turma_id = turmas.id );
    """)
    return [row[0] for row in cursor.fetchall()]


def recupera_discente_por_id(cursor, id_discente):
    cursor.execute(
        """
            SELECT matricula, senha, cpf, data_de_nascimento, email
            FROM   discentes_discente as discente
            WHERE  ( discente.id = %s );
        """,
        (id_discente,),
    )
    records = cursor.fetchone()
    if records is None:
        return None
    matricula, senha, cpf, data_de_nascimento, email = records
    matricula = str(matricula).rjust(9, '0')
    cpf = str(cpf).rjust(11, '0')
    return (matricula, senha, cpf, data_de_nascimento, email)


def show_table_columns(cursor, table_name, schema_name='public'):
    cursor.execute(
        """
            SELECT *
            FROM   information_schema.columns
            WHERE  table_schema = %s
            AND    table_name   = %s;
        """,
        (schema_name, table_name)
    )
    return [row[3] for row in cursor.fetchall()]
