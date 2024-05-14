# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# Programm 1: Eingabe sowie das Speichern und Laden von Daten
from tools_read_save import read_number, save_data, load_data

# Programm 2: Berechnung der Partialsummen der harmonischen Reihe
import harmonic_convergence
from harmonic_convergence import vorwaerts_summation, rueckwaerts_summation
    
def main():
    """
    Hauptfunktion des Experimentierskripts.
    """
    while True:
        try:
            print("\nExperimentsteuerung:\n")
            print("1. Benutzerdefinierte Parameter eingeben und Partialsummen berechnen")
            print("2. Standardparameter verwenden und Partialsummen berechnen")
            print("3. Bereits berechnete Daten aus einer Datei laden")
            print("4. Programm beenden")

            choice = input("\nBitte wählen Sie eine Option:\n")

            if choice == "1":
                # Benutzerdefinierte Parameter
                harmonic_convergence.main()

            elif choice == "2":
                # Vordefinierter Parameter
                start = 1
                stop = 5
                num = 5
                basis = 10
                
                print("\nStandardparameter:")
                print("Anfangswert für den Logarithmusraum: "+ str(start))
                print("Endwert für den Logarithmusraum: "+ str(stop))
                print("Anzahl der zu berechnenden Partialsummen: "+str(num))
                print("Basis des Logarithmusraums: "+str(basis))
                
                result_vorwaerts_float16 = vorwaerts_summation(start, stop, num, basis, np.float16)
                print("\nVorwaertssummation mit np.float16:", result_vorwaerts_float16)

                result_vorwaerts_float32 = vorwaerts_summation(start, stop, num, basis, np.float32)
                print("\nVorwaertssummation mit np.float32:", result_vorwaerts_float32)

                result_vorwaerts_float64 = vorwaerts_summation(start, stop, num, basis, np.float64)
                print("\nVorwaertssummation mit np.float64:", result_vorwaerts_float64)

                result_rueckwaerts_float16 = rueckwaerts_summation(start, stop, num, basis, np.float16)
                print("\nRueckwaertssummation mit np.float16:", result_rueckwaerts_float16)

                result_rueckwaerts_float32 = rueckwaerts_summation(start, stop, num, basis, np.float32)
                print("\nRueckwaertssummation mit np.float32:", result_rueckwaerts_float32)

                result_rueckwaerts_float64 = rueckwaerts_summation(start, stop, num, basis, np.float64)
                print("\nRueckwaertssummation mit np.float64:", result_rueckwaerts_float64)
              
            elif choice == "3":
                print("Hilfe")
                #Hier hab ich keinen Plan
                

            elif choice == "4":
                print("Programm wird beendet.")
                break

            else:
                print("\nUngültige Eingabe. Bitte wählen Sie eine der aufgeführten Optionen.")

        except ValueError:
            print("Fehler beim Funktionsaufruf. Bitte überprüfen Sie die Eingabewerte.")
            continue

if __name__ == "__main__":
    main()
