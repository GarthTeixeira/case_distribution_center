# exemplo simplificado
import pandas as pd

# Dados fictícios
estados = ["PE", "PB", "CE", "RN", "AL", "BA", "SE", "PI"]
populacao_milhoes = [9.56, 4.16, 9.26, 3.45, 3.22, 14.87, 2.3, 3.38]
renda_per_capita = [1113, 1320, 1116, 1373, 1110, 1139, 1218, 1242]

df = pd.DataFrame({
    "Estado": estados,
    "Populacao_milhoes": populacao_milhoes,
    "Renda_per_capita": renda_per_capita
})

# Potencial de consumo = População × Renda
df["Potencial"] = df["Populacao_milhoes"] * df["Renda_per_capita"]

# Definir cobertura aproximada de cada CD
cd_recife_estados = ["PE", "PB", "CE", "RN", "AL", "PI"]
cd_salvador_estados = ["BA", "SE", "AL", "PB", "PI"]

potencial_recife = df[df["Estado"].isin(cd_recife_estados)]["Potencial"].sum()
potencial_salvador = df[df["Estado"].isin(cd_salvador_estados)]["Potencial"].sum()

print(f"Potencial de consumo atendido por CD em Recife: {potencial_recife:,.0f}")
print(f"Potencial de consumo atendido por CD em Salvador: {potencial_salvador:,.0f}")
