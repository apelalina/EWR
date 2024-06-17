"""
Experimentierskript zur Approximation von Pi
"""

import sys
import pandas as pd
import numpy as np
from decimal import Decimal, getcontext # Datentyp
from approx_pi import pi_leibniz, error_pi, plot_pi, pi_viete, pi_chudnovsky
from py_logspace import py_logspace
from tools_read_save import read_number # pylint: disable=import-error

def main():
    print("\nIn diesem Experiment wird die Approximation der Kreiszahl Pi mittels verschiedener Methoden untersucht. Bitte wählen Sie eine Approximationsmethode:\n")
    print("1. Leibniz-Reihe")
    print("2. Monte-Carlo-Methode")
    print("3. Vietas Produktdarstellung")
    print("4. Chudnovsky-Algorithmus")
    print("0. Programm beenden")
    choice = input("\nBitte wählen Sie eine Option:\n")

    if choice == "1":
        print("\nApproximation von Pi mittels der Leibniz-Reihe\n")
        print("Die Leibniz-Reihe ist eine Folge von Partialsummen, die im Unendlichen gegen Pi konvergiert. Je größer der Index der berechneten Partialsumme, desto genauer die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für 20 Eingabewerte zwischen 1 und 10^k\n")

        stop = read_number("Bitte den höchsten Index der Partialsumme eingeben: 10^", data_type = int, lower_limit = 0)

        indizes = []
        pi = []
        fehler = []
        operations = []
        laufzeiten = []

        for n in py_logspace(start = 0, stop = stop, num = 20, basis = 10):
            pi_leibniz_approx, leibniz_ops, leibniz_time = pi_leibniz(n)
            indizes.append(n)
            pi.append(pi_leibniz_approx)
            fehler.append(error_pi(pi_leibniz_approx))
            operations.append(leibniz_ops)
            laufzeiten.append(leibniz_time)

        data = pd.DataFrame({
            "n": indizes,
            "Pi": pi,
            "Fehler": fehler,
            "Operationen": operations,
            "Laufzeit": laufzeiten
        })

        print("\nDie Approximation von Pi mit der Leibniz-Reihe ergab folgende Ergebnisse:")    
        print(data)
        plot_pi(data, y = "Fehler")

    if choice == "3":
        print("\nApproximation von Pi mittels Vietas Produktdarstellung\n")
        print("Vietas Produktdarstellung der Kreiszahl Pi nutzt ein unendliches Produkt, was gegen Pi konvergiert. Je größer der Index des berechneten Partialprodukts, desto genauer die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für 20 Eingabewerte zwischen 1 und 10^k\n")

        stop = read_number("Bitte den höchsten Index des Partialprodukts eingeben: 10^", data_type = int, lower_limit = 0)

        indizes = []
        pi = []
        fehler = []
        operations = []
        laufzeiten = []

        for n in py_logspace(start = 0, stop = stop, num = 20, basis = 10):
            pi_viete_approx, viete_ops, viete_time = pi_viete(n)
            indizes.append(n)
            pi.append(pi_viete_approx)
            fehler.append(error_pi(pi_viete_approx))
            operations.append(viete_ops)
            laufzeiten.append(viete_time)

        data = pd.DataFrame({
            "n": indizes,
            "Pi": pi,
            "Fehler": fehler,
            "Operationen": operations,
            "Laufzeit": laufzeiten
        })

        print("\nDie Approximation von Pi mittels Vietas Produktdarstellung ergab folgende Ergebnisse:")    
        print(data)
        plot_pi(data, y = "Pi")

    if choice == "4":
        print("\nApproximation von Pi mittels Chudnovsky-Algorithmus\n")
        print("Der Chudnovsky-Algorithmus basiert auf der Konvergenz einer verallgemeinerten hypergeometrischen Reihe gegen Pi/4. Je größer der Index der berechneten Partialsumme, desto genauer die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für 20 Eingabewerte zwischen 1 und 10^k\n")

        stop = read_number("Bitte den höchsten Index der Partialsumme eingeben: 10^", data_type = int, lower_limit = 0)

        indizes = []
        pi = []
        fehler = []
        operations = []
        laufzeiten = []

        for n in py_logspace(start = 0, stop = stop, num = 20, basis = 10):
            pi_chudnovsky_approx, chudnovsky_ops, chudnovsky_time = pi_chudnovsky(n)
            indizes.append(n)
            pi.append(pi_chudnovsky_approx)
            fehler.append(error_pi(pi_chudnovsky_approx))
            operations.append(chudnovsky_ops)
            laufzeiten.append(chudnovsky_time)

        data = pd.DataFrame({
            "n": indizes,
            "Pi": pi,
            "Fehler": fehler,
            "Operationen": operations,
            "Laufzeit": laufzeiten
        })

        print("\nDie Approximation von Pi mittels Vietas Produktdarstellung ergab folgende Ergebnisse:")    
        print(data)
        plot_pi(data, y = "Pi")



    if choice == "0":
        print("Programm beendet.")
        sys.exit()



if __name__ == "__main__":
    main()