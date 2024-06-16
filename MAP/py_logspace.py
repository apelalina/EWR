"""
Dieses Programm implementiert die Funktion py_logspace,
die eine Liste von ganzen Zahlen auf einer logarithmischen Skala generiert.

pylint 2.16.2
astroid 2.14.2
Python 3.11.7 | packaged by Anaconda, Inc. 
| (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
9.71/10
"""

import numpy
import matplotlib.pyplot as plt

def py_logspace(start: int, stop: int, num=2, basis=10):

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
    start = input("Start: ")
    while True:
        try:
            start = int(start)
            break
        except ValueError:
            start = input("Bitte geben Sie eine ganze Zahl ein. Start: ")
    
    stop = input("Stop: ")
    while True:
        try:
            stop = int(stop)
            break
        except ValueError:
            stop = input("Bitte geben Sie eine ganze Zahl ein. Stop: ")

    num = input("Num: ")
    while True:
        try:
            num = int(num)
            if num >= 2:
                break
            else:
                num = input("Bitte geben Sie eine Zahl >= 2 ein. Num: ")
        except ValueError:
            num = input("Bitte geben Sie eine ganze Zahl ein. Num: ")
    
    basis = input("Basis: ")
    while True:
        try:
            basis = int(basis)
            break
        except ValueError:
            basis = input("Bitte geben Sie eine ganze Zahl ein. Basis: ")

    try:
        ergebnis = py_logspace(start, stop, num, basis) # Funktionsaufruf
    except ValueError:
        print("Funktionsaufruf gescheitert. Bitte neu aufrufen.")
        

    # Vergleich mit numpy.logspace
    print("py_logspace(): ", ergebnis)
    print("numpy.logspace(): ", numpy.logspace(start, stop, num, base = basis, dtype=numpy.int32))

    # Plot
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