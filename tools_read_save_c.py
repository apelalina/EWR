import json

def read_number(question, data_type, lower_limit=float('-inf'), upper_limit=float('inf')):
    while True:
        try:
            user_input = data_type(input(question))
            if lower_limit <= user_input <= upper_limit:
                return user_input
            else:
                print("Die Eingabe liegt nicht im angegebenen Bereich.")
        except ValueError:
            print("Ungültige Eingabe. Bitte geben Sie eine gültige Zahl ein.")

def save_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def main():
    # Beispiel für die Verwendung der Funktionen
    print("Bitte geben Sie eine Zahl zwischen 3 und 7 ein:")
    number = read_number("Zahl eingeben: ", float, 3, 7)
    print("Eingegebene Zahl:", number)

    data_to_save = {"example_key": "example_value"}
    filename = "example_data.json"
    save_data(data_to_save, filename)
    loaded_data = load_data(filename)
    print("Gespeicherte Daten:", loaded_data)

if __name__ == "__main__":
    main()
