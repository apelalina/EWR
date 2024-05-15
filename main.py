# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import os

# Programm 1: Eingabe sowie das Speichern und Laden von Daten
from tools_read_save import read_number, save_data, load_data

# Programm 2: Berechnung der Partialsummen der harmonischen Reihe
from harmonic_convergence import vorwaerts_summation, rueckwaerts_summation

# Programm 3: py_logspace
from py_logspace import py_logspace

def main():
    """
    Hauptfunktion des Experimentierskripts.
    """
    try:
        print("\nExperimentsteuerung:\n")
        print("1. Benutzerdefinierte Parameter eingeben und Partialsummen berechnen")
        print("2. Benutzerdefinierte Parameter eingeben und Partialsummen berechnen und abspeichern")
        print("3. Standardparameter verwenden und Partialsummen berechnen")
        print("4. Bereits berechnete Daten aus einer Datei laden")
        print("5. Programm beenden")
        choice = input("\nBitte wählen Sie eine Option:\n")

    except ValueError:
        print("Fehler beim Programmaufruf. Bitte wählen Sie 1, 2, 3 oder 4.")
    
    if choice == "1" or choice == "2":

        start = read_number("Anfangswert fuer den Logarithmusraum: ", int)
        stop = read_number("Endwert fuer den Logarithmusraum: ", int)
        basis = read_number("Basis des Logarithmusraums: ", int)
        num = read_number("Anzahl der zu berechnenden Partialsummen: ", int, lower_limit=2)


        result_vorwaerts_float16 = vorwaerts_summation(start, stop, num, basis, np.float16)
        print("\nVorwaertssummation mit np.float16:\n", result_vorwaerts_float16)

        result_vorwaerts_float32 = vorwaerts_summation(start, stop, num, basis, np.float32)
        print("\nVorwaertssummation mit np.float32:\n", result_vorwaerts_float32)

        result_vorwaerts_float64 = vorwaerts_summation(start, stop, num, basis, np.float64)
        print("\nVorwaertssummation mit np.float64:\n", result_vorwaerts_float64)

        result_rueckwaerts_float16 = rueckwaerts_summation(start, stop, num, basis, np.float16)
        print("\nRueckwaertssummation mit np.float16:\n", result_rueckwaerts_float16)

        result_rueckwaerts_float32 = rueckwaerts_summation(start, stop, num, basis, np.float32)
        print("\nRueckwaertssummation mit np.float32:\n", result_rueckwaerts_float32)

        result_rueckwaerts_float64 = rueckwaerts_summation(start, stop, num, basis, np.float64)
        print("\nRueckwaertssummation mit np.float64:\n", result_rueckwaerts_float64)

        if choice == "2":
            print("Die ausgegebenen Daten werden im Ordnder \"convergence_data_export\" im Arbeitsverzeichnis als .csv-Dateien abgespeichert.")
            save_data(result_vorwaerts_float16, "convergence_data_export/result_vorwaerts_float16.csv")
            save_data(result_vorwaerts_float32, "convergence_data_export/result_vorwaerts_float32.csv")
            save_data(result_vorwaerts_float64, "convergence_data_export/result_vorwaerts_float64.csv")
            save_data(result_rueckwaerts_float16, "convergence_data_export/result_rueckwaerts_float16.csv")
            save_data(result_rueckwaerts_float32, "convergence_data_export/result_rueckwaerts_float32.csv")
            save_data(result_rueckwaerts_float64, "convergence_data_export/result_rueckwaerts_float64.csv")

        #Plot
        x_werte = py_logspace(start, stop, num, basis)
        #Linien
        plt.plot(x_werte, result_vorwaerts_float16, label='Vorwaertssummation mit np.float16', color='black')
        plt.plot(x_werte, result_vorwaerts_float32, label='Vorwaertssummation mit np.float32', color='blue')
        plt.plot(x_werte, result_vorwaerts_float64, label='Vorwaertssummation mit np.float64', color='green')
        plt.plot(x_werte, result_rueckwaerts_float16, label='Rueckwaertssummation mit np.float16', color='red')
        plt.plot(x_werte, result_rueckwaerts_float32, label='Rueckwaertssummation mit np.float32', color='purple')
        plt.plot(x_werte, result_rueckwaerts_float64, label='Rueckwaertssummation mit np.float64', color='yellow')
        #Achsenbeschriftung
        plt.xlabel("Index der Partialsummen in logarithmischer Skalierung")
        plt.ylabel("Partialsummen")
        plt.title("Darstellung der Partialsummen")
        #Legende
        plt.legend()
        plt.show()


    if choice == "3":

        start = 1
        stop = 5
        basis = 10
        num = 10

        print("\nStandardparameter:")
        print("Anfangswert für den Logarithmusraum: "+ str(start))
        print("Endwert für den Logarithmusraum: "+ str(stop))
        print("Anzahl der zu berechnenden Partialsummen: "+str(num))
        print("Basis des Logarithmusraums: "+str(basis))


        result_vorwaerts_float16 = vorwaerts_summation(start, stop, num, basis, np.float16)
        print("\nVorwaertssummation mit np.float16:\n", result_vorwaerts_float16)

        result_vorwaerts_float32 = vorwaerts_summation(start, stop, num, basis, np.float32)
        print("\nVorwaertssummation mit np.float32:\n", result_vorwaerts_float32)

        result_vorwaerts_float64 = vorwaerts_summation(start, stop, num, basis, np.float64)
        print("\nVorwaertssummation mit np.float64:\n", result_vorwaerts_float64)

        result_rueckwaerts_float16 = rueckwaerts_summation(start, stop, num, basis, np.float16)
        print("\nRueckwaertssummation mit np.float16:\n", result_rueckwaerts_float16)

        result_rueckwaerts_float32 = rueckwaerts_summation(start, stop, num, basis, np.float32)
        print("\nRueckwaertssummation mit np.float32:\n", result_rueckwaerts_float32)

        result_rueckwaerts_float64 = rueckwaerts_summation(start, stop, num, basis, np.float64)
        print("\nRueckwaertssummation mit np.float64:\n", result_rueckwaerts_float64)

        #Plot
        x_werte = py_logspace(start, stop, num, basis)
        #Linien
        plt.plot(x_werte, result_vorwaerts_float16, label='Vorwaertssummation mit np.float16', color='black')
        plt.plot(x_werte, result_vorwaerts_float32, label='Vorwaertssummation mit np.float32', color='blue')
        plt.plot(x_werte, result_vorwaerts_float64, label='Vorwaertssummation mit np.float64', color='green')
        plt.plot(x_werte, result_rueckwaerts_float16, label='Rueckwaertssummation mit np.float16', color='red')
        plt.plot(x_werte, result_rueckwaerts_float32, label='Rueckwaertssummation mit np.float32', color='purple')
        plt.plot(x_werte, result_rueckwaerts_float64, label='Rueckwaertssummation mit np.float64', color='yellow')
        #Achsenbeschriftung
        plt.xlabel("Index der Partialsummen in logarithmischer Skalierung")
        plt.ylabel("Partialsummen")
        plt.title("Darstellung der Partialsummen")
        #Legende
        plt.legend()
        plt.show()

    if choice == "4":
        print("Die zu ladenden Daten werden aus dem Ordner \"convergence_data_import\" im entsprechenden Arbeitsverzeichnis geladen. Bitte stellen Sie die Daten im csv-Format in diesem Ordner bereit.")
        print("Bitte waehlen Sie folgende Dateinamen: result_vorwaerts_float16.csv, result_vorwaerts_float32.csv, result_vorwaerts_float32.csv, result_rueckwaerts_float16.csv, result_rueckwaerts_float32.csv, result_rueckwaerts_float32.csv")
        ip = input("Programm mit \"ok\" fortsetzen, sobald die Daten bereitgestellt sind: ")

        if(ip == "ok"):
            result_vorwaerts_float16 = load_data("convergence_data_import/result_vorwaerts_float16.csv")
            result_vorwaerts_float32 = load_data("convergence_data_import/result_vorwaerts_float32.csv")
            result_vorwaerts_float64 = load_data("convergence_data_import/result_vorwaerts_float64.csv")
            result_rueckwaerts_float16 = load_data("convergence_data_import/result_rueckwaerts_float16.csv")
            result_rueckwaerts_float32 = load_data("convergence_data_import/result_rueckwaerts_float32.csv")
            result_rueckwaerts_float64 = load_data("convergence_data_import/result_rueckwaerts_float64.csv")

            start = read_number("Was war der Anfangswert fuer diesen Logarithmusraum? ", int)
            stop = read_number("Was war der Endwert fuer diesen Logarithmusraum? ", int)
            basis = read_number("Was war die Basis dieses Logarithmusraums? ", int)
            num = len(result_vorwaerts_float16)

            #Plot
            x_werte = py_logspace(start, stop, num, basis)
            #Linien
            plt.plot(x_werte, result_vorwaerts_float16, label='Vorwaertssummation mit np.float16', color='black')
            plt.plot(x_werte, result_vorwaerts_float32, label='Vorwaertssummation mit np.float32', color='blue')
            plt.plot(x_werte, result_vorwaerts_float64, label='Vorwaertssummation mit np.float64', color='green')
            plt.plot(x_werte, result_rueckwaerts_float16, label='Rueckwaertssummation mit np.float16', color='red')
            plt.plot(x_werte, result_rueckwaerts_float32, label='Rueckwaertssummation mit np.float32', color='purple')
            plt.plot(x_werte, result_rueckwaerts_float64, label='Rueckwaertssummation mit np.float64', color='yellow')
            #Achsenbeschriftung
            plt.xlabel("Index der Partialsummen in logarithmischer Skalierung")
            plt.ylabel("Partialsummen")
            plt.title("Darstellung der Partialsummen")
            #Legende
            plt.legend()
            plt.show()
           
        else:
            print("Programm beendet.")
            exit()
        
    if choice == "5":
        print("Programm beendet.")
        exit()

if __name__ == "__main__":
    main()
