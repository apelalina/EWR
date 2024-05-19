# -*- coding: utf-8 -*-

"""
Dieses Programm implementiert die Funktionen vorwaerts_summation und rueckwaerts_summation,
um Partialsummen der harmonischen Reihe mittels Vorwaertssummation bzw. Rueckwaertssummation
zu berechnen.

pylint 2.16.2
astroid 2.14.2
Python 3.11.7 | packaged by Anaconda, Inc.
| (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
9.84/10
"""

import numpy as np
import matplotlib.pyplot as plt
from py_logspace import py_logspace # pylint: disable=import-error

def vorwaerts_summation(start, stop, num, basis, data_type) -> list:
    """
    Berechnet die Partialsummen der harmonischen Reihe mittels Vorwaertssummation.

    Inputs:
        start (int): Der Anfangswert fuer den Logarithmusraum.
        stop (int): Der Endwert fuer den Logarithmusraum.
        num (int): Die Anzahl der Partialsummen.
        basis (int): Die Basis des Logarithmusraums.
        data_type (numpy.dtype): Der Datentyp fuer die Berechnung.

    Throws:
        ValueError: Wenn ungueltige Eingaben fuer start, stop, num oder basis gemacht werden.

    Returns:
        list: Eine Liste der berechneten Partialsummen.

    """
    result = []
    partialsumme=data_type(0) # Casting zum gewuenschten Datentyp
    for i in range(1, basis**stop +1):
        partialsumme += data_type(1 / (i))
        # damit nicht jedes mal "von vorne" aufsummiert werden muss:
        if i in py_logspace(start, stop, num, basis):
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
        data_type (numpy.dtype): Der Datentyp fuer die Berechnung.

    Throws:
        ValueError: Wenn ungültige Eingaben fuer start, stop, num oder basis gemacht werden.

    Returns:
        list: Eine Liste der berechneten Partialsummen.
    """
    result = []
    for k in py_logspace(start, stop, num, basis):
        partialsumme = data_type(0) # Casting zum gewuenschten Datentyp
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
            start = int(input("Anfangswert fuer den Logarithmusraum: "))
            stop = int(input("Endwert fuer den Logarithmusraum: "))
            num = int(input("Anzahl der zu berechnenden Partialsummen: "))
            basis = int(input("Basis des Logarithmusraums: "))

            # Vorwaertssummation mit verschiedenen Datentypen
            result_vorwaerts_float16 = vorwaerts_summation(start, stop, num, basis, np.float16)
            print("\nVorwaertssummation mit np.float16:", result_vorwaerts_float16)

            result_vorwaerts_float32 = vorwaerts_summation(start, stop, num, basis, np.float32)
            print("\nVorwaertssummation mit np.float32:", result_vorwaerts_float32)

            result_vorwaerts_float64 = vorwaerts_summation(start, stop, num, basis, np.float64)
            print("\nVorwaertssummation mit np.float64:", result_vorwaerts_float64)

            # Kahan-Summation mit verschiedenen Datentypen
            result_rueckwaerts_float16 = rueckwaerts_summation(start, stop, num, basis, np.float16)
            print("\nRueckwaertssummation mit np.float16:", result_rueckwaerts_float16)

            result_rueckwaerts_float32 = rueckwaerts_summation(start, stop, num, basis, np.float32)
            print("\nRueckwaertssummation mit np.float32:", result_rueckwaerts_float32)

            result_rueckwaerts_float64 = rueckwaerts_summation(start, stop, num, basis, np.float64)
            print("\nRueckwaertssummation mit np.float64:", result_rueckwaerts_float64)

            #Plot
            #Werte
            x_werte=py_logspace(start, stop, basis, num)
            y_werte1=result_vorwaerts_float16
            y_werte2=result_vorwaerts_float32
            y_werte3=result_vorwaerts_float64
            y_werte4=result_rueckwaerts_float16
            y_werte5=result_rueckwaerts_float32
            y_werte6=result_rueckwaerts_float64
            #Plot der Linien
            plt.plot(x_werte, y_werte1, label='Vorwaertssummation mit np.float16', color='black')
            plt.plot(x_werte, y_werte2, label='Vorwaertssummation mit np.float32', color='blue')
            plt.plot(x_werte, y_werte3, label='Vorwaertssummation mit np.float64', color='green')
            plt.plot(x_werte, y_werte4, label='Rueckwaertssummation mit np.float16', color='red')
            plt.plot(x_werte, y_werte5, label='Rueckwaertssummation mit np.float32', color='purple')
            plt.plot(x_werte, y_werte6, label='Rueckwaertssummation mit np.float64', color='yellow')
            #Achsenbeschriftung
            plt.xlabel("Index der Partialsummen in logarithmischer Skalierung")
            plt.ylabel("Partialsummen")
            plt.title("Darstellung der Partialsummen")
            #Legende
            plt.legend()
            plt.show()

            break

        except ValueError:
            print("Fehler beim Funktionsaufruf. Bitte ueberpruefen Sie die Eingabewerte.")

            continue

if __name__ == "__main__":
    main()
