"""
Dieses Modul ermöglicht die Eingabe sowie das Speichern und Laden von Daten.

pylint 3.1.0
astroid 3.1.0
Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)]
9.63/10
"""
import numpy as np # zum einlesen und speichern von Daten

def read_number(question: str,
                data_type: type,
                lower_limit: float = float('-Inf'),
                upper_limit: float = float('Inf')) -> "data_type" :
    """
    Generiert eine Liste von ganzen Zahlen auf einer logarithmischen Skala.
    Durch eine leere Eingabe kann das Programm abgebrochen werden.

    Inputs:
        question (str): Aufforderung zur Eingabe
        data_type (type): Gewuenschter Datentyp
        lower_limit: Untere Grenze
        upper_limit: Obere Grenze

    Returns:
        Die eingegebene Zahl im gewuenschten Datentyp
   
    Throws:
        ValueError: wenn eine leere Eingabe gemacht wird.
    """

    eingabe = input(question) # interaktive Eingabe

    while True: # Schleife, die erst verlassen wird, wenn alle Tests bestanden wurden

        if eingabe == "":
            raise ValueError("Keine Eingabe. Programmabbruch.")

        try: # Funktioniert das Casting zum gewuenschten Datentyp?
            eingabe = data_type(eingabe)
            # ist die eingegebene Zahl >= der angegebenen unteren Grenze?
            if eingabe >= lower_limit:
                # ist die eingegebene Zahl <= der angegebenen oberen Grenze?
                if eingabe <= upper_limit:
                    break # Schleife wird verlassen, damit eingabe zurückgegeben werden kann
                eingabe = input("Bitte geben Sie eine Zahl <= " + str(upper_limit) + " ein: ")
            else: # neue Eingabe ermoeglichen
                eingabe = input("Bitte geben Sie eine Zahl >= " + str(lower_limit) + " ein: ")
        except ValueError: # neue Eingabe ermoeglichen
            eingabe = input("Bitte geben Sie eine Zahl vom Typ " + str(data_type) + " ein: ")

    return eingabe # Die Funktion gibt den eingelesenen Wert zurück

def save_data(data, filepath: str):
    """
    Speichert eine Liste von Zahlen in eine csv-Datei mit "," als Trennzeichen.
    Inputs:
        data: Eine Liste an Zahlen
        filepath (string): Pfad der zu speichernden Datei
    Throws:
        RuntimeError: Wenn das Speichern fehlschlägt.
    """
    try:
        np.savetxt(filepath, data, delimiter=',') # delimiter: "," als Trennzeichen
        print(str(filepath) + " erfolgreich gespeichert.")
    except:
        raise RuntimeError("Speichern der Datei fehlgeschlagen.")

def load_data(filepath: str):
    """
    Liest eine Liste von Zahlen aus einer csv-Datei mit "," als Trennzeichen ein.
    Inputs:
        filepath (string): Pfad der zu lesenden Datei
    Throws:
        RuntimeError: Wenn das Einlesen fehlschlägt.
    """
    try:
        npliste = np.loadtxt(filepath, delimiter=',', dtype=float) # delimiter: "," als Trennzeichen
        print(str(filepath) + " erfolgreich eingelesen.")
        return npliste.tolist() # kein numpy-Array, sondern eine Liste zurückgeben
    except:
        raise RuntimeError("Einlesen der Datei fehlgeschlagen.")

def main():
    """Anwednungsbeispiele"""
    # read_number()
    print("Zunächst wird die Funktion load_data() getestet.")
    print("Eine leere Eingabe ermöglicht den Abbruch und führt zum Test der nächsten Funktion.")

    anfrage = "Bitte geben Sie eine ganze Zahl x mit 3 <= x <= 7 ein."
    try: # Falls der Aufruf abgebrochen wird, soll das main-Programm trotzdem weiter laufen
        eingabe_zahl = read_number(anfrage, int, lower_limit=2)
        print("")
        print("Die Funktion gibt zurück: " + str(eingabe_zahl) + ", Datentyp: " +
              str(type(eingabe_zahl)))
    except ValueError:
        print("Abbruch des Tests.")
        exit()

    # read_number()
    print("")
    print("Nun wird eine Beispielliste erstellt und exportiert: [1.1117634, 2.55, 3.3, 144.0]")
    liste = [1.1117634, 2.55, 3.3, 144.0] # eine Beispielliste
    try:
        save_data(liste, "test.csv")
    except RuntimeError:
        print("Speichern der Liste fehlgeschlagen.")

    # read_number()
    print("")
    print("Dieselbe Liste wird nun wieder eingelesen und ausgegeben.")
    try:
        print(load_data("test.csv"))
    except RuntimeError:
        print("Einlesen der Datei fehlgeschlagen.")

if __name__ == "__main__":
    main()
