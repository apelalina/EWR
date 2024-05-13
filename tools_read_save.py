"""
Dieses Modul wrmöglicht die Eingabe sowie das Speichern und Laden von Daten.

pylint 2.16.2
astroid 2.14.2
Python 3.11.7 | packaged by Anaconda, Inc. 
| (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
9.71/10
"""
import numpy as np # zum einlesen und speichern von Daten

def read_number(question: str,
                data_type: type,
                lower_limit: float = float('-Inf'),
                upper_limit: float = float('Inf')) -> "data_type" :

    eingabe = input(question) # interaktive Eingabe

    while True: # Schleife, die erst verlassen wird, wenn alle Tests bestanden wurden
        try: # Funktioniert das Casting zum gewuenschten Datentyp?
            eingabe = data_type(eingabe)
            # ist die eingegebene Zahl >= der angegebenen unteren Grenze?
            if eingabe >= data_type(lower_limit):
                # ist die eingegebene Zahl <= der angegebenen oberen Grenze?
                if eingabe <= data_type(upper_limit):
                    break # Schleife wird verlassen, damit eingabe zurückgegeben werden kann
                eingabe = input("Bitte geben Sie eine Zahl <= " + str(upper_limit) + " ein: ")
            else: # neue Eingabe ermoeglichen
                eingabe = input("Bitte geben Sie eine Zahl >= " + str(lower_limit) + " ein: ")
        except ValueError: # neue Eingabe ermoeglichen
            eingabe = input("Bitte geben Sie eine Zahl vom Typ " + str(data_type) + " ein: ")

    return eingabe # Die Funktion gibt den eingelesenen Wert zurück

def save_data(data, filepath: str):
    np.savetxt(filepath, data, delimiter=',')

def load_data(filepath: str):
    npliste = np.loadtxt(filepath, delimiter=',', dtype=float)
    return npliste.tolist()

def main():
    """Hauptfunktion des Programms"""
    anfrage = "Bitte geben Sie eine ganze Zahl x mit 3 <= x <= 7 ein."
    eingabe_zahl = read_number(anfrage, float, 3.0, 7.0)
    print(eingabe_zahl)

    liste = [1.1117634238476,1,2,3,4,5,6,7,8,9]
    save_data(liste, "test.csv")

    print(liste)
    print(load_data("test.csv"))

if __name__ == "__main__":
    main()
