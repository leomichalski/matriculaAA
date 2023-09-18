# matriculaAA
Bot que realiza matrícula extraordinária pelo SIGAA automaticamente. Favor não DDoS.

- [Como rodar uma instância local com Docker](#como-rodar-uma-instância-local-com-docker)
    - [Construir imagem Docker necessária para construir as outras imagens](#construir-imagem-docker-necessária-para-construir-as-outras-imagens)
    - [Clonar este repositório](#clonar-este-repositório)
    - [Configurar um email para envio de notificações de novas vagas](#configurar-um-email-para-envio-de-notificações-de-novas-vagas)
    - [Construir as imagens Docker](#construir-as-imagens-docker)
    - [Configurar e rodar o painel administrativo](#configurar-e-rodar-o-painel-administrativo)
    - [Rodar o "detector-de-vagas"](#rodar-o-detector-de-vagas)
    - [Rodar o "realizador-de-matriculas"](#rodar-o-realizador-de-matriculas)


## Como rodar uma instância local com Docker
É necessário ter [Docker](https://docs.docker.com/get-docker/) e [docker-compose](https://docs.docker.com/compose/) instalados. Não é seguro rodar uma instância pública desta forma, pois as senhas do Django e do PostgreSQL para desenvolvimento local estão públicas no [repositório do GitHub](https://github.com/leomichalski/matriculaAA).

##### Construir imagem Docker necessária para construir as outras imagens

```
# Clonar o repositório que contém a Dockerfile
git clone https://github.com/leomichalski/pyautogui

# Construir a imagem Docker
docker build pyautogui/docker -t leommiranda/pyautogui
```

##### Clonar este repositório

```
# Clonar o repositório
git clone https://github.com/leomichalski/matriculaAA
```

##### Configurar um email para envio de notificações de novas vagas
Caso o provedor escolhido seja o Gmail, no exemplo abaixo, substituir "leonardomichalskim@gmail.com" pelo endereço de email adequado. Depois, substituir "txkhauissqakizji" por uma [app specific password](https://support.google.com/mail/answer/185833), a senha padrão do Gmail não funciona.

```
# Navegar até este repositório
cd matriculaAA

# Criar arquivo ".envs/.local/.email" que define as variáveis de ambiente necessárias
echo -n "\
SENDER_EMAIL=leonardomichalskim@gmail.com
SENDER_PASSWORD=txkhauissqakizji
" > .envs/.local/.email
```

Obs: a senha "txkhauissqakizji" deste exemplo não funciona mais.

##### Construir as imagens Docker

```
docker-compose -f docker-compose-local.yml build
```

##### Configurar e rodar o painel administrativo
Com a API e o banco de dados, é possível cadastrar estudantes e que turmas interessam a esses estudantes.

```
# Rodar painel
docker-compose -f docker-compose-local.yml up django

# Acessar o painel em localhost:8000/admin . O superusuário é "super" e a senha é "senha12345".
# Agora, basta cadastrar turmas e discentes. Os departamentos já foram populados automaticamente.
```

##### Rodar o "detector-de-vagas"
Com o "detector-de-vagas", é possível acionar alertas quando surge uma vaga que interesse a alguma pessoa. O detector emite dois alertas: o primeiro envia um email à pessoa; o segundo aciona o "realizador-de-matriculas" para fazer a matrícula automática dela.

```
docker-compose -f docker-compose-local.yml up detector-de-vagas
```

##### Rodar o "realizador-de-matriculas"
O "realizador-de-matriculas" recebe alertas do "detector-de-vagas" para fazer matrículas automáticas.

```
docker-compose -f docker-compose-local.yml up realizador-de-matriculas
```


## Como rodar uma instância pública com Docker Compose
É necessário ter [Docker](https://docs.docker.com/get-docker/) e [docker-compose](https://docs.docker.com/compose/) instalados. Também é necessário que a máquina tenha um IP externo público.

##### Acessar um terminal no servidor
Por exemplo, uma forma de accessar um terminal no servidor é o SSH. Todos os seguintes comandos foram pensados para serem rodados diretamente no servidor. 

##### Construir imagem Docker necessária para construir as outras imagens

```
# Clonar o repositório que contém a Dockerfile
git clone https://github.com/leomichalski/pyautogui

# Construir a imagem Docker
docker build pyautogui/docker -t leommiranda/pyautogui
```

##### Clonar este repositório

```
# Clonar o repositório
git clone https://github.com/leomichalski/matriculaAA
```

##### Configurar um email para envio de notificações de novas vagas
Caso o provedor escolhido seja o Gmail, no exemplo abaixo, substituir "leonardomichalskim@gmail.com" pelo endereço de email adequado. Depois, substituir "txkhauissqakizji" por uma [app specific password](https://support.google.com/mail/answer/185833), a senha padrão do Gmail não funciona.

```
# Navegar até este repositório
cd matriculaAA

# Criar arquivo ".envs/.production/.email" que define as variáveis de ambiente necessárias
echo -n "\
SENDER_EMAIL=leonardomichalskim@gmail.com
SENDER_PASSWORD=txkhauissqakizji
" > .envs/.production/.email
```

Obs: a senha "txkhauissqakizji" deste exemplo não funciona mais.

##### Configurar superusuário e senha do painel administrativo
No exemplo abaixo, substituir "TROCAR ESTE EMAIL DE SUPERUSUARIO" e "TROCAR ESTA SENHA DE SUPERUSUARIO" pelos dados adequados. É possível utilizar o arquivo [.envs/.local/.superuser](/.envs/.local/.superuser) como exemplo.

```
# Navegar até este repositório
cd matriculaAA

# Criar pasta caso não exista
mkdir -p .envs/.production

# Criar arquivo ".envs/.production/.superuser" que define as variáveis de ambiente necessárias
echo -n "\
SUPERUSER_EMAIL=TROCAR ESTE EMAIL DE SUPERUSUARIO
SUPERUSER_PASSWORD=TROCAR ESTA SENHA DE SUPERUSUARIO
" > .envs/.production/.superuser
```

##### Configurar variáveis do PostgreSQL
No exemplo abaixo, substituir "NOME DO BANCO", "NOME DE USUARIO DO BANCO" e "SENHA DO USUARIO DO BANCO" pelos dados adequados. É possível utilizar o arquivo [.envs/.local/.postgres](/.envs/.local/.postgres) como exemplo.

```
# Navegar até este repositório
cd matriculaAA

# Criar pasta caso não exista
mkdir -p .envs/.production

# Criar arquivo ".envs/.production/.postgres" que define as variáveis de ambiente necessárias
echo -n "\
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=NOME DO BANCO
POSTGRES_USER=NOME DE USUARIO DO BANCO
POSTGRES_PASSWORD=SENHA DO USUARIO DO BANCO
" > .envs/.production/.postgres
```

##### Configurar variáveis de ambiente do Django

Para gerar uma [chave secreta do Django](https://docs.djangoproject.com/en/dev/ref/settings/#secret-key), basta rodar o seguinte código em Python em um ambiente com o Django instalado.

```
from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())
```

No exemplo abaixo, substituir "CHAVE SECRETA DO DJANGO" pelo chave gerada no passo anterior.

```
# Navegar até este repositório
cd matriculaAA

# Criar pasta caso não exista
mkdir -p .envs/.production

# Criar arquivo ".envs/.production/.django" que define a variável de ambiente necessária
echo -n "\
DJANGO_SECRET_KEY='CHAVE SECRETA DO DJANGO'
" > .envs/.production/.django
```

##### Configurar domínio do servidor como uma variável de ambiente
No exemplo abaixo, substituir "DOMINIO" pelo domínio do servidor (por exemplo, 50.250.100.120.sslip.io ou google.com).

```
# Navegar até este repositório
cd matriculaAA

# Criar pasta caso não exista
mkdir -p .envs/.server_name

# Criar arquivo ".envs/.production/.server_name" que define a variável de ambiente necessária
echo -n "\
SERVER_NAME=DOMINIO
" > .envs/.production/.server_name
```

##### Construir as imagens Docker

```
docker-compose build
```

##### Configurar e rodar o painel administrativo
Com a API e o banco de dados, é possível cadastrar estudantes e que turmas interessam a esses estudantes. Também é criado um proxy reverso, que serve para servir arquivos estáticos e para intermediar com o — protocolo HTTPS — o tráfego externo até a API.

```
# Rodar painel
docker-compose up django

# Acessar o painel em ${DOMINIO}/admin , utilizando superusuário e senha definidos anteriormente.
# Agora, basta cadastrar turmas e discentes. Os departamentos já foram populados automaticamente.
```

##### Rodar o "detector-de-vagas"
Com o "detector-de-vagas", é possível acionar alertas quando surge uma vaga que interesse a alguma pessoa. O detector emite dois alertas: o primeiro envia um email à pessoa; o segundo aciona o "realizador-de-matriculas" para fazer a matrícula automática dela.

```
docker-compose up detector-de-vagas
```

##### Rodar o "realizador-de-matriculas"
O "realizador-de-matriculas" recebe alertas do "detector-de-vagas" para fazer matrículas automáticas.

```
docker-compose up realizador-de-matriculas
```
