# psaux-monitor

Este é um breve guia sobre como configurar e executar o seu projeto.

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)

## Configuração

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Crie um arquivo `.env` na raiz do projeto com suas credenciais SSH:

    ```env
    SSH_HOST=sua_maquina
    SSH_USERNAME=seu_usuario_ssh
    SSH_KEY_PATH=/caminho/para/sua/chave.pem
    ```

3. Execute o seguinte comando para construir e iniciar os containers Docker:

    ```bash
    docker-compose up -d --build
    ```

    Isso irá construir as imagens e iniciar os contêineres no modo detached.

## Acesso ao Projeto

Após a execução bem-sucedida do comando `docker-compose up`, o seu projeto estará acessível em [http://localhost:PORTA](http://localhost:PORTA).

## Parar e Remover Containers

Para parar e remover os containers, execute o seguinte comando:

```bash
docker-compose down
