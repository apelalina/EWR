"""
Dieses Modul wrmöglicht die Eingabe sowie das Speichern und Laden von Daten.

pylint 2.16.2
astroid 2.14.2
Python 3.11.7 | packaged by Anaconda, Inc. 
| (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
9.71/10
"""

def read_number(question: str, data_type: type, lower_limit: float = float('-Inf'), upper_limit: float = float('Inf')) -> "data_type" :
    eingabe = input(question)
    if data_type == int:
        while True:
            try:
                eingabe = int(eingabe)
                if float(eingabe) >= float(lower_limit):
                    if float(eingabe) <= float(upper_limit):
                        break
                    else:
                        eingabe = input("Bitte geben Sie eine ganze Zahl <= " + str(upper_limit) + " ein: ")
                else:
                    eingabe = input("Bitte geben Sie eine ganze Zahl >= " + str(lower_limit) + " ein: ")
            except ValueError:
                eingabe = input("Bitte geben Sie eine ganze Zahl ein: ")

    elif data_type == float:
        while True:
            try:
                eingabe = float(eingabe)
                if eingabe >= float(lower_limit):
                    if eingabe <= float(upper_limit):
                        break
                    else:
                        eingabe = input("Bitte geben Sie eine Gleitkommazahl <= " + str(upper_limit) + " ein: ")
                else:
                    eingabe = input("Bitte geben Sie eine Gleitkommazahl >= " + str(lower_limit) + " ein: ")
            except ValueError:
                eingabe = input("Bitte geben Sie eine Gleitkommazahl ein: ")

    return eingabe


def main():
    """Hauptfunktion des Programms"""
    anfrage = "Bitte geben Sie eine ganze Zahl x mit 3 <= x <= 7 ein."
    eingabe_zahl = read_number(anfrage, float, 3.0, 7.0)
    print(eingabe_zahl)
   
if __name__ == "__main__":
    main()
