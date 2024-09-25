# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configure seaborn for better aesthetics
sns.set(style="whitegrid")

# Read the CSV file
data = pd.read_csv("pessoas_por_municipio_com_pib_risco_cleaned.csv")

# Removing the '%' symbol and converting the column to numeric
# Replace 'N/A' and any other non-numeric values with NaN
data["Porcentagem da população atendida pelo SUS"] = pd.to_numeric(
    data["Porcentagem da população atendida pelo SUS"].str.replace('%', '', regex=True), errors="coerce"
)

# Drop rows with NaN values in the percentage column
data.dropna(subset=["Porcentagem da população atendida pelo SUS"], inplace=True)

# Ensure other columns with potential 'N/A' values are cleaned as well
data["Total de Pessoas atendidas pelo SUS"] = pd.to_numeric(data["Total de Pessoas atendidas pelo SUS"], errors="coerce").fillna(0)
data["População"] = pd.to_numeric(data["População"], errors="coerce").fillna(0)
data["PIB"] = pd.to_numeric(data["PIB"], errors="coerce").fillna(0)

# Rescale PIB to thousands
data['PIB (milhares)'] = data['PIB'] / 1000  # Converting PIB to thousands

# Proceed with the remaining code
# Sort the data by 'Porcentagem da população atendida pelo SUS'
data_sorted = data.sort_values(by="Porcentagem da população atendida pelo SUS")

# Boxplot for standard deviation
column_data = data["Porcentagem da população atendida pelo SUS"]

# Generate a box plot to visualize the standard deviation along with other distribution aspects
plt.figure(figsize=(8, 6))
plt.boxplot(column_data, vert=False, patch_artist=True, 
            boxprops=dict(facecolor='lightblue', color='blue'), 
            whiskerprops=dict(color='blue'), 
            capprops=dict(color='blue'), 
            medianprops=dict(color='red'))

plt.title("Box Plot for 'Porcentagem da população atendida pelo SUS'")
plt.xlabel("Porcentagem da população atendida pelo SUS")
plt.tight_layout()
plt.savefig("./graphs_images/box_plot_population_served_by_SUS.png")
plt.show()

# Calculate the mean, median, mode, and standard deviation
mean = column_data.mean()
median = column_data.median()
mode = column_data.mode()[0]  # Mode could have multiple values; we take the first
std_dev = column_data.std()

# Plotting the data points
plt.figure(figsize=(10, 6))
plt.scatter(range(len(column_data)), column_data, color='blue', label='Dados', zorder=3)

# Adding lines for mean, median, mode, and standard deviation range
plt.axhline(mean, color='red', linestyle='--', label=f'Média: {mean:.2f}', zorder=1)
plt.axhline(median, color='green', linestyle='-.', label=f'Mediana: {median:.2f}', zorder=1)
plt.axhline(mode, color='orange', linestyle=':', label=f'Moda: {mode:.2f}', zorder=1)
plt.axhline(mean + std_dev, color='purple', linestyle=':', label=f'Média + Desvio Padrão: {mean + std_dev:.2f}', zorder=1)
plt.axhline(mean - std_dev, color='purple', linestyle=':', label=f'Média - Desvio Padrão: {mean - std_dev:.2f}', zorder=1)

plt.title("Dados e estatísticas de média, moda, mediana e desvio padrão")
plt.xlabel("ID para dados de cada município")
plt.ylabel("Porcentagem da população atendida pelo SUS (%)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5, zorder=0)
plt.tight_layout()
plt.savefig("./graphs_images/scatter_plot_population_served_by_SUS.png")
plt.show()

# Top 10 municipalities with the highest SUS attendance rates
top_10_attendance = data_sorted.nlargest(10, "Porcentagem da população atendida pelo SUS")

# Top 10 municipalities with the lowest SUS attendance rates
bottom_10_attendance = data_sorted.nsmallest(10, "Porcentagem da população atendida pelo SUS")

# Plotting the top 10 municipalities with the highest SUS attendance rates
plt.figure(figsize=(12, 6))
sns.barplot(x="Porcentagem da população atendida pelo SUS", y="Município", data=top_10_attendance, palette="Blues_d")
plt.title("Top 10 Municípios com Maior Taxa de Atendimento do SUS")
plt.xlabel("Porcentagem da População Atendida (%)")
plt.ylabel("Município")
plt.tight_layout()
plt.savefig("./graphs_images/top_10_highest_sus_attendance.png")
plt.show()

# Plotting the top 10 municipalities with the lowest SUS attendance rates
plt.figure(figsize=(12, 6))
sns.barplot(x="Porcentagem da população atendida pelo SUS", y="Município", data=bottom_10_attendance, palette="Reds_d")
plt.title("Top 10 Municípios com Menor Taxa de Atendimento do SUS")
plt.xlabel("Porcentagem da População Atendida (%)")
plt.ylabel("Município")
plt.tight_layout()
plt.savefig("./graphs_images/top_10_lowest_sus_attendance.png")
plt.show()

## CORRELATIONS

# Correlation analysis
correlation_matrix = data[['Total de Pessoas atendidas pelo SUS', 
                           'População', 
                           'Porcentagem da população atendida pelo SUS', 
                           'PIB']].corr()

# Display the correlation matrix
print("Matrix de correlação:")
print(correlation_matrix)

# Visualize the correlations using a heatmap
plt.figure(figsize=(10, 8))
plt.matshow(correlation_matrix, cmap='coolwarm', fignum=1)
plt.colorbar()
plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=90)
plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
plt.title('Mapa de calor da correlação', pad=20)
plt.show()

# Additional analysis: Correlation between PIB and Porcentagem da população atendida pelo SUS
correlation = data['PIB'].corr(data['Porcentagem da população atendida pelo SUS'])
print(f"Coeficiente de correlação entre PIB e Porcentagem da população atendida pelo SUS: {correlation}")

# Improved scatter plot with logarithmic scale for PIB vs Porcentagem da população atendida pelo SUS
plt.figure(figsize=(10, 6))
sns.scatterplot(x='PIB (milhares)', y='Porcentagem da população atendida pelo SUS', data=data)
plt.title('PIB vs. Porcentagem da população atendida pelo SUS')
plt.xlabel('PIB (milhares)')
plt.ylabel('Porcentagem da população atendida pelo SUS')

# Adding a trend line
sns.regplot(x='PIB (milhares)', y='Porcentagem da população atendida pelo SUS', data=data, scatter=False, color='red', logx=True)

plt.tight_layout()
plt.savefig("./graphs_images/scatter_plot_pib_vs_sus_attendance_percentage.png")
plt.show()

# Additional analysis: Correlation between PIB and Total de Pessoas atendidas pelo SUS
correlation = data['PIB'].corr(data['Total de Pessoas atendidas pelo SUS'])
print(f"Coeficiente de correlação entre PIB e Total de Pessoas atendidas pelo SUS: {correlation}")

# Improved scatter plot with logarithmic scale for PIB vs Porcentagem da população atendida pelo SUS
plt.figure(figsize=(10, 6))
sns.scatterplot(x='PIB (milhares)', y='Total de Pessoas atendidas pelo SUS', data=data)
plt.title('PIB vs. Total de Pessoas atendidas pelo SUS')
plt.xlabel('PIB (milhares)')
plt.ylabel('Total de Pessoas atendidas pelo SUS')

# Adding a trend line
sns.regplot(x='PIB (milhares)', y='Total de Pessoas atendidas pelo SUS', data=data, scatter=False, color='red', logx=True)

plt.tight_layout()
plt.savefig("./graphs_images/scatter_plot_pib_vs_sus_attendance_absolute.png")
plt.show()

# Top 10 municipalities with the highest PIB
top_10_pib = data.nlargest(10, "PIB")

# Top 10 municipalities with the lowest PIB
bottom_10_pib = data.nsmallest(10, "PIB")

# Plotting the top 10 municipalities with the highest PIB
plt.figure(figsize=(12, 6))
sns.barplot(x="PIB", y="Município", data=top_10_pib, palette="Greens_d")
plt.title("Top 10 Municípios com Maior PIB")
plt.xlabel("PIB")
plt.ylabel("Município")
plt.tight_layout()
plt.savefig("./graphs_images/top_10_highest_pib.png")
plt.show()

# Plotting the top 10 municipalities with the lowest PIB
plt.figure(figsize=(12, 6))
sns.barplot(x="PIB", y="Município", data=bottom_10_pib, palette="Oranges_d")
plt.title("Top 10 Municípios com Menor PIB")
plt.xlabel("PIB")
plt.ylabel("Município")
plt.tight_layout()
plt.savefig("./graphs_images/top_10_lowest_pib.png")
plt.show()

# Additional analysis: Correlation between Population at Risk and Population served by SUS
correlation_risk_sus = data['População exposta ao risco'].corr(data['Total de Pessoas atendidas pelo SUS'])
print(f"Coeficiente de correlação entre População exposta ao risco e Total de Pessoas atendidas pelo SUS: {correlation_risk_sus}")

# Scatter plot with regression line for Population at Risk vs. Population served by SUS
plt.figure(figsize=(10, 6))
sns.scatterplot(x='População exposta ao risco', y='Total de Pessoas atendidas pelo SUS', data=data)
plt.title('População exposta ao risco vs. Total de Pessoas atendidas pelo SUS')
plt.xlabel('População exposta ao risco')
plt.ylabel('Total de Pessoas atendidas pelo SUS')

# Adding a trend line
sns.regplot(x='População exposta ao risco', y='Total de Pessoas atendidas pelo SUS', data=data, scatter=False, color='red')

plt.tight_layout()
plt.savefig("./graphs_images/scatter_plot_risk_vs_sus.png")
plt.show()

# Top 10 municipalities with the highest population at risk
top_10_risk = data[data["População exposta ao risco"] > 0].nlargest(10, "População exposta ao risco")

# Top 10 municipalities with the lowest population at risk
bottom_10_risk = data[data["População exposta ao risco"] > 0].nsmallest(10, "População exposta ao risco")

# Plotting the top 10 municipalities with the highest population at risk
plt.figure(figsize=(12, 6))
sns.barplot(x="População exposta ao risco", y="Município", data=top_10_risk, palette="Reds_d")
plt.title("Top 10 Municípios com Maior População Exposta ao Risco")
plt.xlabel("População Exposta ao Risco")
plt.ylabel("Município")
plt.tight_layout()
plt.savefig("./graphs_images/top_10_highest_population_at_risk.png")
plt.show()

# Plotting the top 10 municipalities with the lowest population at risk
plt.figure(figsize=(12, 6))
sns.barplot(x="População exposta ao risco", y="Município", data=bottom_10_risk, palette="Blues_d")
plt.title("Top 10 Municípios com Menor População Exposta ao Risco")
plt.xlabel("População Exposta ao Risco")
plt.ylabel("Município")
plt.tight_layout()
plt.savefig("./graphs_images/top_10_lowest_population_at_risk.png")
plt.show()
