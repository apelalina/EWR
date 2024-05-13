"""
Dieses Modul wrmöglicht die Eingabe sowie das Speichern und Laden von Daten.

pylint 2.16.2
astroid 2.14.2
Python 3.11.7 | packaged by Anaconda, Inc. 
| (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
9.71/10
"""

def read_number(question: str, data_type: type, lower_limit: float = float('-Inf'), upper_limit: float = float('Inf')) -> "data_type" :
    
    eingabe = input(question) # interaktive Eingabe
    
    while True: # Schleife, die unendlich läuft und erst verlassen wird, wenn alle Tests bestanden wurden
        try: # Funktioniert das Casting zum gewuenschten Datentyp?
            eingabe = data_type(eingabe)
            if eingabe >= data_type(lower_limit): # ist die eingegebene Zahl >= der angegebenen unteren Grenze?
                if eingabe <= data_type(upper_limit): # ist die eingegebene Zahl <= der angegebenen oberen Grenze?
                    break # Schleife wird verlassen, damit eingabe zurückgegeben werden kann
                else:
                    eingabe = input("Bitte geben Sie eine Zahl <= " + str(upper_limit) + " ein: ") # neue Eingabe ermöglichen
            else:
                eingabe = input("Bitte geben Sie eine Zahl >= " + str(lower_limit) + " ein: ") # neue Eingabe ermöglichen
        except ValueError:
            eingabe = input("Bitte geben Sie eine Zahl vom Typ " + str(data_type) + " ein: ") # neue Eingabe ermöglichen
    
    return eingabe # Die Funktion gibt den eingelesenen Wert zurück


def main():
    """Hauptfunktion des Programms"""
    anfrage = "Bitte geben Sie eine ganze Zahl x mit 3 <= x <= 7 ein."
    eingabe_zahl = read_number(anfrage, float, 3.0, 7.0)
    print(eingabe_zahl)
   
if __name__ == "__main__":
    main()
