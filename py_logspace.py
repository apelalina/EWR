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

def py_logspace(start: int, stop: int, num=2, basis=10):

    """
    Generiert eine Liste von ganzen Zahlen auf einer logarithmischen Skala.

    Inputs:
        start (int): Startpunkt des Intervalls
        stop (int): Endpunkt des Intervalls
        num (int): Anzahl der zu ermittelnden Werte (muss >= 2 sein)
        basis (int): Basis für logarithmische Skala

    Returns:
        list[int]: Liste von ganzen Zahlen auf einer logarithmischen Skala
        
    Throws:
        ValueError: wenn num kleiner als 2
    """

    if num < 2:
        raise ValueError("num < 2 ist ungültig")

    schritt = (stop - start) / (num - 1)

    # Liste
    liste = []

    # Gesamtberechnung
    for i in range(num):

        # Berechnung Exponent
        exponent = start + schritt * i

        # Berechnung Wert
        wert = basis ** exponent

        # Hinzufügen des ganzzahligen Anteils der Zahl zur Liste
        liste.append(int(wert))

    return liste

def main():
    """Hauptfunktion des Programms"""

    #Test
    start = 2
    stop = 4
    num = 5
    basis = 10

    try:
        liste = py_logspace(start, stop, num, basis)
        print(liste)
    except ValueError as error:
        print("Fehler:", error)

    #Vergleich mit numpy.logspace
    print("Vergleich mit numpy.logspace():")
    print(py_logspace(3, 9, 6, 10))
    print(numpy.logspace(3, 9, 6, 10))

    #Grafik
    plt.plot(py_logspace(start, stop, num, basis))
    plt.show()

if __name__ == "__main__":
    main()
