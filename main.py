import csv
from collections import Counter

PATH = "DADOS.txt"
SECOND_CSV = "censo.csv"    
THIRD_CSV = "pib.csv"       
RISK_CSV = "risco.csv"     

def normalize_text(text):
    if isinstance(text, str):
        return " ".join(word.capitalize() for word in text.strip().lower().split())
    return text


def get_column_data(column_name):
    if DATA_SET and column_name in DATA_SET[0]:
        return [line[column_name] for line in DATA_SET]
    else:
        return f"Column '{column_name}' not found."


def generate_csv_people_by_municipality():
    municipality_data = get_column_data("MUNICÍPIO")

    municipality_count = Counter(municipality_data)

    second_csv_data = read_second_csv()
    third_csv_data = read_third_csv()
    risk_csv_data = read_risk_csv()

    with open(
        "pessoas_por_municipio_com_pib.csv", mode="w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "ID",
                "Município",
                "Total de Pessoas atendidas pelo SUS",
                "População",
                "Porcentagem da população atendida pelo SUS",
                "PIB", 
                "População exposta ao risco",  
            ]
        )

        for idx, (municipality, count) in enumerate(
            municipality_count.items(), start=1
        ):
            normalized_municipality = normalize_text(municipality)
            total = second_csv_data.get(normalized_municipality, "N/A")
            pib = third_csv_data.get(normalized_municipality, "N/A")
            population_at_risk = risk_csv_data.get(normalized_municipality, "N/A")

            # Replace 99999999999993 with 0 in the population exposed to risk
            if population_at_risk == "99999999999993":
                population_at_risk = "0"

            ratio = 0
            if total != "N/A" and total != 0:
                ratio = round((count / int(total)) * 100, 2)
            else:
                ratio = "N/A"
            
            writer.writerow([idx, normalized_municipality, count, total, f"{ratio}%", pib, population_at_risk, sanitation])

    print("CSV file 'pessoas_por_municipio_pib_risco_sanitario.csv' generated successfully with risk and sanitation data!")


def read_txt_file():
    with open(PATH, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        data = [line for line in csv_reader]

    return data


def read_second_csv():
    data = {}
    with open(SECOND_CSV, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for line in csv_reader:
            municipality = line.get("MUNICÍPIO")
            total = line.get("TOTAL")
            if municipality and total:
                normalized_municipality = normalize_text(municipality)
                data[normalized_municipality] = total

    return data


def read_third_csv():
    data = {}
    with open(THIRD_CSV, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for line in csv_reader:
            municipality = line.get("MUNICÍPIO")
            pib = line.get("PIB")
            if municipality and pib:
                normalized_municipality = normalize_text(municipality)
                data[normalized_municipality] = pib

    return data


def read_risk_csv():
    data = {}
    with open(RISK_CSV, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for line in csv_reader:
            municipality = line.get("Local") 
            population_at_risk = line.get(" \"População exposta ao risco\"")
            if municipality and population_at_risk:
                normalized_municipality = normalize_text(municipality)
                data[normalized_municipality] = population_at_risk

    return data


# Load the data from the first file
DATA_SET = read_txt_file()

if __name__ == "__main__":
    generate_csv_people_by_municipality()
