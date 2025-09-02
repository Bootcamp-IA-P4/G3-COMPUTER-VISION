#!/bin/bash

# Script para entrenar el modelo YOLOv8m con el dataset completo (50 epochs).
# Los resultados se guardarán en la carpeta 'training_results'.

echo "Iniciando el entrenamiento del modelo YOLOv8m con el dataset completo..."

yolo detect train \
    model=yolov8m.pt \
    data='data/datasets/curated/dataset_v1_yolov8/data.yaml' \
    epochs=50 \
    project='training_results' \
    name='yolov8m_full_dataset_50_epochs' \
    save_json=True \
    save_hybrid=True \
    plots=True

echo "Entrenamiento finalizado. Los resultados se encuentran en la carpeta training_results/yolov8m_full_dataset_50_epochs"
