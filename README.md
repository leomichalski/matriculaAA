# matriculaAA

#### :x: Não participe de um ataque DDoS.
#### :x: Evite rodar uma nova instância do projeto. Vamos evitar que o SIGAA fique indisponível.
#### :white_check_mark: Considere me enviar um email em [leonardomichalskim@gmail.com](mailto:leonardomichalskim@gmail.com).
#### :white_check_mark: Se achou útil e quer me encorajar a dar manutenção ao projeto, é só deixar uma estrelinha :star:.

A ideia deste projeto é melhorar a experiência com o SIGAA, chega de desperdiçar os primeiros dias da matrícula extraordinária ansiosamente apertando F5 a cada 5 minutos. Permita que um bot faça a sua matrícula caso encontre uma vaga que você deseja.

## Sumário


- [Como rodar uma instância local com Docker Compose](#como-rodar-uma-instância-local-com-docker-compose)
- [Como rodar uma instância pública com Docker Compose](#como-rodar-uma-instância-pública-com-docker-compose)
- [Como rodar uma instância (local ou pública) com Kubernetes](#como-rodar-uma-instância-local-ou-pública-com-kubernetes)


## Como rodar uma instância local com Docker Compose
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

# Criar arquivo ".envs/.local/.email" com o email
echo -n "\
SENDER_EMAIL=leonardomichalskim@gmail.com
" > .envs/.local/.email

# Criar arquivo ".envs/.local/.email_password" com a senha do email
echo -n "\
SENDER_PASSWORD=txkhauissqakizji
" > .envs/.local/.email_password
```

Obs: a senha "txkhauissqakizji" deste exemplo não funciona mais.


##### Construir as imagens Docker

```
docker compose -f deploy/compose/docker-compose-local.yml --project-directory . build
```

##### Configurar e rodar o painel administrativo
Com a API e o banco de dados, é possível cadastrar estudantes e que turmas interessam a esses estudantes.

```
# Rodar painel
docker compose -f deploy/compose/docker-compose-local.yml --project-directory . up django

# Acessar o painel em localhost:8000/admin . O superusuário é "super" e a senha é "senha12345".
# Agora, basta cadastrar turmas e discentes. Os departamentos já foram populados automaticamente.
```

##### Rodar o "detector-de-vagas"
Com o "detector-de-vagas", é possível acionar alertas quando surge uma vaga que interesse a alguma pessoa. O detector emite dois alertas: o primeiro envia um email à pessoa; o segundo aciona o "realizador-de-matriculas" para fazer a matrícula automática dela.

```
docker compose -f deploy/compose/docker-compose-local.yml --project-directory . up detector-de-vagas
```

##### Rodar o "realizador-de-matriculas"
O "realizador-de-matriculas" recebe alertas do "detector-de-vagas" para fazer matrículas automáticas.

```
docker compose -f deploy/compose/docker-compose-local.yml --project-directory . up realizador-de-matriculas
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

# Criar arquivo ".envs/.production/.email" com o email
echo -n "\
SENDER_EMAIL=leonardomichalskim@gmail.com
" > .envs/.production/.email

# Criar arquivo ".envs/.production/.email_password" com a senha do email
echo -n "\
SENDER_PASSWORD=txkhauissqakizji
" > .envs/.production/.email_password
```

Obs: a senha "txkhauissqakizji" deste exemplo não funciona mais.

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

##### Configurar variáveis de ambiente do Django, incluindo superusuário e senha do painel administrativo

Para gerar uma [chave secreta do Django](https://docs.djangoproject.com/en/dev/ref/settings/#secret-key), basta rodar o seguinte código em Python em um ambiente com o Django instalado.

```
from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())
```

No exemplo abaixo, substituir "CHAVE SECRETA DO DJANGO" pelo chave gerada no passo anterior. Substituir "TROCAR ESTE EMAIL DE SUPERUSUARIO" e "TROCAR ESTA SENHA DE SUPERUSUARIO" pelos dados adequados. É possível utilizar o arquivo [.envs/.local/.django](/.envs/.local/.django) como exemplo.

```
# Navegar até este repositório
cd matriculaAA

# Criar pasta caso não exista
mkdir -p .envs/.production

# Criar arquivo ".envs/.production/.django" que define as variáveis de ambiente necessárias
echo -n "\
DJANGO_SECRET_KEY='CHAVE SECRETA DO DJANGO'
SUPERUSER_EMAIL=TROCAR ESTE EMAIL DE SUPERUSUARIO
SUPERUSER_PASSWORD=TROCAR ESTA SENHA DE SUPERUSUARIO
" > .envs/.production/.django
```

##### Configurar domínio do servidor como uma variável de ambiente
No exemplo abaixo, substituir "DOMINIO" pelo domínio do servidor (por exemplo, 50.250.100.120.sslip.io ou google.com). Dica: usar `.nip.io` ou `.sslip.io` caso não haja um domínio disponível.

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
docker compose -f deploy/compose/docker-compose.yml --project-directory . build
```

##### Configurar e rodar o painel administrativo
Com o banco de dados (postgres) e o painel (django), é possível cadastrar estudantes e que turmas interessam a esses estudantes. Neste caso, o proxy reverso (nginx) serve para servir arquivos estáticos e para intermediar com o — protocolo HTTPS — o tráfego externo até a API. O cerbot mantém atualizados os certicados SSL usados no protocolo HTTPS.

```
# Rodar painel
docker compose -f deploy/compose/docker-compose.yml --project-directory . up postgres django nginx certbot

# Acessar o painel em ${DOMINIO}/admin , utilizando superusuário e senha definidos anteriormente.
# Agora, basta cadastrar turmas e discentes. Os departamentos já foram populados automaticamente.
```

##### Rodar o "detector-de-vagas"
Com o "detector-de-vagas", é possível acionar alertas quando surge uma vaga que interesse a alguma pessoa. O detector emite dois alertas: o primeiro envia um email à pessoa; o segundo aciona o "realizador-de-matriculas" para fazer a matrícula automática dela.

```
docker compose -f deploy/compose/docker-compose.yml --project-directory . up detector-de-vagas
```

##### Rodar o "realizador-de-matriculas"
O "realizador-de-matriculas" recebe alertas do "detector-de-vagas" para fazer matrículas automáticas.

```
docker compose -f deploy/compose/docker-compose.yml --project-directory . up realizador-de-matriculas
```


## Como rodar uma instância (local ou pública) com Kubernetes
É necessário que o cluster Kubernetes tenha acesso Docker Registry onde as imagens são armazenadas.

##### Requisitos

* Servidor PostgreSQL rodando a parte. Foram testadas as versões 14 e 15.
* Ferramenta [ingress-nginx](https://github.com/kubernetes/ingress-nginx) instalada no cluster.
* Ferramenta [cert-manager](https://github.com/cert-manager/cert-manager) instalada no cluster.
* Ferramenta [strimzi-kafka-operator](https://github.com/strimzi/strimzi-kafka-operator) instalada no cluster. Também pode ser instalada como dependência do chart, basta utilizar `helm install (...) --set strimzi.enabled=true`. Caso for instalada separada do chart, talvez seja necessário modificar alguns values `helm install (...) --set strimzi.kafka.listener.port=9092 --set strimzi.clusterName='kafka-cluster'`

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

# Navegar até este repositório
cd matriculaAA
```

##### Construir as imagens Docker

```
docker compose -f deploy/compose/docker-compose.yml --project-directory . build django detector-de-vagas realizador-de-matriculas
```

##### Subir imagens construídas para o Docker Registry

Depende do Docker Registry utilizado (DockerHub, AWS ECR, etc) e da distribuição do Kubernetes (kind, k3s, RKE, etc).

##### Rodar os bots ("detector-de-vagas" e "realizador-de-matriculas") com um painel administrativo local

```
helm upgrade --install matriculaaa deploy/k8s/charts/matriculaaa --set endpoint=localhost --set externalAccess.enabled=false --set debug=true

# Aguardar, e acessar o painel administrativo em localhost:31000/admin
```

Também é necessário setar o restante dos "values" requeridos, conforme consta na tabela do [README.md do Helm chart](deploy/k8s/charts/matriculaaa/README.md). Principalmente, os "values" relacionados ao servidor PostgreSQL.

##### Rodar os bots ("detector-de-vagas" e "realizador-de-matriculas") com um painel administrativo público

Configurar os "Helm chart values" da instalação de acordo com o [README.md do chart](deploy/k8s/charts/matriculaaa/README.md). Então, instalar com o seguinte comando.

```
helm upgrade --install matriculaaa deploy/k8s/charts/matriculaaa --set endpoint=SUBSTITUIR_PELO_DOMINIO_PUBLICO

# Aguardar, e acessar o painel administrativo em SUBSTITUIR_PELO_DOMINIO_PUBLICO
```

Também é necessário setar o restante dos "values" requeridos, conforme consta na tabela do [README.md do Helm chart](deploy/k8s/charts/matriculaaa/README.md). Principalmente, os "values" relacionados ao servidor PostgreSQL.

A depender do Docker Registry, talvez seja necessário alterar os nomes das imagens Docker (`django.container.image`, `detectorDeVagas.container.image` e `realizadorDeMatriculas.container.image`) e as tags das imagens Docker (`django.container.tag`, `detectorDeVagas.container.tag` e `realizadorDeMatriculas.container.tag`).

Dica: usar o IP externo com o final `.nip.io` ou `.sslip.io` caso não haja um domínio público disponível.
