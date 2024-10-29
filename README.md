# TerraFarming Application

# Visão Geral
O TerraFarming é um sistema de agricultura inteligente que utiliza IoT, análise de dados e inteligência artificial para otimizar as práticas agrícolas. O sistema coleta dados de sensores de umidade do solo, processa imagens e vídeos armazenados, e fornece recomendações personalizadas para os agricultores através de uma aplicação web moderna.

Este repositório contém o código para os microserviços e funções Lambda do aplicativo TerraFarming, junto com a configuração da infraestrutura AWS usando Terraform. O TerraFarming é um aplicativo de agricultura inteligente que utiliza inteligência artificial para fornecer recomendações aos agricultores com base em métricas do solo e condições climáticas.

- **Alguns Recursos ainda serão implementados no futuro** 

Componentes Principais

1.  AWS Lambda
    -   Função: Executa código serverless para as funções de fulfillment e lógica de negócios.
    -   Uso no TerraFarming: Processa solicitações dos usuários, realiza cálculos e interage com outros serviços AWS.

2.  Amazon API Gateway
    -   Função: Gerencia e roteia as requisições da API.
    -   Uso no TerraFarming: Direciona as solicitações dos usuários para os serviços apropriados.

3.  Amazon DynamoDB
    -   Função: Banco de dados NoSQL altamente escalável.
    -   Uso no TerraFarming: Armazena dados não-relacionais, como informações de sensores e perfis de usuários.

4.  Amazon Lex
    -   Função: Serviço de processamento de linguagem natural e chatbot.
    -   Uso no TerraFarming: Processa entradas de texto e voz dos usuários, identifica intenções e extrai informações relevantes.

5.  Amazon SageMaker
    -   Função: Plataforma de aprendizado de máquina.
    -   Uso no TerraFarming: Treina e implanta modelos de ML para previsões agrícolas, análise de imagens e recomendações personalizadas.

6.  AWS Rekognition
    -   Função: Serviço de análise de imagens e vídeos.
    -   Uso no TerraFarming: Analisa imagens de culturas para detecção de doenças, pragas e estágio de crescimento.

7.  AWS IoT Core
    -   Função: Plataforma para conectar e gerenciar dispositivos IoT.
    -   Uso no TerraFarming: Gerencia a conexão e os dados dos sensores agrícolas.

10. Amazon S3
    -   Função: Armazenamento de objetos.
    -   Uso no TerraFarming: Armazena arquivos, imagens e backups de dados.

12. Amazon SNS
    -   Função: Serviço de notificações.
    -   Uso no TerraFarming: Envia alertas e notificações push para os usuários.

13. Amazon SES
    -   Função: Serviço de e-mail.
    -   Uso no TerraFarming: Envia e-mails transacionais e relatórios aos usuários.

14. Amazon CloudFront
    -   Função: Rede de entrega de conteúdo (CDN).
    -   Uso no TerraFarming: Distribui conteúdo estático e protege contra ataques DDoS.

15. Amazon Route 53
    -   Função: Serviço de DNS e roteamento de tráfego.
    -   Uso no TerraFarming: Gerencia o DNS do aplicativo e implementa estratégias de failover.

19. Amazon Cognito
    -   Função: Serviço de autenticação e gerenciamento de identidade.
    -   Uso no TerraFarming: Gerencia a autenticação e autorização dos usuários.

20. AWS KMS
    -   Função: Serviço de gerenciamento de chaves.
    -   Uso no TerraFarming: Gerencia chaves de criptografia para proteger dados sensíveis.

21. AWS Shield e WAF
    -   Função: Serviços de segurança e firewall de aplicações web.
    -   Uso no TerraFarming: Protege contra ataques DDoS e ameaças web.

22. AWS Config
    -   Função: Serviço de avaliação, auditoria e avaliação de conformidade.
    -   Uso no TerraFarming: Monitora a conformidade da configuração dos recursos AWS.

23. AWS CloudTrail
    -   Função: Serviço de auditoria e logging.
    -   Uso no TerraFarming: Registra todas as atividades da conta AWS para fins de auditoria.

28. AWS Step Functions
    -   Função: Serviço de orquestração de fluxos de trabalho.
    -   Uso no TerraFarming: Coordena a execução de múltiplos serviços AWS em workflows complexos.

29. AWS Bedrock
    -   Função: Plataforma de IA generativa que oferece acesso a múltiplos modelos de linguagem e imagem de ponta.
    -   Uso no TerraFarming: Fornece capacidades avançadas de IA para várias aplicações agrícolas.
    -   Modelos utilizados:
        A. Claude
        -   Uso: Geração de recomendações detalhadas e análise de texto complexo.
        -   Aplicações:\
            - Elaboração de planos de tarefas personalizados baseados em dados agrícolas.\
            - Interpretação avançada de dados de sensores para insights acionáveis.\
            - Geração de relatórios detalhados sobre condições da safra e previsões de produtividade.\
            - Assistente virtual para agricultores, capaz de responder perguntas complexas sobre práticas agrícolas.

        B. Jurassic Mid

        -   Uso: Processamento de linguagem natural e geração de texto eficiente.
        -   Aplicações:\
            - Criação de resumos concisos de grandes volumes de dados agrícolas.\
            - Geração de alertas contextualizados baseados em condições específicas do campo.\
            - Tradução e adaptação de informações técnicas para linguagem acessível aos agricultores.\
            - Automação de comunicações rotineiras, como atualizações de status e lembretes de tarefas.

        C. Stable Diffusion

        -   Uso: Análise sofisticada e geração de imagens relacionadas à agricultura.
        -   Aplicações:\
            - Processamento avançado de imagens do campo para identificação precoce de doenças e pragas.\
            - Detecção automatizada de problemas nas plantações, como estresse hídrico ou deficiências nutricionais.\
            - Geração de visualizações preditivas do desenvolvimento da safra baseadas em dados atuais.\
            - Criação de imagens ilustrativas para relatórios e materiais educativos sobre práticas agrícolas.
    -   Integração no TerraFarming: Estes modelos trabalham em conjunto para fornecer uma solução completa de IA para agricultura, combinando análise textual, processamento de linguagem natural e visão computacional para otimizar todas as facetas da produção agrícola.

Esta explicação expandida do AWS Bedrock destaca como cada modelo específico (Claude, Jurassic Mid e Stable Diffusion) é utilizado no contexto do TerraFarming, fornecendo exemplos concretos de suas aplicações na agricultura de precisão.

30. Amazon ECR
    -   Função: Registro de contêineres.
    -   Uso no TerraFarming: Armazena, gerencia e implanta imagens de contêineres Docker.

32. AWS Certificate Manager
    -   Função: Gerenciamento de certificados SSL/TLS.
    -   Uso no TerraFarming: Provisiona, gerencia e implanta certificados para conexões seguras.

33. Amazon QuickSight
    -   Função: Serviço de business intelligence.
    -   Uso no TerraFarming: Cria visualizações e dashboards interativos para análise de dados agrícolas.

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


* Funções lambda para geração de mídia:

1.  Umidade do Solo:
    -   Imagens de culturas ideais para o nível atual de umidade do solo.
    -   Visualizações de técnicas de irrigação recomendadas (gotejamento, aspersão, etc.).
    -   Representações de cobertura do solo adequada para reter umidade.

2.  Temperatura do Solo:
    -   Imagens de plantas que se desenvolvem bem na temperatura atual do solo.
    -   Visualizações de técnicas de manejo do solo para regular a temperatura (mulching, cobertura vegetal).
    -   Representações de sistemas de aquecimento/resfriamento do solo para estufas.

3.  Umidade do Ar:
    -   Imagens de culturas adaptadas às condições atuais de umidade do ar.
    -   Visualizações de técnicas para controle de umidade (nebulização, ventilação).
    -   Representações de estruturas de proteção contra excesso ou falta de umidade.

4.  Temperatura do Ar:
    -   Imagens de plantas resistentes à temperatura atual do ar.
    -   Visualizações de estruturas de proteção (estufas, túneis, telas de sombreamento).
    -   Representações de técnicas de plantio adequadas para a temperatura (consórcio, rotação).

5.  Luminosidade (Sol ou Estufa):
    -   Imagens de culturas que se desenvolvem bem no nível atual de luminosidade.
    -   Visualizações de técnicas de manejo de luz (sistemas de iluminação artificial, telas de sombreamento).
    -   Representações de disposições ideais de plantas para otimizar o uso da luz disponível.

Para criar GIFs informativos para agricultores sobre os tópicos mencionados, podemos descrever como eles poderiam ser representados visualmente. Vou sugerir conceitos para cada tópico:

1.  Umidade do Solo:
    Um GIF mostrando um corte transversal do solo, com partículas de água se movendo. O nível de umidade poderia variar, indicando solo seco, ideal e encharcado. Uma planta poderia ser mostrada reagindo a essas mudanças.

2.  Temperatura do Solo:
    Um termômetro inserido no solo, com a temperatura variando. As cores do solo poderiam mudar de frio (azul) para quente (vermelho). Sementes ou raízes poderiam ser mostradas reagindo às mudanças de temperatura.

3.  Umidade do Ar:
    Um higrômetro simples com o ponteiro se movendo entre "seco" e "úmido". Gotas de água poderiam aparecer no ar quando a umidade aumenta, e desaparecer quando diminui.

4.  Temperatura do Ar:
    Um termômetro ao ar livre, com a temperatura subindo e descendo. O ambiente ao redor poderia mudar (por exemplo, plantas murchando com calor extremo ou geada formando-se com frio intenso).

5.  Luminosidade (Sol ou Estufa):
    Para o sol, um ciclo dia/noite com o sol se movendo no céu. Para estufa, lâmpadas de crescimento ligando e desligando. Em ambos os casos, uma planta poderia ser mostrada crescendo em resposta à luz.

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

Arquitetura do Sistema

json

Copiar

```
[IoT Devices] --> [IoT Core] --> [Lambda Functions]
                                       |
                                       v
                             [Bedrock] --> [DynamoDB]
                                |
                                |
                                v
                            [API Gateway]
                                |
                                |
                                v
                        [ECS (Web App)] 
                             |
                             v
              [Load Balancer] <---> [Route 53]---------> Usuário (internet)
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

    `git clone https://github.com/seu-usuario/TerraFarmingparking.git
    cd TerraFarmingparking`

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
