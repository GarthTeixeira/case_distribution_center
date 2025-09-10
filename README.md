# 📘 README – Análise de Localização de Centro de Distribuição

Este projeto contém três scripts em Python que ajudam a comparar cidades candidatas para implantação de um Centro de Distribuição (CD), considerando distâncias, custos imobiliários e potencial de consumo.

## 🚀 Scripts
### 1. Comparador de distâncias

- Usa coordenadas (latitude/longitude) para calcular distâncias entre cidades.

- Compara o total de quilômetros percorridos a partir de Recife e Salvador até capitais do Nordeste.

- Ajuda a identificar qual CD tem localização mais estratégica.


### 2. Potencial de consumo
   
- Calcula um índice simplificado de potencial de consumo por estado.

- Fórmula: População × Renda per capita.

- Define quais estados estariam sob cobertura de cada cidade candidata.

- Compara o potencial de consumo atendido por cada opção de CD.

## 🛠️ Requisitos

- Python 3.9+

- Pandas (pip install pandas)

## 📌 Observações

- Os cálculos de distância usam fórmulas geográficas simples (não incluem trânsito real).

- Estes scripts são provas de conceito para auxiliar comparações estratégicas.
