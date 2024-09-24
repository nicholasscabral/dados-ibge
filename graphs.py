import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure seaborn for better aesthetics
sns.set(style="whitegrid")

# Read the CSV file
data = pd.read_csv("planilha_incrementada.csv")

# Ensure the 'Porcentagem da população atendida pelo SUS' is in numeric format
data["Porcentagem da população atendida pelo SUS"] = pd.to_numeric(
    data["Porcentagem da população atendida pelo SUS"], errors="coerce"
)

# Drop rows with NaN values in the percentage column
data.dropna(subset=["Porcentagem da população atendida pelo SUS"], inplace=True)

# Sort the data by 'Porcentagem da população atendida pelo SUS'
data_sorted = data.sort_values(by="Porcentagem da população atendida pelo SUS")

# Top 10 municipalities with the highest SUS attendance rates
top_10_attendance = data_sorted.nlargest(
    10, "Porcentagem da população atendida pelo SUS"
)

# Top 10 municipalities with the lowest SUS attendance rates
bottom_10_attendance = data_sorted.nsmallest(
    10, "Porcentagem da população atendida pelo SUS"
)

# Plotting the top 10 municipalities with the highest SUS attendance rates
plt.figure(figsize=(12, 6))
sns.barplot(
    x="Porcentagem da população atendida pelo SUS",
    y="Município",
    data=top_10_attendance,
    palette="Blues_d",
)
plt.title("Top 10 Municípios com Maior Taxa de Atendimento do SUS")
plt.xlabel("Porcentagem da População Atendida (%)")
plt.ylabel("Município")
plt.show()

# Plotting the top 10 municipalities with the lowest SUS attendance rates
plt.figure(figsize=(12, 6))
sns.barplot(
    x="Porcentagem da população atendida pelo SUS",
    y="Município",
    data=bottom_10_attendance,
    palette="Reds_d",
)
plt.title("Top 10 Municípios com Menor Taxa de Atendimento do SUS")
plt.xlabel("Porcentagem da População Atendida (%)")
plt.ylabel("Município")
plt.show()
