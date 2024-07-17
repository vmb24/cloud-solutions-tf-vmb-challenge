# cloud-solutions-tf-vmb-challenge
VMB cloud solutions codes for smart agriculture solution for challenge using Terraform, AWS ECS and other resouces with Lambda, API Gateway, CloudWatch, SNS, AI with AWS Bedrock and others resources and features this cloud.

Para arquitetar os microserviços listados, é uma prática comum utilizar uma combinação de sub-redes públicas e privadas para garantir segurança e acessibilidade adequada:

Sub-rede Pública:

Weather-service: Este serviço geralmente precisa de acesso externo para obter informações meteorológicas atualizadas.
Greenhouse-service: Pode precisar de acesso externo para integrações com sensores externos ou serviços de monitoramento remoto.

Sub-rede Privada:

Farmer-service: Contém dados sensíveis do agricultor e informações de conta que devem ser protegidas.
Soil-metrics-service: Lida com dados de métricas do solo que podem ser sensíveis e devem ser acessados apenas internamente.
Crop-health-service: Envolve informações críticas sobre a saúde das plantas que devem ser protegidas.
Equipment-health-service: Pode conter dados sobre manutenção e estado dos equipamentos agrícolas que requerem proteção.

Estrutura dos Repositórios ECR
Você deve criar um repositório ECR separado para cada microserviço. Aqui está a estrutura de nomenclatura sugerida:

farmer-service
soil-metrics-service
crop-health-service
equipment-health-service
weather-service
greenhouse-service