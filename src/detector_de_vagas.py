import mechanicalsoup

from random import random
import time

import os
import ssl
import time
import smtplib
from datetime import datetime
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from threading import Thread, Condition

from utils import run_in_parallel


def send_email(body, subject, sender_password,
               receiver_email='leonardomichalskim@gmail.com',
               sender_email='leonardomichalskim@gmail.com',
               file_attachment_list=[]):
    port = 465  # For SSL

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['to'] = receiver_email
    msg.attach(MIMEText(body, 'plain'))

    for filename in file_attachment_list:
        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {os.path.split(filename)[-1]}'
            )
        msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', port,
                          context=ssl.create_default_context()) as server:
        server.login(msg['From'], sender_password)
        server.sendmail(msg['From'], msg['to'], msg.as_string())


####################################################################################################
# CONECTAR SOMENTE UMA VEZ A CADA 10 ~ 20 minutos
####################################################################################################


tentou_se_matricular_em_desenho = False

try:
    while True:
        # conectar ao SIGAA
        print("conectar ao SIGAA")
        conseguiu = False
        while not conseguiu:
            try:
                browser = mechanicalsoup.StatefulBrowser(user_agent='MechanicalSoup')
                browser.open("https://sig.unb.br/sigaa/public/turmas/listar.jsf")  # <Response [200]>
                conseguiu = True
                print("conseguiu conectar ao SIGAA")
            except:
                time.sleep(random()*2 + 3)  # 3 a 5 segundos
                conseguiu = False
                print("aaaaaaa nao conseguiu conectar ao SIGAA")

        ####################################################################################################
        # CRAWLING E EXTRAÇÃO DE DADOS, REPETIR PARA CADA DEPARTAMENTO NO QUAL OS USUÁRIOS TEM INTERESSE
        ####################################################################################################

        # TODO: pegar departamentos do banco
        departamento_list = [
         #   518,  # MAT DEP DE MATEMATICA
            673,  # FGA
          #  514,  # EST DEP DE ESTATISTICA
        ]

        for departamento in departamento_list:
            # selecionar o form
            print("selecionar o form")
            conseguiu = False
            while not conseguiu:
                try:
                    time.sleep(random()*2 + 3)
                    browser.select_form('#formTurma')
                    conseguiu = True
                    print("conseguiu selecionar o form")
                except:
                    conseguiu = False
                    print("aaaaaaa nao conseguiu selecionar o form")

            # preencher o form
            print("preencher o form")
            conseguiu = False
            while not conseguiu:
                try:
                    time.sleep(random()*5 + 3)  # 5 a 8 segundos
                    browser["formTurma:inputDepto"] = departamento
                    # browser["formTurma:inputNivel"] = 'G'  # fuck mestrando doutorando
                    # browser["formTurma:inputPeriodo"] = '1'
                    conseguiu = True
                    print("conseguiu preencher o form")
                except:
                    conseguiu = False
                    print("aaaaaaa nao conseguiu preencher o form")


            # submeter o form
            print("submeter o form")
            conseguiu = False
            while not conseguiu:
                try:
                    time.sleep(random()*2 + 4)  # 4 a 6
                    response = browser.submit_selected()
                    conseguiu = True
                    print("conseguiu submeter o form")
                except:
                    conseguiu = False
                    print("aaaaaaa nao conseguiu submeter o form")

            # listar disciplinas
            print("listar disciplinas")

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
                    # print(vagas_ofertadas, "|", vagas_ocupadas, "|", nome_disciplina, "|", nome_professor, "|", horario_codificado, "|", horario_decodificado)

                    quantidade_de_vagas = abs(vagas_ofertadas - vagas_ocupadas)

                    # if ("MAT0025" in nome_disciplina) and ("246N12" in horario_codificado) and ("ADAIL" in nome_professor):
                    #     if (quantidade_de_vagas <= 30):
                    #         continue
                    #     print(nome_disciplina, quantidade_de_vagas)
                    #     try:
                    #         send_email(
                    #             body="favor entrar no sigaa o mais rápido possível\nacredito que tenha uma vaga na disciplina, mas talvez seja reservada\n\n" + str(nome_disciplina).lower() + "\n" + str(nome_professor).lower()+ "\n" + str(horario_decodificado).lower(),
                    #             subject="vaga em " + str(nome_disciplina).lower(),
                    #             sender_password="txkhauissqakizji",
                    #             receiver_email='luizamvll@gmail.com',
                    #             sender_email='leonardomichalskim@gmail.com'
                    #         )
                    #     except:
                    #         print("EMAIL FALHOU")

                    def a(nome_d, lista):
                        for palavra in lista:
                            if palavra.lower() not in nome_d.lower():
                                return False
                        return True

                    if a(nome_disciplina, ['arquitetura', 'desenho', 'software']):
                        print(quantidade_de_vagas, 'vagas em arquitetura com', nome_professor.split()[0].capitalize())
                        #try:
                        #    send_email(
                        #        body="teste da notificacao\n",
                        #        subject="teste da notificacao\n",
                        #        sender_password="txkhauissqakizji",
                        #        receiver_email='leonardomichalskim@gmail.com',
                        #        sender_email='leonardomichalskim@gmail.com'
                        #    )
                        #except:
                        #    print("EMAIL FALHOU")

                    if quantidade_de_vagas <= 0:
                        continue

                    if a(nome_disciplina, ['arquitetura', 'desenho', 'software']):
                        for _ in range(20):
                            print('@'*80)
                        print(nome_disciplina, 'vagas:', quantidade_de_vagas, 'prof:', nome_professor.split()[0], 'horario:', horario_codificado)
                        for _ in range(20):
                            print('@'*80)
                        try:
                            tentou_se_matricular_em_desenho = True
                            run_in_parallel("""
                            docker run --rm -it -v ${PWD}:/curr -w /curr leommiranda/pyautogui \
                              python3 realiza_matricula.py --measure-time --take-screenshots \
                              --matricula="190046945" --senha="" --cpf="07554385151" \
                              --data-de-nascimento="13102000" \
                              --codigo-disciplina="FGA0208" --nome-docente="MILENE SERRANO" \
                              --horario-codificado="26M12" \
                              --pasta-destino-screenshots="screenshots" \
                              --pasta-imagens-pyautogui="images_to_locate"
                            """)

                        except:
                            print("MATRICULA FALHOU")
                        try:
                            send_email(
                                body="entre no sigaa o mais rápido possível\n" + str(nome_disciplina).lower() + "\n" + str(nome_professor).lower(),
                                subject="vaga em " + str(nome_disciplina).lower(),
                                sender_password="txkhauissqakizji",
                                receiver_email='leonardomichalskim@gmail.com',
                                sender_email='leonardomichalskim@gmail.com'
                            )
                        except:
                            print("EMAIL FALHOU")

#                    if a(nome_disciplina, ['sistema', 'banco', 'dado', '2']):
#                        print(nome_disciplina, 'vagas:', quantidade_de_vagas, 'prof:', nome_professor.split()[0], 'horario:', horario_codificado)

#                    if a(nome_disciplina, ['ricos para engenharia']) and 'rodrigo' in nome_professor.lower():
#                        print(nome_disciplina, 'vagas:', quantidade_de_vagas, 'prof:', nome_professor.split()[0], 'horario:', horario_codificado)

#                    if a(nome_disciplina, ['compilador']):
#                        print(nome_disciplina, 'vagas:', quantidade_de_vagas, 'prof:', nome_professor.split()[0], 'horario:', horario_codificado)

#                    if a(nome_disciplina, ['o e qualidade']):
#                        print(nome_disciplina, 'vagas:', quantidade_de_vagas, 'prof:', nome_professor.split()[0], 'horario:', horario_codificado)

#                    if a(nome_disciplina, ['fundamentos de sistemas operacionais']):
#                        print(nome_disciplina, 'vagas:', quantidade_de_vagas, 'prof:', nome_professor.split()[0], 'horario:', horario_codificado)

#                    if a(nome_disciplina, ['estrutura', 'dado', '2']):
#                        print(nome_disciplina, 'vagas:', quantidade_de_vagas, 'prof:', nome_professor.split()[0], 'horario:', horario_codificado)


        # nem precisa voltar pra página de seleção de forms, já que o form fica acima dos resultados
        print("dormir antes de repetir.")
        print(datetime.now())
        print('#'*125)
        print()
        print()
        del browser
        del soup
        #time.sleep(random()*5*60 + 5*60)  # de 5*60 segundos até 10*60 segundos
        tempo_ate_acordar = int(random()*2.5*60 + 2.5*60)  # de 2.5*60 segundos até 5*60 segundos
        time.sleep(tempo_ate_acordar)
        # time.sleep(random()*10*60 + 10*60)  # de 10*60 segundos até 20*60 segundos
except:
    pass

