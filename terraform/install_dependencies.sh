#!/bin/bash

# Diretório base dos módulos
BASE_DIR="modules/services/lambdas"

# Lista de Lambdas
LAMBDAS=(
  "moisture_task_planner"
  "soil_moisture_data_processing_recommendations"
)

# Instala as dependências para cada Lambda
for lambda in "${LAMBDAS[@]}"; do
  LAMBDA_DIR="$BASE_DIR/$lambda/lambda"
  echo "Instalando dependências para $lambda"
  if [ -f "$LAMBDA_DIR/requirements.txt" ]; then
    pip install -r "$LAMBDA_DIR/requirements.txt" -t "$LAMBDA_DIR/"
  else
    echo "Arquivo requirements.txt não encontrado para $lambda"
  fi
done