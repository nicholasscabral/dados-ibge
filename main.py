import csv
from collections import Counter

# File paths
PATH = "DADOS.txt"
SECOND_CSV = "OUTRO_DADOS_SEM_ASPAS.csv"  # Name of the second CSV


def normalize_text(text):
    """
    Converts the first letter of each word to uppercase.
    """
    return " ".join(
        word.capitalize() for word in text.strip().lower().split()
    )  # Converts the first letter to uppercase


def get_column_data(column_name):
    """
    Returns the data from a specific column, if it exists in the dataset.
    """
    if DATA_SET and column_name in DATA_SET[0]:
        return [line[column_name] for line in DATA_SET]
    else:
        return f"Column '{column_name}' not found."


def generate_csv_people_by_municipality():
    """
    Generates a CSV file with the number of people per municipality, including the 'total' column from the second CSV.
    """
    municipality_data = get_column_data("MUNICÍPIO")

    # Count how many people exist per municipality in the first dataset
    municipality_count = Counter(municipality_data)

    # Read the second CSV to get the 'total' column
    second_csv_data = read_second_csv()

    # Generate the final CSV with the desired information
    with open(
        "pessoas_por_municipio.csv", mode="w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "ID",
                "Município",
                "Total de Pessoas atendidas pelo SUS",
                "População",
                "Porcentagem da população atendida pelo SUS",
            ]
        )

        for idx, (municipality, count) in enumerate(
            municipality_count.items(), start=1
        ):
            normalized_municipality = normalize_text(
                municipality
            )  # Normalizes the municipality name
            total = second_csv_data.get(
                normalized_municipality, "N/A"
            )  # Searches for the 'total' from the second CSV
            print(normalized_municipality, total)
            print(type(count), type(total))
            ratio = 0
            if total != "N/A":
                ratio = round((count / int(total)) * 100, 2)
            else:
                ratio = "N/A"
            writer.writerow([idx, normalized_municipality, count, total, f"{ratio}%"])

    print("CSV file 'asdf.csv' generated successfully!")


def read_txt_file():
    """
    Reads a .txt file separated by commas and returns the data as a list of dictionaries.
    Each dictionary represents a row with keys as the column names.
    """
    with open(PATH, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        data = [line for line in csv_reader]

    return data


def read_second_csv():
    """
    Reads the second CSV file that contains the 'total' column by municipality.
    Returns a dictionary with the municipality as the key and the 'total' value as the value.
    """
    data = {}
    with open(SECOND_CSV, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for line in csv_reader:
            municipality = line.get("MUNICÍPIO")
            total = line.get("TOTAL")
            if municipality and total:
                normalized_municipality = normalize_text(
                    municipality
                )  # Normalizes the municipality name
                data[normalized_municipality] = (
                    total  # Adds the municipality and its total to the dictionary
                )

    return data


# Load the data from the first file
DATA_SET = read_txt_file()

if __name__ == "__main__":
    generate_csv_people_by_municipality()
