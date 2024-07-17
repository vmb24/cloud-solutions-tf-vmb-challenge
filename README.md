# Terrafarming Application

## Visão Geral

Este repositório contém o código para os microserviços e funções Lambda do aplicativo Terrafarming, junto com a configuração da infraestrutura AWS usando Terraform. O Terrafarming é um aplicativo de agricultura inteligente que utiliza inteligência artificial para fornecer recomendações aos agricultores com base em métricas do solo e condições climáticas.

## Estrutura do Repositório

```plaintext
.
|-services
├── microservices/
│   ├── farmer-service/
│   │   ├── app/
│   │   │   ├── controllers/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   ├── services/
│   │   │   ├── utils/
│   │   │   ├── main.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── soil-metrics-service/
│   │   ├── app/
│   │   │   ├── controllers/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   ├── services/
│   │   │   ├── utils/
│   │   │   ├── main.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── crop-health-service/
│   │   ├── app/
│   │   │   ├── controllers/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   ├── services/
│   │   │   ├── utils/
│   │   │   ├── main.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── equipment-health-service/
│   │   ├── app/
│   │   │   ├── controllers/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   ├── services/
│   │   │   ├── utils/
│   │   │   ├── main.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── weather-service/
│   │   ├── app/
│   │   │   ├── controllers/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   ├── services/
│   │   │   ├── utils/
│   │   │   ├── main.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── greenhouse-service/
│   │   ├── app/
│   │   │   ├── controllers/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   ├── services/
│   │   │   ├── utils/
│   │   │   ├── main.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
├── lambdas/
│   ├── image-analysis/
│   │   ├── lambda_function.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── weather-recommendation/
│   │   ├── lambda_function.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── modules/
│   │   ├── microservices/
│   │   │   ├── farmer-service/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   ├── outputs.tf
│   │   │   ├── soil-metrics-service/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   ├── outputs.tf
│   │   │   ├── crop-health-service/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   ├── outputs.tf
│   │   │   ├── equipment-health-service/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   ├── outputs.tf
│   │   │   ├── weather-service/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   ├── outputs.tf
│   │   │   ├── greenhouse-service/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   ├── outputs.tf
│   │   ├── lambdas/
│   │   │   ├── image-analysis/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   ├── outputs.tf
│   │   │   ├── weather-recommendation/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   ├── outputs.tf
├── README.md
└── scripts/
    ├── build_and_push.sh

```

Microserviços
-------------

### Farmer Service

O `farmer-service` gerencia informações dos agricultores, incluindo operações CRUD.

#### Endpoints

-   `POST /farmers`: Cria um novo agricultor.
-   `GET /farmers/{id}`: Obtém informações de um agricultor.
-   `PUT /farmers/{id}`: Atualiza informações de um agricultor.
-   `DELETE /farmers/{id}`: Deleta um agricultor.

### Soil Metrics Service

O `soil-metrics-service` gerencia as métricas do solo (pH, umidade, temperatura).

#### Endpoints

-   `POST /soil-metrics`: Adiciona métricas do solo.
-   `GET /soil-metrics/{id}`: Obtém métricas do solo.
-   `PUT /soil-metrics/{id}`: Atualiza métricas do solo.
-   `DELETE /soil-metrics/{id}`: Deleta métricas do solo.

### Crop Health Service

O `crop-health-service` gerencia a saúde das colheitas.

#### Endpoints

-   `POST /crop-health`: Adiciona informações de saúde da colheita.
-   `GET /crop-health/{id}`: Obtém informações de saúde da colheita.
-   `PUT /crop-health/{id}`: Atualiza informações de saúde da colheita.
-   `DELETE /crop-health/{id}`: Deleta informações de saúde da colheita.

### Equipment Health Service

O `equipment-health-service` gerencia a saúde dos equipamentos agrícolas.

#### Endpoints

-   `POST /equipment-health`: Adiciona informações de saúde dos equipamentos.
-   `GET /equipment-health/{id}`: Obtém informações de saúde dos equipamentos.
-   `PUT /equipment-health/{id}`: Atualiza informações de saúde dos equipamentos.
-   `DELETE /equipment-health/{id}`: Deleta informações de saúde dos equipamentos.

### Weather Service

O `weather-service` fornece informações climáticas e previsões.

#### Endpoints

-   `GET /weather/current`: Obtém informações climáticas atuais.
-   `GET /weather/forecast`: Obtém previsões climáticas.

### Greenhouse Service

O `greenhouse-service` gerencia informações das estufas.

#### Endpoints

-   `POST /greenhouse`: Adiciona uma nova estufa.
-   `GET /greenhouse/{id}`: Obtém informações de uma estufa.
-   `PUT /greenhouse/{id}`: Atualiza informações de uma estufa.
-   `DELETE /greenhouse/{id}`: Deleta uma estufa.

Funções Lambda
--------------

### Image Analysis

A função `image-analysis` utiliza o Amazon Rekognition para analisar imagens e fornecer métricas.

### Weather Recommendation

A função `weather-recommendation` fornece recomendações com base nas condições climáticas e métricas do solo.

Conceitos Utilizados
--------------------

### SOLID

Os princípios SOLID foram aplicados para garantir que os microserviços sejam bem projetados e manteníveis:

-   **Single Responsibility Principle (SRP)**: Cada classe tem uma única responsabilidade.
-   **Open/Closed Principle (OCP)**: As classes estão abertas para extensão, mas fechadas para modificação.
-   **Liskov Substitution Principle (LSP)**: As subclasses podem ser substituídas por suas classes base.
-   **Interface Segregation Principle (ISP)**: Muitas interfaces específicas são melhores do que uma interface única.
-   **Dependency Inversion Principle (DIP)**: Dependa de abstrações, não de implementações concretas.

### Linguagem e Tecnologias

-   **Linguagem**: Python
-   **Infraestrutura**: AWS (ECS, ECR, Lambda, Terraform)
-   **Bibliotecas de IA**: Amazon Rekognition, Amazon Bedrock e Amazon SageMaker

Configuração e Implantação
--------------------------

### Pré-requisitos

-   Docker
-   AWS CLI configurado
-   Terraform instalado

### Instruções de Configuração

1.  Clone o repositório:

    sh

    Copiar código

    `git clone https://github.com/seu-usuario/terrafarming.git
    cd terrafarming`

2.  Configure suas credenciais AWS e inicialize o Terraform:

    sh

    Copiar código

    `cd terraform
    terraform init`

3.  Aplique a configuração do Terraform:

    sh

    Copiar código

    `terraform apply`

4.  Construa e envie as imagens Docker para o ECR:

    sh

    Copiar código

    `cd scripts
    ./build_and_push.sh`

### Executando os Microserviços

Cada microserviço pode ser executado localmente usando Docker Compose ou implantado no ECS conforme definido nos arquivos Terraform.

Contribuições
-------------

Contribuições são bem-vindas! Por favor, faça um fork do repositório e envie um pull request com suas alterações.

* * * * *

Este documento cobre a configuração inicial e a arquitetura do aplicativo Terrafarming. Para mais detalhes sobre cada microserviço e função Lambda, consulte a documentação específica em cada diretório correspondente.