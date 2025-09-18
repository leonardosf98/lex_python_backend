# Projeto Lex Python Backend

Este projeto foi desenvolvido para uma palestra da **OrangeJuice**, comunidade de tecnologia da FCamara. O objetivo é demonstrar como criar uma API backend em Python para agendamento de consultas odontológicas, integrando com AWS DynamoDB e Lambda, utilizando FastAPI.

## Arquitetura

- **FastAPI**: API REST principal, responsável por receber e gerenciar os agendamentos.
- **AWS DynamoDB**: Banco de dados NoSQL utilizado para armazenar os agendamentos.
- **AWS Lambda**: Função que interage com o Lex (chatbot) e faz requisições à API FastAPI.
- **Lex**: Chatbot da AWS que coleta informações do usuário e aciona a Lambda.

### Fluxo

1. O usuário interage com o Lex para agendar uma consulta.
2. O Lex chama a função Lambda (`lambda_function.py`), que valida os dados e faz uma requisição HTTP para a API FastAPI.
3. A API FastAPI (`main.py`) valida o horário, verifica disponibilidade e registra o agendamento no DynamoDB.
4. O Lex retorna a confirmação ou mensagem de erro ao usuário.

## Configuração

### 1. Instalar dependências

```sh
pip install -r requirements.txt
```

2. Configurar AWS CLI
Execute o comando abaixo e insira suas credenciais (Access Key e Secret Key) de um usuário IAM com permissões para DynamoDB:

```sh
aws configure
```

3. Criar tabela DynamoDB
Execute o comando abaixo para criar a tabela Appointments:

```sh
aws dynamodb create-table \
  --table-name Appointments \
  --attribute-definitions AttributeName=date,AttributeType=S AttributeName=time,AttributeType=S \
  --key-schema AttributeName=date,KeyType=HASH AttributeName=time,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST
```

4. Criar usuário IAM
Acesse o console AWS IAM.
Crie um usuário com permissões para DynamoDB (AmazonDynamoDBFullAccess).
Gere as credenciais (Access Key e Secret Key) e configure no passo anterior.

5. Configurar API_URL na Lambda
No arquivo lambda_function.py, defina o endereço da sua API FastAPI:

```sh
API_URL = "https://<seu-endereco-api>"
```

## Estrutura dos arquivos

- **main.py**: Implementação da API FastAPI.
- **lambda_function.py**: Função Lambda responsável pela integração com o Lex.
- **schema.py**: Definição do modelo de dados para agendamentos.
- **aws.commands.bash**: Script para criação e configuração da tabela DynamoDB.
- **requirements.txt**: Lista de dependências do projeto.

### Observações

- Certifique-se de que a API FastAPI esteja acessível publicamente para que a Lambda consiga realizar requisições.
- Este projeto é destinado apenas para fins educacionais e demonstração na palestra.

**OrangeJuice | FCamara**

Arquivos citados:  
- [main.py](http://_vscodecontentref_/2)  
- [lambda_function.py](http://_vscodecontentref_/3)  
- [schema.py](http://_vscodecontentref_/4)  
- [aws.commands.bash](http://_vscodecontentref_/5)  
- [requirements.txt](http://_vscodecontentref_/6)