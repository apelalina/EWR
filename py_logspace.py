"""
Dieses Programm implementiert die Funktion py_logspace,
die eine Liste von ganzen Zahlen auf einer logarithmischen Skala generiert.

pylint 2.16.2
astroid 2.14.2
Python 3.11.7 | packaged by Anaconda, Inc. 
| (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
10/10
"""

import numpy
import matplotlib.pyplot as plt

def py_logspace(start: int, stop: int, num: int =2, basis: int =10) -> list[int]:

    """
    Generiert eine Liste von ganzen Zahlen auf einer logarithmischen Skala.

    Inputs:
        start (int): Startpunkt des Intervalls
        stop (int): Endpunkt des Intervalls
        num (int): Anzahl der zu ermittelnden Werte (muss >= 2 sein)
        basis (int): Basis fuer logarithmische Skala

    Returns:
        list[int]: Liste von ganzen Zahlen auf einer logarithmischen Skala
   
    Throws:
        ValueError: wenn num < 2 uebergeben wird
    """

    if num < 2:
        raise ValueError("Bitte geben Sie num >= 2 an.")

    schritt = (stop - start) / (num - 1)

    # Liste
    liste = []

    # Gesamtberechnung
    for i in range(num):

        # Berechnung Exponent
        exponent = start + schritt * i

        # Berechnung Wert
        wert = basis ** exponent

        # Hinzufuegen des ganzzahligen Anteils der Zahl zur Liste
        liste.append(int(wert))

    return liste

def main():
    """Hauptfunktion des Programms"""

    # Definition der Variablen
    start = int(input("Start: "))
    stop = int(input("Stop: "))
    num = int(input("num: "))
    basis = int(input("basis: "))

    try:
        liste = py_logspace(start, stop, num, basis)
        print("py_logspace():",liste)
    except ValueError as error:
        print("Fehler:", error)
        num = int(input("Bitte geben sie num erneut ein: "))
    # Vergleich mit numpy.logspace
    print("numpy.logspace(): ", numpy.logspace(start, stop, num, basis))

    # Plot
    ergebnis = py_logspace(start, stop, num, basis) # Funktionsaufruf
    plt.plot(ergebnis, ergebnis, '-b') # Plot mit Linie
    plt.plot(ergebnis, ergebnis, 'ro', label='Zahlen im Logspace') # Punkte über der Linie
    plt.legend(loc='lower right')
    plt.yscale('log',base=basis) # logarithmische Skalierung der y-Achse
    plt.grid()
    plt.title("Darstellung der generierten Zahlen") # Beschriftungen
    plt.xlabel("Lineare Skalierung")
    ylabel= "Logarithmische Skalierung zur Basis "+str(basis)
    plt.ylabel(ylabel)
    plt.show()
   
if __name__ == "__main__":
    main()
