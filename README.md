# Terrafarming Application

## Visão Geral

Este repositório contém o código para os microserviços e funções Lambda do aplicativo Terrafarming, junto com a configuração da infraestrutura AWS usando Terraform. O Terrafarming é um aplicativo de agricultura inteligente que utiliza inteligência artificial para fornecer recomendações aos agricultores com base em métricas do solo e condições climáticas.

## Estrutura do Repositório

```plaintext
.
├─ services
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
├── microservices/
    ├── farmer_service/
    │   ├── app.py
    │   ├── controllers/
    │   │   ├── __init__.py
    │   │   ├── farmer_controller.py
    │   ├── models/
    │   │   ├── __init__.py
        │   ├── farmer.py
        ├── services/
        │   ├── __init__.py
        │   ├── farmer_service.py
        ├── repositories/
        │   ├── __init__.py
        │   ├── farmer_repository.py
        ├── tests/
        │   ├── __init__.py
        │   ├── test_farmer_service.py
        ├── utils/
        │   ├── __init__.py
        │   ├── responses.py
        └── requirements.txt
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
│   ├── s3/
│   │  ├── upload_to_s3/
│   │  │   ├── app/
│   │  │   │   ├── main.py
│   │  │   │   ├── requirements.txt
│   │  │   ├── Dockerfile
├─terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── modules/
│   ├── microservices/
│   │   ├── farmer-service/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
│   │   ├── soil-metrics-service/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
│   │   ├── crop-health-service/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
│   │   ├── equipment-health-service/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
│   │   ├── weather-service/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
│   │   ├── greenhouse-service/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
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

#### Estrutura do Projeto:

`
farmer_service/
├── app.py
├── controllers/
│   ├── __init__.py
│   ├── farmer_controller.py
├── models/
│   ├── __init__.py
│   ├── farmer.py
├── services/
│   ├── __init__.py
│   ├── farmer_service.py
├── repositories/
│   ├── __init__.py
│   ├── farmer_repository.py
├── tests/
│   ├── __init__.py
│   ├── test_farmer_service.py
├── utils/
│   ├── __init__.py
│   ├── responses.py
└── requirements.txt
`

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


Comunicação entre serviços
--------------------------

### Comunicações e Fluxo de Eventos

Para um sistema que utiliza microserviços e funções Lambda com EventBridge, a comunicação entre os serviços pode ser visualizada como um fluxo de eventos. Cada serviço publica eventos ao realizar certas ações, e outros serviços ou funções Lambda podem ser configurados para escutar esses eventos e reagir a eles.


#### 1\. Farmer Service

-   **Publica**: `FarmerUpdate`
-   **Consumidores**:
    -   **Soil Metrics Service**: Pode escutar atualizações de informações do agricultor para ajustar as métricas de solo associadas.
    -   **Weather Service**: Pode escutar atualizações de informações do agricultor para fornecer previsões de clima mais precisas baseadas na localização.

#### 2\. Soil Metrics Service

-   **Publica**: `SoilMetricsUpdate`
-   **Consumidores**:
    -   **Crop Health Service**: Pode usar as atualizações das métricas do solo para ajustar as recomendações de saúde das plantações.
    -   **Equipment Health Service**: Pode ajustar a manutenção dos equipamentos baseada nas condições do solo.

#### 3\. Crop Health Service

-   **Publica**: `CropHealthUpdate`
-   **Consumidores**:
    -   **Farmer Service**: Pode notificar os agricultores sobre o estado atual das plantações e recomendações.
    -   **Greenhouse Service**: Pode ajustar as condições da estufa para otimizar a saúde das plantas.

#### 4\. Equipment Health Service

-   **Publica**: `EquipmentHealthUpdate`
-   **Consumidores**:
    -   **Farmer Service**: Pode notificar os agricultores sobre o estado atual dos equipamentos e recomendações de manutenção.
    -   **Soil Metrics Service**: Pode ajustar as métricas do solo considerando o desempenho dos equipamentos.

#### 5\. Weather Service

-   **Publica**: `WeatherUpdate`
-   **Consumidores**:
    -   **Weather Recommendation Lambda**: Pode gerar recomendações baseadas nas previsões do clima.
    -   **Crop Health Service**: Pode ajustar as recomendações de saúde das plantações considerando as previsões climáticas.

#### 6\. Greenhouse Service

-   **Publica**: `GreenhouseUpdate`
-   **Consumidores**:
    -   **Farmer Service**: Pode notificar os agricultores sobre as condições atuais da estufa e recomendações.

#### 7\. Funções Lambda

-   **Image Analysis Lambda**
    -   **Publica**: `ImageAnalyzed`
    -   **Consumidores**:
        -   **Crop Health Service**: Pode ajustar as recomendações de saúde das plantações baseadas na análise de imagens.
-   **Weather Recommendation Lambda**
    -   **Publica**: `WeatherRecommendation`
    -   **Consumidores**:
        -   **Farmer Service**: Pode notificar os agricultores sobre as recomendações baseadas no clima.

### Fluxo de Comunicação

#### Exemplo de Fluxo de Comunicação

1.  **Farmer Service** atualiza as informações do agricultor e publica um evento `FarmerUpdate`.
2.  **Soil Metrics Service** e **Weather Service** escutam o evento `FarmerUpdate` e atualizam suas próprias informações.
3.  **Soil Metrics Service** publica um evento `SoilMetricsUpdate`.
4.  **Crop Health Service** escuta o evento `SoilMetricsUpdate` e ajusta suas recomendações de saúde das plantações, publicando um evento `CropHealthUpdate`.
5.  **Farmer Service** escuta o evento `CropHealthUpdate` e notifica o agricultor sobre as novas recomendações.
6.  **Weather Service** publica um evento `WeatherUpdate`.
7.  **Weather Recommendation Lambda** escuta o evento `WeatherUpdate`, processa as informações e publica um evento `WeatherRecommendation`.
8.  **Farmer Service** escuta o evento `WeatherRecommendation` e notifica o agricultor sobre as novas recomendações baseadas no clima.


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


Armazenamento de imagens e outros objetos
-----------------------------------------

### Estrutura de Arquivos para S3

O Amazon S3 (Simple Storage Service) é um serviço de armazenamento em nuvem da AWS que permite armazenar e recuperar qualquer quantidade de dados a qualquer momento. Na infraestrutura que estamos desenvolvendo, o S3 será usado para armazenar imagens e dados brutos que precisam ser processados pelas funções Lambda e pelos microserviços.

#### 1\. Nome do Bucket: `terrafarming-metrics-data-storage`

#### 2\. Diretórios e Arquivos

`terrafarming-metrics-data-storage/
├── farmer_data/
│   ├── {farmer_id}/
│   │   ├── profile/
│   │   │   ├── profile_image.jpg
│   │   ├── soil_metrics/
│   │   │   ├── metrics_{timestamp}.json
│   │   ├── crop_health/
│   │   │   ├── image_{timestamp}.jpg
│   │   │   ├── analysis_{timestamp}.json
│   │   ├── equipment_health/
│   │   │   ├── image_{timestamp}.jpg
│   │   │   ├── analysis_{timestamp}.json
│   │   ├── greenhouse/
│   │   │   ├── metrics_{timestamp}.json
│   │   ├── weather/
│   │   │   ├── forecast_{timestamp}.json
│   │   │   ├── recommendation_{timestamp}.json
├── logs/
│   ├── {service_name}/
│   │   ├── log_{timestamp}.txt`


# Estrutura de configuração do S3 usando Terraform

## Visão geral

Esse diretório contém arquivos de configuração do Terraform e um script Python para gerenciar um bucket S3 usado em nosso aplicativo. O bucket S3 é usado principalmente para armazenar imagens e dados brutos que serão processados por funções Lambda e microsserviços.

## Estrutura do diretório

```plaintext
├─ services
│  ├── s3/
│  │  ├── upload_to_s3/
│  │  │   ├── app/
│  │  │   │   ├── main.py
│  │  │   │   ├── requirements.txt
│  │  │   ├── Dockerfile
terraform/
├── modules/
│   ├── ...
│   ├── storage
│   │   ├── outputs.tf
│   │   ├── S3_images_storage.tf
│   │   ├── variables.tf
└── README.md
```

Estrutura do banco de dados
------------------------------------

### Estrutura das Tabelas no DynamoDB

#### 1\. **Farmer Service**

Tabela: `Farmers`

plaintext

Copiar código

`Farmers
├── FarmerID (Partition Key)
├── Name
├── Email
├── PhoneNumber
├── Address`

#### 2\. **Soil Metrics Service**

Tabela: `SoilMetrics`

plaintext

Copiar código

`SoilMetrics
├── MetricID (Partition Key)
├── FarmerID (Sort Key)
├── Date
├── pHLevel
├── MoistureLevel
├── Temperature`

#### 3\. **Crop Health Service**

Tabela: `CropHealth`

plaintext

Copiar código

`CropHealth
├── CropID (Partition Key)
├── FarmerID (Sort Key)
├── Date
├── HealthStatus
├── ImageURL
├── AnalysisResult`

#### 4\. **Equipment Health Service**

Tabela: `EquipmentHealth`

plaintext

Copiar código

`EquipmentHealth
├── EquipmentID (Partition Key)
├── FarmerID (Sort Key)
├── Date
├── HealthStatus
├── Metrics`

#### 5\. **Weather Service**

Tabela: `WeatherData`

plaintext

Copiar código

`WeatherData
├── WeatherID (Partition Key)
├── Date
├── Temperature
├── Humidity
├── Precipitation
├── FarmerID (Sort Key)`

#### 6\. **Greenhouse Service**

Tabela: `GreenhouseData`

plaintext

Copiar código

`GreenhouseData
├── GreenhouseID (Partition Key)
├── FarmerID (Sort Key)
├── Date
├── Temperature
├── Humidity
├── CO2Level`

#### 7\. **Image Analysis Lambda**

Tabela: `ImageAnalysisResults`

plaintext

Copiar código

`ImageAnalysisResults
├── AnalysisID (Partition Key)
├── ImageURL
├── AnalysisDate
├── Result`

#### 8\. **Weather Recommendation Lambda**

Tabela: `WeatherRecommendations`

plaintext

Copiar código

`WeatherRecommendations
├── RecommendationID (Partition Key)
├── FarmerID (Sort Key)
├── Date
├── Recommendation`


Importância do S3 na infraestrutura
--------------------------------------

- **Armazenamento**: O S3 fornece uma solução de armazenamento dimensionável e durável para imagens e dados que precisam ser processados pelo nosso sistema.
- **Integração**: As imagens armazenadas podem ser acessadas diretamente por funções Lambda para análise, e os resultados podem ser armazenados novamente no S3 para processamento posterior.
- **Custo-benefício**: O S3 oferece uma maneira econômica de armazenar grandes quantidades de dados com alta disponibilidade e confiabilidade.

Ao usar o S3, garantimos que nosso aplicativo possa lidar com grandes volumes de dados de forma eficiente, dando suporte aos requisitos de processamento e análise do nosso aplicativo de agricultura inteligente.


### Explicação da Importância do S3 na Infraestrutura

- **Armazenamento**: O S3 fornece uma solução escalável e durável para armazenamento de imagens e dados que precisam ser processados pelo nosso sistema.
- **Integração**: As imagens armazenadas podem ser acessadas diretamente pelas funções Lambda para análise, e os resultados podem ser armazenados de volta no S3 para processamento posterior.
- **Custo-benefício**: O S3 oferece uma maneira econômica de armazenar grandes quantidades de dados com alta disponibilidade e confiabilidade.

Usando o S3, garantimos que nosso aplicativo possa lidar com grandes volumes de dados de forma eficiente, suportando os requisitos de processamento e análise do nosso aplicativo de agricultura inteligente.

### Finalidade do S3 na Infraestrutura

1.  **Armazenamento de Dados do Agricultor**:

    -   **Profile**: Imagens de perfil do agricultor.
    -   **Soil Metrics**: Arquivos JSON contendo métricas de solo coletadas em diferentes momentos.
    -   **Crop Health**: Imagens e análises das safras para verificar saúde e doenças.
    -   **Equipment Health**: Imagens e análises da saúde dos equipamentos agrícolas.
    -   **Greenhouse**: Métricas de estufas coletadas periodicamente.
    -   **Weather**: Previsões do tempo e recomendações baseadas nas condições meteorológicas.
2.  **Logs**:

    -   **Logs de Serviços**: Arquivos de log gerados por diferentes serviços para monitoramento e debugging.

### Utilização do S3 na Infraestrutura

1.  **Armazenamento de Imagens e Métricas**:

    -   As funções Lambda, como `ImageAnalyzed` e `WeatherRecommendation`, podem fazer upload de imagens e arquivos de métricas para o S3 após a análise.
2.  **Integração com Outros Serviços**:

    -   Os microserviços podem acessar os arquivos no S3 para processamento adicional ou para fornecer dados necessários para a tomada de decisões.
3.  **Monitoramento e Logging**:

    -   Logs gerados por serviços e funções Lambda são armazenados no S3, permitindo fácil acesso e análise.

### Exemplo de Código para Upload no S3 (Python)

`
import boto3
import os

s3_client = boto3.client('s3')

def upload_to_s3(file_path, bucket_name, s3_key):
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"File {file_path} uploaded to {bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading file to S3: {str(e)}")

file_path = "path/to/your/file.jpg"
bucket_name = "terrafarming-metrics-data-storage"
s3_key = "farmer_data/12345/crop_health/image_20240705.jpg"

upload_to_s3(file_path, bucket_name, s3_key)
`

Script Python
-------------

-   **upload_images.py**: Um script Python que faz upload de imagens de um diretório local para o bucket do S3.

Usage
-----

### Configuração do bucket S3

1.  **Inicializar o Terraform**: Navegue até o diretório `terraform/` e execute:

    sh

    Copiar código

    `terraform init`

2.  **Aplicar a configuração do Terraform**: Aplique a configuração para criar o bucket S3:

    sh

    Copiar código

    `terraform apply`

### Uploading Images to S3

1.  **Instalar o Boto3**: Certifique-se de que você tenha o Boto3 instalado em seu ambiente Python:

    sh

    Copiar código

    `pip install boto3`

2.  **Execute o script de upload**: Execute o script `upload_images.py` para fazer upload de imagens para o bucket do S3:

    sh

    Copiar código

    `python upload_images.py`

Esta estrutura facilita o gerenciamento de dados e a integração entre diferentes componentes da aplicação, garantindo que todas as informações necessárias estejam centralizadas e acessíveis de forma eficiente.


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