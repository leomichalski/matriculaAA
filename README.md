# matriculaAA
Bot que realiza matrícula extraordinária pelo SIGAA automaticamente. Favor não DDoS.

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

##### Construir o docker-compose.yml

```
docker-compose build
```

##### Configurar e rodar o painel administrador
Com a API e o banco de dados, é possível cadastrar estudantes e que turmas interessam a esses estudantes.

```
# Rodar painel
docker-compose up node

# Acessar o painel em localhost:8000/admin . O superusuário é "super" e a senha é "senha12345".
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
