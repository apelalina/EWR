"""
Experimentierskript zur Approximation von Pi
"""

import sys
import pandas as pd
import numpy as np
from decimal import Decimal, getcontext # Datentyp
import matplotlib.pyplot as plt 
from approx_pi import pi_leibniz, error_pi, pi_viete, pi_chudnovsky, pi_montecarlo
from py_logspace import py_logspace
from tools_read_save import read_number # pylint: disable=import-error

def experiment_pi(algorithm: str, stop: int, precision = 100):

    if algorithm not in ["montecarlo", "leibniz", "viete", "chudnovsky"]:
        raise ValueError("Bitte geben Sie eine der folgenden Optionen als Algorithmus an: montecarlo, leibniz, viete, chudnovsky")

    indizes = []
    pi = []
    fehler = []
    operations = []
    laufzeiten = []

    for n in py_logspace(start = 0, stop = stop, num = 30, basis = 10):
        if algorithm == "montecarlo":
            pi_approx, ops, time = pi_montecarlo(n, precision)
        elif algorithm == "leibniz":
            pi_approx, ops, time = pi_leibniz(n, precision)
        elif algorithm == "viete":
            pi_approx, ops, time = pi_viete(n, precision)
        elif algorithm == "chudnovsky":
            pi_approx, ops, time = pi_chudnovsky(n, precision)
        
        indizes.append(n)
        pi.append(pi_approx)
        fehler.append(error_pi(pi_approx))
        operations.append(ops)
        laufzeiten.append(time)

    data = pd.DataFrame({
            "n": indizes,
            "Pi": pi,
            "Fehler": fehler,
            "Operationen": operations,
            "Laufzeit": laufzeiten
        })

    return data

def plot_pi(data, y = "Pi", linecolor = "blue", pointcolor = "darkblue", label = ""):

    if y == "Pi":
        plt.semilogx(data["n"], data["Pi"], color = linecolor)
        plt.plot(data["n"], data["Pi"], color = pointcolor,   marker = '.', linestyle = '', label = label)
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Schäzung von $\pi$")
        plt.grid()
        plt.legend()

    if y == "Fehler":
        plt.loglog(data["n"], data["Fehler"], color = linecolor)
        plt.plot(data["n"], data["Fehler"], color = pointcolor,   marker = '.', linestyle = '', label = label)
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Fehler (Differenz zu $\pi$)")
        plt.grid()
        plt.legend()

    if y == "Laufzeit":
        plt.loglog(data["n"], data["Laufzeit"], color = linecolor)
        plt.plot(data["n"], data["Laufzeit"], color = pointcolor,   marker = '.', linestyle = '', label = label)
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Laufzeit in ms")
        plt.grid()
        plt.legend()

    if y == "Operationen":
        plt.loglog(data["n"], data["Operationen"], color = linecolor)
        plt.plot(data["n"], data["Operationen"], color = pointcolor,   marker = '.', linestyle = '', label = label)
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Anzahl der benötigten Operationen")
        plt.grid()
        plt.legend()
    
    if y == "Montecarlo":
        getcontext().prec = 1010
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        pi = Decimal(pi) * Decimal('1')
        plt.scatter(data["n"], data["Pi"], s = 4, color = pointcolor, label = label)
        plt.axhline(y=pi, color="red", label = "$\pi$")
        plt.xlabel("Eingabeparameter n (Anzahl generierter Punkte)")
        plt.ylabel("Schäzung von $\pi$")
        plt.grid()
        plt.legend(loc='lower right')
    
    if y == "Laufzeit_Fehler":
        data_sorted = data.sort_values('Laufzeit')
        plt.loglog(data_sorted["Laufzeit"], data_sorted["Fehler"], color = linecolor)
        plt.plot(data_sorted["Laufzeit"], data_sorted["Fehler"], color = pointcolor,   marker = '.', linestyle = 'none', label = label)
        plt.xlabel("Laufzeit in ms")
        plt.ylabel("Differenz zu $\pi$")
        plt.grid()
        plt.legend()
    

def main():
    print("\nIn diesem Experiment wird die Effizienz und Genauigkeit in der Approximation der Kreiszahl Pi mittels ausgew¨ahlter Algorithmen untersucht. Bitte wählen Sie eine Approximationsmethode:\n")
    print("1. Monte-Carlo-Methode")
    print("2. Leibniz-Reihe")
    print("3. Vietas Produktdarstellung")
    print("4. Chudnovsky-Algorithmus")
    print("5. Alle Algorithmen vergleichen")
    print("6. Mantissenlängen vergleichen")
    print("7. Demonstration eines Minimalbeispiels")
    print("0. Programm beenden")

    while True:
        choice = input("\nBitte wählen Sie eine Option:\n")
        if choice in ["1", "2", "3", "4", "5", "6", "7", "0"]:
            break
        else:
            print("Dies ist keine der angebotenen Optionen.")

    if choice == "1":
        print("\nApproximation von Pi mit der Monte-Carlo-Methode\n")
        print("Dabei wird Pi mithilfe eines Zufallsexperiments geschätzt. Je öfter das Zufallsexperiment wiederholt wird, desto genauer ist die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für 30 Eingabewerte zwischen 1 und 10^k\n")

        stop = read_number("Bitte die Anzahl der Zufallsexperimente für die Monte-Carlo-Methode eingeben: 10^", data_type = int, lower_limit = 0)
        precision = read_number("Mantissenlänge der Zahlendarstellung: ", data_type = int, lower_limit = 1, upper_limit = 1000)

        data1 = experiment_pi("montecarlo", stop, precision)
        data2 = experiment_pi("montecarlo", stop, precision)
        data3 = experiment_pi("montecarlo", stop, precision)
        data4 = experiment_pi("montecarlo", stop, precision)
        data5 = experiment_pi("montecarlo", stop, precision)
        data6 = experiment_pi("montecarlo", stop, precision)
        data7 = experiment_pi("montecarlo", stop, precision)
        data8 = experiment_pi("montecarlo", stop, precision)
        data9 = experiment_pi("montecarlo", stop, precision)
        data10 = experiment_pi("montecarlo", stop, precision)

        # Datenreihen zusammenfügen
        data1["Versuchsreihe"] = 1
        data2["Versuchsreihe"] = 2
        data3["Versuchsreihe"] = 3
        data4["Versuchsreihe"] = 4
        data5["Versuchsreihe"] = 5
        data6["Versuchsreihe"] = 6
        data7["Versuchsreihe"] = 7
        data8["Versuchsreihe"] = 8
        data9["Versuchsreihe"] = 9
        data10["Versuchsreihe"] = 10

        data = pd.concat([data1, data2, data3, data4, data5, data6, data7, data8, data9, data10])

        data.to_csv("pi_montecarlo_" + str(stop) + ".csv")
        print("Die Ergebnisse wurden in " + "pi_montecarlo_" + str(stop) + ".csv im Arbeitsverzeichnis gespeichert.\n")

        print("\nDa es sich bei der Monte-Carlo-Methode um ein stochastisches Verfahren handelt, wurde das von Ihnen spezifizierte Experiment 10 Mal wiederholt:")
        
        plot_pi(data, "Montecarlo", label = "Schätzung von $\pi$ nach Monte-Carlo")
        plt.savefig('Montecarlo_Konvergenzplot.pdf')
        plt.show()

        print("In der Abbildung ist jedoch erkennbar, dass die verschiedenen Durchgänge für große n immer ähnlichere Ergebnisse liefern. Deshalb wird nachfolgend zur Übersichtlichkeit nur noch eine einzige Datenreihe dargestellt.\n")

        plot_pi(data1, "Fehler", label = "Monte-Carlo-Methode")
        plt.savefig('Montecarlo_Fehlerplot.pdf')
        plt.show()

        plot_pi(data1, "Laufzeit", label="Monte-Carlo-Methode")
        plt.savefig('Montecarlo_Laufzeitplot.pdf')
        plt.show()

        plot_pi(data1, "Operationen", label="Monte-Carlo-Methode")
        plt.savefig('Montecarlo_Operationenplot.pdf')
        plt.show()

        plot_pi(data1, "Laufzeit_Fehler", label="Monte-Carlo-Methode")
        plt.savefig('Montecarlo_Laufzeit_Fehlerplot.pdf')
        plt.show()

        print("\nAlle Plots wurden im Arbeitsverzeichnis gespeichert.\n")

    elif choice == "2":
        print("\nApproximation von Pi mittels der Leibniz-Reihe\n")
        print("Die Leibniz-Reihe ist eine Folge von Partialsummen, die im Unendlichen gegen Pi/4 konvergiert. Je größer der Index der berechneten Partialsumme, desto genauer die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für 30 Eingabewerte zwischen 1 und 10^k\n")

        stop = read_number("Bitte den höchsten Index der Partialsumme der Leibniz-Reihe eingeben: 10^", data_type = int, lower_limit = 0)
        precision = read_number("Mantissenlänge der Zahlendarstellung: ", data_type = int, lower_limit = 1, upper_limit = 1000)

        data = experiment_pi("leibniz", stop, precision)

        data.to_csv("pi_leibniz_" + str(stop) + ".csv")
        print("Die Ergebnisse wurden in " + "pi_leibniz_" + str(stop) + ".csv im Arbeitsverzeichnis gespeichert.\n")

        plot_pi(data, "Pi", label = "Pi nach Leibniz-Approximation")
        getcontext().prec = 1010
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        pi = Decimal(pi)
        plt.axhline(y=pi, color="red", label = "$\pi$")
        plt.legend()
        plt.savefig('Leibniz_Konvergenzplot.pdf')
        plt.show()

        plot_pi(data, "Fehler", label = "Leibniz-Approximation")
        plt.savefig('Leibniz_Fehlerplot.pdf')
        plt.show()

        plot_pi(data, "Laufzeit", label="Leibniz-Approximation")
        plt.savefig('Leibniz_Laufzeitplot.pdf')
        plt.show()

        plot_pi(data, "Operationen", label="Leibniz-Approximation")
        plt.savefig('Leibniz_Operationenplot.pdf')
        plt.show()

        plot_pi(data, "Laufzeit_Fehler", label="Leibniz-Approximation")
        plt.savefig('Leibniz_Laufzeit_Fehlerplot.pdf')
        plt.show()

        print("\nAlle Plots wurden im Arbeitsverzeichnis gespeichert.\n")

    elif choice == "3":
        print("\nApproximation von Pi mittels Vietes Produktdarstellung\n")
        print("Vietes Produktdarstellung der Kreiszahl Pi nutzt ein unendliches Produkt, was gegen Pi/2 konvergiert. Je größer der Index des berechneten Partialprodukts, desto genauer die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für 30 Eingabewerte zwischen 1 und 10^k\n")

        stop = read_number("Bitte den höchsten Index des Partialprodukts für Vietes Produktdarstellung eingeben: 10^", data_type = int, lower_limit = 0)
        precision = read_number("Mantissenlänge der Zahlendarstellung: ", data_type = int, lower_limit = 1, upper_limit = 1000)

        data = experiment_pi("viete", stop, precision)

        data.to_csv("pi_viete_" + str(stop) + ".csv")
        print("Die Ergebnisse wurden in " + "pi_viete_" + str(stop) + ".csv im Arbeitsverzeichnis gespeichert.\n")

        plot_pi(data, "Pi", label = "Pi nach Viete-Approximation")
        getcontext().prec = 1010
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        pi = Decimal(pi)
        plt.axhline(y=pi, color="red", label = "$\pi$")
        plt.legend()
        plt.savefig('Viete_Fehlerplot.pdf')
        plt.show()

        plot_pi(data, "Fehler", label = "Viete-Approximation")
        plt.savefig('Viete_Fehlerplot.pdf')
        plt.show()

        plot_pi(data, "Laufzeit", label="Viete-Approximation")
        plt.savefig('Viete_Laufzeitplot.pdf')
        plt.show()

        plot_pi(data, "Operationen", label="Viete-Approximation")
        plt.savefig('Viete_Operationenplot.pdf')
        plt.show()

        plot_pi(data, "Laufzeit_Fehler", label="Viete-Approximation")
        plt.savefig('Viete_Laufzeit_Fehlerplot.pdf')
        plt.show()

        print("\nAlle Plots wurden im Arbeitsverzeichnis gespeichert.\n")

    elif choice == "4":
        print("\nApproximation von Pi mittels Chudnovsky-Algorithmus\n")
        print("Der Chudnovsky-Algorithmus basiert auf der Konvergenz einer verallgemeinerten hypergeometrischen Reihe gegen 1/Pi. Je größer der Index der berechneten Partialsumme, desto genauer die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für 30 Eingabewerte zwischen 1 und 10^k\n")

        stop = read_number("Bitte den höchsten Index der Partialsumme für den Chudnovsky-Algorithmus eingeben: 10^", data_type = int, lower_limit = 0)
        precision = read_number("Mantissenlänge der Zahlendarstellung: ", data_type = int, lower_limit = 1, upper_limit = 1000)

        data = experiment_pi("chudnovsky", stop, precision)

        data.to_csv("pi_chudnovsky_" + str(stop) + ".csv")
        print("Die Ergebnisse wurden in " + "pi_chudnovsky_" + str(stop) + ".csv im Arbeitsverzeichnis gespeichert.\n")

        plot_pi(data, "Pi", label = "Pi nach Chudnovsky")
        getcontext().prec = 1010
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        pi = Decimal(pi)
        plt.axhline(y=pi, color="red", label = "$\pi$")
        plt.legend()
        plt.savefig('Chudnovsky_Konvergenzplot.pdf')
        plt.show()

        plot_pi(data, "Fehler", label = "Chudnovsky-Algorithmus")
        plt.savefig('Chudnovsky_Fehlerplot.pdf')
        plt.show()

        plot_pi(data, "Laufzeit", label="Chudnovsky-Algorithmus")
        plt.savefig('Chudnovsky_Laufzeitplot.pdf')
        plt.show()

        plot_pi(data, "Operationen", label="Chudnovsky-Algorithmus")
        plt.savefig('Chudnovsky_Operationenplot.pdf')
        plt.show()

        plot_pi(data, "Laufzeit_Fehler", label="Chudnovsky-Algorithmus")
        plt.savefig('Chudnovsky_Laufzeit_Fehlerplot.pdf')
        plt.show()

        print("\nAlle Plots wurden im Arbeitsverzeichnis gespeichert.\n")

    elif choice == "5":
        print("\nVergleich der Algorithmen: Monte-Carlo-Methode, Leibniz-Reihe, Vietes Produktdarstellung, Chudnovsky-Algorithmus \n")
        stop_montecarlo = read_number("Bitte die Anzahl der Zufallsexperimente für die Monte-Carlo-Methode eingeben: 10^", data_type = int, lower_limit = 0)
        stop_leibniz = read_number("Bitte den höchsten Index der Partialsumme der Leibniz-Reihe eingeben: 10^", data_type = int, lower_limit = 0)
        stop_viete = read_number("Bitte den höchsten Index des Partialprodukts für Vietes Produktdarstellung eingeben: 10^", data_type = int, lower_limit = 0)
        stop_chudnovsky = read_number("Bitte den höchsten Index der Partialsumme für den Chudnovsky-Algorithmus eingeben: 10^", data_type = int, lower_limit = 0)

        precision = read_number("Mantissenlänge der Zahlendarstellung: ", data_type = int, lower_limit = 1, upper_limit = 1000)

        # Experimente durchführen
        data_montecarlo = experiment_pi("montecarlo", stop_montecarlo, precision)
        print("Berechnungen für Monte-Carlo abgeschlossen.")
        data_leibniz = experiment_pi("leibniz", stop_leibniz, precision)
        print("Berechnungen für Leibniz abgeschlossen.")
        data_viete = experiment_pi("viete", stop_viete, precision)
        print("Berechnungen für Viete abgeschlossen.")
        data_chudnovsky = experiment_pi("chudnovsky", stop_chudnovsky, precision)
        print("Berechnungen für Chudnovsky abgeschlossen.")

        # Datensätze zusammenfügen und
        data_montecarlo["Algorithmus"] = "montecarlo"
        data_leibniz["Algorithmus"] = "leibniz"
        data_viete["Algorithmus"] = "viete"
        data_chudnovsky["Algorithmus"] = "chudnovsky"
        data = pd.concat([data_montecarlo, data_leibniz, data_viete, data_chudnovsky])

        # Daten abspeichern
        data.to_csv("Algorithmenvergleich_" + str(precision) + ".csv")
        print("Die Ergebnisse wurden in " + "Algorithmenvergleich" + str(precision) + ".csv im Arbeitsverzeichnis gespeichert.\n")

        # Konvergenzplot
        plot_pi(data_montecarlo, y = "Pi", linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Pi", linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Pi", linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Pi", linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        getcontext().prec = 1010
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        pi = Decimal(pi)
        plt.axhline(y=pi, color="slategrey", label = "$\pi$")
        plt.grid()
        plt.legend()
        plt.savefig('Algorithmenvergleich_Konvergenzplot.pdf')
        plt.show()

        # Fehlerplot
        plot_pi(data_montecarlo, y = "Fehler", linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Fehler", linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Fehler", linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Fehler", linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Algorithmenvergleich_Fehlerplot.pdf')
        plt.show()

        # Laufzeitplot
        plot_pi(data_montecarlo, y = "Laufzeit", linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Laufzeit", linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Laufzeit", linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Laufzeit", linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Algorithmenvergleich_Laufzeitplot.pdf')
        plt.show()

        # Operationenplot
        plot_pi(data_montecarlo, y = "Operationen", linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Operationen", linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Operationen", linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Operationen", linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        # Kurven für O(n) und O(n^2) einfügen
        getcontext().prec = 1010
        x_vec = range(max(data["n"]) + 1)
        f1_vec = []
        f2_vec = []
        for x in x_vec:
            f1_vec.append((Decimal('20')* Decimal('1')) * (Decimal(x) * Decimal('1')))
        for x in x_vec:
            f2_vec.append((Decimal('20')* Decimal('1')) * (Decimal(x) * Decimal('1'))**Decimal('2'))
        plt.plot(x_vec, f1_vec, color = "darkgray", label = "f(x) = 20 * x")
        plt.plot(x_vec, f2_vec, color = "silver", label = "g(x) = 20 * $x^{2}$")

        plt.legend()
        plt.savefig('Algorithmenvergleich_Operationenplot.pdf')
        plt.show()

        # Laufzeit-Fehler-Plot
        plot_pi(data_montecarlo, y = "Laufzeit_Fehler", linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Laufzeit_Fehler", linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Laufzeit_Fehler", linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Laufzeit_Fehler", linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Algorithmenvergleich_Laufzeit-Fehler-Plot.pdf')
        plt.show()

        print("\nAlle Plots wurden im Arbeitsverzeichnis gespeichert.\n")

    elif choice == "6":

        # Algorithmus auswählen
        print("\nFür welchen Algorithmus möchten Sie verschiedene Mantissenlängen vergleichen?")
        while True:
            algorithm = input("Algorithmus (montecarlo, leibniz, viete, chudnovsky): ")   
            if algorithm not in ["montecarlo", "leibniz", "viete", "chudnovsky"]:
                print("Bitte geben Sie eine der folgenden Optionen als Algorithmus an: montecarlo, leibniz, viete, chudnovsky")
            else:
                break
        
        # Eingabeparameter
        if algorithm == "montecarlo":
            stop = read_number("Bitte die Anzahl der Zufallsexperimente für die Monte-Carlo-Methode eingeben: 10^", data_type = int, lower_limit = 0)
            legend_title = "Monte-Carlo-Methode"
        elif algorithm == "leibniz":
            stop = read_number("Bitte den höchsten Index der Partialsumme der Leibniz-Reihe eingeben: 10^", data_type = int, lower_limit = 0)
            legend_title = "Leibniz-Reihe"
        elif algorithm == "viete":
            stop = read_number("Bitte den höchsten Index des Partialprodukts für Vietes Produktdarstellung eingeben: 10^", data_type = int, lower_limit = 0)
            legend_title = "Vietes Produktdarstellung"
        elif algorithm == "chudnovsky":
            stop = read_number("Bitte den höchsten Index der Partialsumme für den Chudnovsky-Algorithmus eingeben: 10^", data_type = int, lower_limit = 0)
            legend_title = "Chudnovsky-Algorithmus"

        # Mantissenlängen
        print("\nBitte geben Sie 5 verschiedene Mantissenlängen an, die sie vergleichen möchten.")
        precision1 = read_number("1. Mantissenlänge der Zahlendarstellung: ", data_type = int, lower_limit = 1, upper_limit = 1000)
        precision2 = read_number("2. Mantissenlänge der Zahlendarstellung: ", data_type = int, lower_limit = 1, upper_limit = 1000)
        precision3 = read_number("3. Mantissenlänge der Zahlendarstellung: ", data_type = int, lower_limit = 1, upper_limit = 1000)
        precision4 = read_number("4. Mantissenlänge der Zahlendarstellung: ", data_type = int, lower_limit = 1, upper_limit = 1000)
        precision5 = read_number("5. Mantissenlänge der Zahlendarstellung: ", data_type = int, lower_limit = 1, upper_limit = 1000)
        print("\n")

        # Berechnungen
        data1 = experiment_pi(algorithm = algorithm, stop = stop, precision = precision1)
        data1["Mantissenlänge"] = precision1
        print("Berechnungen für Mantissenlänge " + str(precision1) + " abgeschlossen.")
        data2 = experiment_pi(algorithm = algorithm, stop = stop, precision = precision2)
        data2["Mantissenlänge"] = precision2
        print("Berechnungen für Mantissenlänge " + str(precision2) + " abgeschlossen.")
        data3 = experiment_pi(algorithm = algorithm, stop = stop, precision = precision3)
        data3["Mantissenlänge"] = precision3
        print("Berechnungen für Mantissenlänge " + str(precision3) + " abgeschlossen.")
        data4 = experiment_pi(algorithm = algorithm, stop = stop, precision = precision4)
        data4["Mantissenlänge"] = precision4
        print("Berechnungen für Mantissenlänge " + str(precision4) + " abgeschlossen.")
        data5 = experiment_pi(algorithm = algorithm, stop = stop, precision = precision5)
        data5["Mantissenlänge"] = precision5
        print("Berechnungen für Mantissenlänge " + str(precision5) + " abgeschlossen.")

        # Datensätze mergen
        data = pd.concat([data1, data2, data3, data4, data5])

        # Daten abspeichern
        data.to_csv("Mantissenvergleich_" + str(algorithm) + ".csv")
        print("Die Ergebnisse wurden in " + "Mantissenvergleich_" + str(algorithm) + ".csv im Arbeitsverzeichnis gespeichert.")

        # Plots
        print("\nDie Auswirkungen verschiedener Mantissenlängen sind nun im Fehler- und Laufzeitplot erkennbar:")

        # Fehlerplot
        plot_pi(data1, y = "Fehler", linecolor = "red", pointcolor = "darkred", label = "Mantissenlänge " + str(precision1))
        plot_pi(data2, y = "Fehler", linecolor = "orange", pointcolor = "darkorange", label = "Mantissenlänge " + str(precision2))
        plot_pi(data3, y = "Fehler", linecolor = "green", pointcolor = "darkgreen", label = "Mantissenlänge " + str(precision3))
        plot_pi(data4, y = "Fehler", linecolor = "blue", pointcolor = "darkblue", label = "Mantissenlänge " + str(precision4))
        plot_pi(data5, y = "Fehler", linecolor = "darkviolet", pointcolor = "purple", label = "Mantissenlänge " + str(precision5))
        plt.legend(title = legend_title)
        plt.savefig("Mantissenvergleich_Fehlerplot_" + str(algorithm) + ".pdf")
        plt.show()

        # Laufzeitplot
        plot_pi(data1, y = "Laufzeit", linecolor = "red", pointcolor = "darkred", label = "Mantissenlänge " + str(precision1))
        plot_pi(data2, y = "Laufzeit", linecolor = "orange", pointcolor = "darkorange", label = "Mantissenlänge " + str(precision2))
        plot_pi(data3, y = "Laufzeit", linecolor = "green", pointcolor = "darkgreen", label = "Mantissenlänge " + str(precision3))
        plot_pi(data4, y = "Laufzeit", linecolor = "blue", pointcolor = "darkblue", label = "Mantissenlänge " + str(precision4))
        plot_pi(data5, y = "Laufzeit", linecolor = "darkviolet", pointcolor = "purple", label = "Mantissenlänge " + str(precision5))
        plt.legend(title = legend_title)
        plt.savefig("Mantissenvergleich_Laufzeitplot_" + str(algorithm) + ".pdf")
        plt.show()

        print("\nAlle Plots wurden im Arbeitsverzeichnis gespeichert.\n")

    elif choice == "7":
        print("\nIn diesem Programm wird die Approximation der Kreiszahl Pi experimentell untersucht. Zur Approximation werden folgende Algorithmen genutzt: Monte-Carlo-Methode, Leibniz-Reihe, Vietes Produktdarstellung, Chudnovsky-Algorithmus.")
        print("\nBei der Monte-Carlo-Methode wird Pi mithilfe eines Zufallsexperiments geschätzt. Je öfter das Zufallsexperiment wiederholt wird (n), desto genauer ist die Schätzung von Pi.")
        print("\nDie Leibniz-Reihe ist eine Folge von Partialsummen, die im Unendlichen gegen Pi/4 konvergiert. Je größer der Index der berechneten Partialsumme (n), desto genauer die Schätzung von Pi.")
        print("\nVietes Produktdarstellung der Kreiszahl Pi nutzt ein unendliches Produkt, was gegen Pi/2 konvergiert. Je größer der Index des berechneten Partialprodukts (n), desto genauer die Schätzung von Pi.")
        print("\nDer Chudnovsky-Algorithmus basiert auf der Konvergenz einer verallgemeinerten hypergeometrischen Reihe gegen 1/Pi. Je größer der Index der berechneten Partialsumme (n), desto genauer die Schätzung von Pi.")

        print("\nEs werden nun folgende Eingabeparameter gewählt:")
        print("Monte-Carlo-Methode: n = 10^6")
        print("Leibniz-Reihe: n = 10^6")
        print("Vietes Produktdarstellung: n = 10^5")
        print("Chudnovsky-Algorithmus: n = 10^3")

        # Berechnungen
        print("\nBeginn der Berechnungen...")
        data_montecarlo = experiment_pi("montecarlo", 6, precision = 150)
        print("Berechnungen für Monte-Carlo abgeschlossen.")
        data_leibniz = experiment_pi("leibniz", 6, precision = 150)
        print("Berechnungen für Leibniz abgeschlossen.")
        data_viete = experiment_pi("viete", 5, precision = 150)
        print("Berechnungen für Viete abgeschlossen.")
        data_chudnovsky = experiment_pi("chudnovsky", 3, precision = 150)
        print("Berechnungen für Chudnovsky abgeschlossen.")

        # Datensätze zusammenfügen
        data_montecarlo["Algorithmus"] = "montecarlo"
        data_leibniz["Algorithmus"] = "leibniz"
        data_viete["Algorithmus"] = "viete"
        data_chudnovsky["Algorithmus"] = "chudnovsky"
        data = pd.concat([data_montecarlo, data_leibniz, data_viete, data_chudnovsky])

        # Daten abspeichern
        data.to_csv("Minimalbeispiel_Algorithmenvergleich.csv")
        print("Die Ergebnisse wurden in " + "Minimalbeispiel_Algorithmenvergleich.csv im Arbeitsverzeichnis gespeichert.\n")

        # Plots
        # Konvergenzplot
        plot_pi(data_montecarlo, y = "Pi", linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Pi", linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Pi", linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Pi", linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        getcontext().prec = 1010
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        pi = Decimal(pi)
        plt.axhline(y=pi, color="slategrey", label = "$\pi$")
        plt.grid()
        plt.legend()
        plt.savefig('Algorithmenvergleich_Konvergenzplot.pdf')
        plt.show()

        # Fehlerplot
        plot_pi(data_montecarlo, y = "Fehler", linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Fehler", linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Fehler", linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Fehler", linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Minimalbeispiel_Fehlerplot.pdf')
        plt.show()

        # Laufzeitplot
        plot_pi(data_montecarlo, y = "Laufzeit", linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Laufzeit", linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Laufzeit", linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Laufzeit", linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Minimalbeispiel_Laufzeitplot.pdf')
        plt.show()

        # Operationenplot
        plot_pi(data_montecarlo, y = "Operationen", linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Operationen", linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Operationen", linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Operationen", linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Minimalbeispiel_Operationenplot.pdf')
        plt.show()

        # Laufzeit-Fehler-Plot
        plot_pi(data_montecarlo, y = "Laufzeit_Fehler", linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Laufzeit_Fehler", linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Laufzeit_Fehler", linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Laufzeit_Fehler", linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Minimalbeispiel_Laufzeit-Fehler-Plot.pdf')
        plt.show()

        # Mantissenlänge
        print("\nAuch die Mantissenlänge des verwendeten Datentyps hat einen Einfluss auf die Genauigkeit der Ergebnisse.")
        print("Die bisherigen Berechnungen wurden mit einer Mantissenlänge von 150 durchgeführt.")
        print("Je länger die Mantisse des verwendeten Datentyps, desto genauer die Berechnung, aber auch desto länger die Laufzeit.")
        print("Dies wird nachfolgend am Beispiel von Vietes Produktdarstellung demonstriert:\n")

        # Berechnungen mit verschiedenen Mantissenlängen
        precision1 = 50
        precision2 = 100
        precision3 = 150
        precision4 = 200
        precision5 = 250

        data1 = experiment_pi(algorithm = "viete", stop = 5, precision = precision1)
        print("Berechnungen für Mantissenlänge " + str(precision1) + " abgeschlossen.")
        data2 = experiment_pi(algorithm = "viete", stop = 5, precision = precision2)
        print("Berechnungen für Mantissenlänge " + str(precision2) + " abgeschlossen.")
        data3 = experiment_pi(algorithm = "viete", stop = 5, precision = precision3)
        print("Berechnungen für Mantissenlänge " + str(precision3) + " abgeschlossen.")
        data4 = experiment_pi(algorithm = "viete", stop = 5, precision = precision4)
        print("Berechnungen für Mantissenlänge " + str(precision4) + " abgeschlossen.")
        data5 = experiment_pi(algorithm = "viete", stop = 5, precision = precision5)
        print("Berechnungen für Mantissenlänge " + str(precision5) + " abgeschlossen.")

        # Daten mergen
        data1["Mantissenlänge"] = 50
        data2["Mantissenlänge"] = 100
        data3["Mantissenlänge"] = 150
        data4["Mantissenlänge"] = 200
        data5["Mantissenlänge"] = 250
        data = pd.concat([data1, data2, data3, data4, data5])

        # Daten abspeichern
        data.to_csv("Minimalbeispiel_Mantissenvergleich.csv")
        print("Die Ergebnisse wurden in " + "Minimalbeispiel_Mantissenvergleich.csv im Arbeitsverzeichnis gespeichert.\n")

        # Fehlerplot
        plot_pi(data1, y = "Fehler", linecolor = "red", pointcolor = "darkred", label = "Mantissenlänge " + str(precision1))
        plot_pi(data2, y = "Fehler", linecolor = "orange", pointcolor = "darkorange", label = "Mantissenlänge " + str(precision2))
        plot_pi(data3, y = "Fehler", linecolor = "green", pointcolor = "darkgreen", label = "Mantissenlänge " + str(precision3))
        plot_pi(data4, y = "Fehler", linecolor = "blue", pointcolor = "darkblue", label = "Mantissenlänge " + str(precision4))
        plot_pi(data5, y = "Fehler", linecolor = "darkviolet", pointcolor = "purple", label = "Mantissenlänge " + str(precision5))
        plt.legend(title = "Vietes Produktdarstellung")
        plt.savefig('Minimalbeispiel_Mantissenlängen_Fehler.pdf')
        plt.show()

        # Laufzeitplot
        plot_pi(data1, y = "Laufzeit", linecolor = "red", pointcolor = "darkred", label = "Mantissenlänge " + str(precision1))
        plot_pi(data2, y = "Laufzeit", linecolor = "orange", pointcolor = "darkorange", label = "Mantissenlänge " + str(precision2))
        plot_pi(data3, y = "Laufzeit", linecolor = "green", pointcolor = "darkgreen", label = "Mantissenlänge " + str(precision3))
        plot_pi(data4, y = "Laufzeit", linecolor = "blue", pointcolor = "darkblue", label = "Mantissenlänge " + str(precision4))
        plot_pi(data5, y = "Laufzeit", linecolor = "darkviolet", pointcolor = "purple", label = "Mantissenlänge " + str(precision5))
        plt.legend(title = "Vietes Produktdarstellung")
        plt.savefig('Minimalbeispiel_Mantissenlängen_Laufzeit.pdf')
        plt.show()

        print("Alle Abbildungen wurden im Arbeitsverzeichnis gespeichert.")

    elif choice == "0":
        print("Programm beendet.")
        sys.exit()


if __name__ == "__main__":
    main()