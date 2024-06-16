"""
Experimentierskript zur Approximation von Pi
"""

import sys
import pandas as pd
import numpy as np
from decimal import Decimal, getcontext # Datentyp
from approx_pi import pi_leibniz, error_pi, plot_pi
from py_logspace import py_logspace
from tools_read_save import read_number, save_data, load_data # pylint: disable=import-error

def main():
    print("\nIn diesem Experiment wird die Approximation der Kreiszahl Pi mittels verschiedener Methoden untersucht. Bitte wählen Sie eine Approximationsmethode:\n")
    print("1. Leibniz-Reihe")
    print("2. Monte-Carlo-Methode")
    print("3. Viete-Algorithmus")
    print("4. Chudnovsky-Algorithmus")
    print("0. Programm beenden")
    choice = input("\nBitte wählen Sie eine Option:\n")

    if choice == "1":
        print("\nApproximation von Pi mittels der Leibniz-Reihe\n")
        print("Die Leibniz-Reihe ist eine Folge von Partialsummen, die im Unendlichen gegen Pi konvergiert. Je größer der Index der berechneten Partialsumme, desto genauer die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des Experiments als Zweierpotenz (2^k) erwartet. Das Programm approximiert Pi für 200 Eingabewerte zwischen 1 und 2^k\n")

        stop = read_number("Bitte den höchsten Index der Partialsumme der Leibniz-Reihe eingeben: 2^", data_type = int, lower_limit = 0)

        indizes = []
        pi = []
        fehler = []
        operations = []
        laufzeiten = []

        for n in py_logspace(start = 0, stop = stop, num = 200, basis = 2):
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



    if choice == "0":
        print("Programm beendet.")
        sys.exit()



if __name__ == "__main__":
    main()