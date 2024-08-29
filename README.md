# tech4parking Application

# Visão Geral\
O TerraFarming é um sistema de agricultura inteligente que utiliza IoT, análise de dados e inteligência artificial para otimizar as práticas agrícolas. O sistema coleta dados de sensores de umidade do solo, processa imagens e vídeos armazenados, e fornece recomendações personalizadas para os agricultores através de uma aplicação web moderna.

Este repositório contém o código para os microserviços e funções Lambda do aplicativo tech4parking, junto com a configuração da infraestrutura AWS usando Terraform. O tech4parking é um aplicativo de agricultura inteligente que utiliza inteligência artificial para fornecer recomendações aos agricultores com base em métricas do solo e condições climáticas.

Componentes Principais

1.  AWS IoT Core
2.  Amazon S3
3.  AWS Lambda
4.  Amazon DynamoDB
5.  Amazon Bedrock
6.  Amazon CloudWatch
7.  Amazon ECS (Elastic Container Service)
8.  Amazon ECR (Elastic Container Registry)
9.  Elastic Load Balancing
10. Amazon Route 53
11. AWS Certificate Manager (ACM)
12. AWS Polly
13. API Gateway

Detalhamento dos Componentes

1.  AWS IoT Core

-   Gerencia a conexão dos sensores de umidade do solo
-   Configurado para receber leituras de umidade em intervalos específicos:
    -   Coleta 10 leituras de umidade consecutivas
    -   Calcula a média dessas 10 leituras
    -   Envia a média para processamento
    -   Aguarda por duas horas antes de iniciar o próximo ciclo de leituras (se configurado assim pelo agricultor)

Regras do IoT Core:

-   UmidadeMediaRule
    -   Trigger: Recebimento da média de umidade após 10 leituras
    -   Ação: Encaminha os dados para processamento via Lambda
-   ConfiguracaoLeituraRule
    -   Permite que o agricultor configure o intervalo entre os ciclos de leitura (padrão de 2 horas)

1.  Amazon S3

-   Bucket para armazenamento de imagens e vídeos capturados no campo
-   Bucket separado para armazenamento de dados processados e resultados de análises

1.  AWS Lambda Functions

-   moisture_lambda
    -   Trigger: IoT Core (UmidadeMediaRule)
    -   Função: Processa os dados de umidade e atualiza o DynamoDB
    -   Integrações: DynamoDB, Bedrock (para recomendações)
-   task_planning_lambda
    -   Trigger: CloudWatch Events (agendado)
    -   Função: Gera planos de tarefas baseados nos dados de umidade e recomendações
    -   Integrações: DynamoDB, Bedrock
-   generate_accessible_content
    -   Trigger: DynamoDB Streams (MoistureAverages)
    -   Função: Funcionalidades como transcrição de texto em fala para pessoas com deficiencia, dentre outras.
    -   Integrações: SNS
-   image_generation_lambda
    -   Trigger: Diversos eventos (novos dados no DynamoDB, solicitações da aplicação web, etc.)
    -   Função: Gera imagens personalizadas baseadas nos dados agrícolas
    -   Integrações: DynamoDB (para leitura de dados), S3 (para armazenamento das imagens geradas)
-   video_processing_lambda
    -   Trigger: S3 (quando novos vídeos são carregados)
    -   Função: Processa vídeos armazenados no S3 e atualiza o DynamoDB
    -   Integrações: DynamoDB, Bedrock (para análise de vídeo)

1.  Amazon DynamoDB

-   MoistureHistory: Armazena histórico de leituras de umidade
-   MoistureAverages: Armazena médias de umidade calculadas
-   TaskPlans: Armazena planos de tarefas gerados
-   ImageAnalysis: Armazena resultados de análises de imagens
-   Videos: Armazena metadados e URLs de vídeos processados

1.  Amazon Bedrock\
    O Amazon Bedrock é utilizado para análises avançadas e geração de recomendações personalizadas. Três modelos são empregados:

-   Claude
    -   Uso: Geração de recomendações detalhadas e análise de texto complexo
    -   Aplicações: Elaboração de planos de tarefas, interpretação de dados de sensores
-   Jurassic Mid
    -   Uso: Processamento de linguagem natural e geração de texto
    -   Aplicações: Criação de resumos de dados, geração de alertas contextualizados
-   Stable Diffusion
    -   Uso: Análise e geração de imagens
    -   Aplicações: Processamento de imagens do campo, detecção de problemas nas plantações

1.  Amazon CloudWatch

-   Monitoramento de todos os componentes do sistema
-   Configuração de alarmes para condições críticas

1.  Amazon ECS (Elastic Container Service)

-   Hospeda a aplicação web do TerraFarming
-   Gerencia os containers Docker da aplicação
-   Configurado com auto-scaling para lidar com variações de carga

1.  Amazon ECR (Elastic Container Registry)

-   Armazena as imagens Docker da aplicação web

1.  Elastic Load Balancing

-   Distribui o tráfego entre os containers da aplicação web
-   Garante alta disponibilidade e escalabilidade

1.  Amazon Route 53

-   Gerencia o DNS para o domínio da aplicação web

1.  AWS Certificate Manager (ACM)

-   Fornece e gerencia o certificado SSL/TLS para a aplicação web

1.  Geração de Imagens com AWS Lambda\
    Em vez de usar um serviço externo para análise de imagens, implementamos uma solução personalizada de geração de imagens usando AWS Lambda. Esta abordagem nos permite criar visualizações específicas baseadas nos dados coletados.

image_generation_lambda:

-   Trigger: Pode ser acionada por eventos diversos (novos dados no DynamoDB, solicitações da aplicação web, etc.)
-   Função: Gera imagens personalizadas baseadas nos dados agrícolas
-   Integrações: DynamoDB (para leitura de dados), S3 (para armazenamento das imagens geradas)

A função utiliza bibliotecas Python como Pillow ou Matplotlib para criar visualizações como:

-   Mapas de calor de umidade do solo
-   Gráficos de crescimento das plantas
-   Visualizações de distribuição de nutrientes

Arquitetura do Sistema

json

Copiar

```
[IoT Devices] --> [IoT Core] --> [Lambda Functions] --> [DynamoDB]
                                       |
                                       v
[S3 (Raw Data)] --> [Lambda] --> [image_generation_lambda] --> [S3 (Generated Images)]
[S3 (Videos)] --> [Lambda Functions] --> [Bedrock] --> [DynamoDB]
                                |
                                |
                                v
                        [ECS (Web App)] <----> [Lambda Functions]
                             |
                             v
              [Load Balancer] <---> [Route 53]
                                         |
                                         v
                                   [ACM Certificate]

```

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

    `git clone https://github.com/seu-usuario/tech4parking.git
    cd tech4parking`

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

Contribuições
-------------

Contribuições são bem-vindas! Por favor, faça um fork do repositório e envie um pull request com suas alterações.

* * * * *
