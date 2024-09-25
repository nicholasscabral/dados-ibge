import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure seaborn for better aesthetics
sns.set(style="whitegrid")

# Read the CSV file
data = pd.read_csv("planilha_incrementada.csv")

# Removing the '%' symbol and converting the column to numeric
data["Porcentagem da população atendida pelo SUS"] = data["Porcentagem da população atendida pelo SUS"].str.replace('%', '').astype(float)

# Ensure the 'Porcentagem da população atendida pelo SUS' is in numeric format
data["Porcentagem da população atendida pelo SUS"] = pd.to_numeric(
    data["Porcentagem da população atendida pelo SUS"], errors="coerce"
)

# Drop rows with NaN values in the percentage column
data.dropna(subset=["Porcentagem da população atendida pelo SUS"], inplace=True)

# Sort the data by 'Porcentagem da população atendida pelo SUS'
data_sorted = data.sort_values(by="Porcentagem da população atendida pelo SUS")

# Descriptive statistics
# Select the last column and apply descriptive statistics
last_column_stats = data["Porcentagem da população atendida pelo SUS"].describe()
# Drop the 'count' entry
last_column_stats = last_column_stats.drop("count")
# Display the result
print(last_column_stats)

# Boxplot for standart deviation
# Select the column of interest
column_data = data["Porcentagem da população atendida pelo SUS"]

# Generate a box plot to visualize the standard deviation along with other distribution aspects
plt.figure(figsize=(8, 6))

# Creating the box plot for the selected column
plt.boxplot(column_data, vert=False, patch_artist=True, 
            boxprops=dict(facecolor='lightblue', color='blue'), 
            whiskerprops=dict(color='blue'), 
            capprops=dict(color='blue'), 
            medianprops=dict(color='red'))

# Adding titles and labels
plt.title("Box Plot for 'Porcentagem da população atendida pelo SUS'")
plt.xlabel("Percentage of Population Served by SUS")

# Display the plot
plt.tight_layout()
plt.show()

# Calculate the mean, median, mode, and standard deviation
mean = column_data.mean()
median = column_data.median()
mode = column_data.mode()[0]  # Mode could have multiple values; we take the first
std_dev = column_data.std()

# Plotting the data points
plt.figure(figsize=(10, 6))
plt.scatter(range(len(column_data)), column_data, color='blue', label='Data Points', zorder=3)

# Adding lines for mean, median, mode, and standard deviation range
plt.axhline(mean, color='red', linestyle='--', label=f'Mean: {mean:.2f}', zorder=1)
plt.axhline(median, color='green', linestyle='-.', label=f'Median: {median:.2f}', zorder=1)
plt.axhline(mode, color='orange', linestyle=':', label=f'Mode: {mode:.2f}', zorder=1)
plt.axhline(mean + std_dev, color='purple', linestyle=':', label=f'Mean + Std Dev: {mean + std_dev:.2f}', zorder=1)
plt.axhline(mean - std_dev, color='purple', linestyle=':', label=f'Mean - Std Dev: {mean - std_dev:.2f}', zorder=1)

# Add titles and labels
plt.title("Graph with Data Points, Mean, Mode, Median, and Standard Deviation")
plt.xlabel("Index of Data Points")
plt.ylabel("Porcentagem da população atendida pelo SUS (%)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5, zorder=0)

# Show the plot
plt.tight_layout()
plt.show()

'''
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
'''