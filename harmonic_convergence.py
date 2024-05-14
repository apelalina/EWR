"""
Dieses Programm implementiert die Funktionen vorwaerts_summation und rueckwaerts_summation,
um Partialsummen der harmonischen Reihe mittels Vorwaertssummation bzw. Rueckwaertssummation
zu berechnen.

pylint 2.16.2
astroid 2.14.2
Python 3.11.7 | packaged by Anaconda, Inc.
| (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
8,96/10
"""

import numpy as np
from py_logspace import py_logspace

def vorwaerts_summation(start, stop, num, basis, data_type) -> list:
    """
    Berechnet die Partialsummen der harmonischen Reihe mittels Vorwaertssummation.

    Inputs:
        start (int): Der Anfangswert für den Logarithmusraum.
        stop (int): Der Endwert für den Logarithmusraum.
        num (int): Die Anzahl der Partialsummen.
        basis (int): Die Basis des Logarithmusraums.
        data_type (numpy.dtype): Der Datentyp für die Berechnung.

    Throws:
        ValueError: Wenn ungueltige Eingaben fuer start, stop, num oder basis gemacht werden.

    Returns:
        list: Eine Liste der berechneten Partialsummen.

    """
    result = []
    for k in py_logspace(start, stop, num, basis):
        partialsumme = data_type(0)
        for variable in range(int(k)):
            partialsumme += data_type(1 / (variable + 1))
        result.append(partialsumme)
    return result

def rueckwaerts_summation(start, stop, num, basis, data_type) -> list:
    """
    Berechnet die Partialsummen der harmonischen Reihe mittels Rueckwaertssummation.

    Inputs:
        start (int): Der Anfangswert für den Logarithmusraum.
        stop (int): Der Endwert für den Logarithmusraum.
        num (int): Die Anzahl der Partialsummen.
        basis (int): Die Basis des Logarithmusraums.
        data_type (numpy.dtype): Der Datentyp für die Berechnung.

    Throws:
        ValueError: Wenn ungültige Eingaben für start, stop, num oder basis gemacht werden.

    Returns:
        list: Eine Liste der berechneten Partialsummen.
    """
    result = []
    for k in py_logspace(start, stop, num, basis):
        partialsumme = data_type(0)
        for variable in range(int(k), 0, -1):  # Rueckwaertsschleife
            partialsumme += data_type(1 / variable)
        result.append(partialsumme)
    return result


def main():
    """
    Hauptfunktion des Programms, die die Berechnung und Ausgabe der Partialsummen durchfuehrt.
    """
    while True:
        try:
            #Nutzereingaben
            start = int(input("Start: "))
            stop = int(input("Stop: "))
            num = int(input("Num: "))
            basis = int(input("Basis: "))

            # Vorwaertssummation mit verschiedenen Datentypen
            result_vorwaerts_float16 = vorwaerts_summation(start, stop, num, basis, np.float16)
            print("Vorwaertssummation mit np.float16:", result_vorwaerts_float16)

            result_vorwaerts_float32 = vorwaerts_summation(start, stop, num, basis, np.float32)
            print("Vorwaertssummation mit np.float32:", result_vorwaerts_float32)

            result_vorwaerts_float64 = vorwaerts_summation(start, stop, num, basis, np.float64)
            print("Vorwaertssummation mit np.float64:", result_vorwaerts_float64)

            # Kahan-Summation mit verschiedenen Datentypen
            result_rueckwaerts_float16 = rueckwaerts_summation(start, stop, num, basis, np.float16)
            print("Rueckwaertssummation mit np.float16:", result_rueckwaerts_float16)

            result_rueckwaerts_float32 = rueckwaerts_summation(start, stop, num, basis, np.float32)
            print("Rueckwaertssummation mit np.float32:", result_rueckwaerts_float32)

            result_rueckwaerts_float64 = rueckwaerts_summation(start, stop, num, basis, np.float64)
            print("Rueckwaertssummation mit np.float64:", result_rueckwaerts_float64)

            break

        except ValueError:
            print("Fehler beim Funktionsaufruf. Bitte ueberpruefen Sie die Eingabewerte.")
            continue

if __name__ == "__main__":
    main()
