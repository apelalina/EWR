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
        getcontext().prec = 1010
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        pi = Decimal(pi) * Decimal('1')
        plt.semilogx(data["n"], data["Pi"], color = linecolor)
        plt.plot(data["n"], data["Pi"], color = pointcolor,   marker = '.', linestyle = '', label = label)
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Schäzung von $\pi$")
        plt.axhline(y=pi, color="red", label = "$\pi$")
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
    print("\nIn diesem Experiment wird die Approximation der Kreiszahl Pi mittels verschiedener Methoden untersucht. Bitte wählen Sie eine Approximationsmethode:\n")
    print("1. Monte-Carlo-Methode")
    print("2. Leibniz-Reihe")
    print("3. Vietas Produktdarstellung")
    print("4. Chudnovsky-Algorithmus")
    print("5. Alle Algorithmen vergleichen")
    print("6. Mantissenlängen vergleichen")
    print("7. Demonstration eines Minimalbeispiels")
    print("0. Programm beenden")
    choice = input("\nBitte wählen Sie eine Option:\n")

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

        data = pd.concat([data1, data2, data3, data4, data5, data6, data7, data8, data9, data10])

        data1.to_csv("pi_montecarlo_" + str(stop) + ".csv")
        print("Die Ergebnisse wurden in " + "pi_montecarlo_" + str(stop) + ".csv im Arbeitsverzeichnis gespeichert.\n")

        print("\nDa es sich bei der Monte-Carlo-Methode um ein stochastisches Verfahren handelt, wurde das von Ihnen spezifizierte Experiment 10 Mal wiederholt:")
        
        plot_pi(data, "Montecarlo", label = "Schätzung nach Monte-Carlo")
        plt.savefig('Montecarlo_Konvergenzplot.pdf')
        plt.show()

        print("In der Abbildung ist jedoch erkennbar, dass die verschiedenen Durchgänge für große n immer ähnlichere Ergebnisse liefern. Deshalb wird nachfolgend zur Übersichtlichkeit nur noch eine einzige Datenreihe dargestellt.\n")

        plot_pi(data1, "Fehler", label = "Monte-Carlo-Schätzung")
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

    if choice == "2":
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
        pi = Decimal(pi) * Decimal('1')
        plt.axhline(y=pi, color="red", label = "$\pi$")
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

    if choice == "3":
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
        pi = Decimal(pi) * Decimal('1')
        plt.axhline(y=pi, color="red", label = "$\pi$")
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

    if choice == "4":
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
        pi = Decimal(pi) * Decimal('1')
        plt.axhline(y=pi, color="red", label = "$\pi$")
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


    if choice == "5":
        stop_montecarlo = read_number("Bitte die Anzahl der Zufallsexperimente für die Monte-Carlo-Methode eingeben: 10^", data_type = int, lower_limit = 0)
        stop_leibniz = read_number("Bitte den höchsten Index der Partialsumme der Leibniz-Reihe eingeben: 10^", data_type = int, lower_limit = 0)
        stop_viete = read_number("Bitte den höchsten Index des Partialprodukts für Vietas Produktdarstellung eingeben: 10^", data_type = int, lower_limit = 0)
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

        # Datensätze zusammenfügen
        data_montecarlo["Algorithmus"] = "montecarlo"
        data_leibniz["Algorithmus"] = "leibniz"
        data_viete["Algorithmus"] = "viete"
        data_chudnovsky["Algorithmus"] = "chudnovsky"
        data = pd.concat(data_montecarlo, data_leibniz, data_viete, data_chudnovsky)

        # Daten abspeichern
        data.to_csv("Algorithmenvergleich" + str(precision) + ".csv")
        print("Die Ergebnisse wurden in " + "Algorithmenvergleich" + str(precision) + ".csv im Arbeitsverzeichnis gespeichert.\n")

        # Konvergenzplot
        plot_pi(data_montecarlo, y = "Pi", linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Pi", linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Pi", linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Pi", linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        getcontext().prec = 1010
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        pi = Decimal(pi)
        plt.axhline(y=pi, color="purple", label = "$\pi$")
        plt.savefig('Vergleich_Konvergenzplot.pdf')
        plt.show()



        # Fehlerplot
        plt.loglog(data_montecarlo["n"], data_montecarlo["Fehler"], color = 'blue', label = "Monte-Carlo")
        plt.plot(data_montecarlo["n"], data_montecarlo["Fehler"], color = 'darkblue',   marker = '.', linestyle = '') # Datenpunkte
        plt.loglog(data_leibniz["n"], data_leibniz["Fehler"], color = 'green', label = "Leibniz")
        plt.plot(data_leibniz["n"], data_leibniz["Fehler"], color = 'darkgreen',   marker = '.', linestyle = '') # Datenpunkte
        plt.loglog(data_viete["n"], data_viete["Fehler"], color = 'red', label = "Viete")
        plt.plot(data_viete["n"], data_viete["Fehler"], color = 'darkred',   marker = '.', linestyle = '') # Datenpunkte
        plt.loglog(data_chudnovsky["n"], data_chudnovsky["Fehler"], color = 'orange', label = "Chudnovsky")
        plt.plot(data_chudnovsky["n"], data_chudnovsky["Fehler"], color = 'darkorange',   marker = '.', linestyle = '') # Datenpunkte
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Differenz zu $\pi$")
        plt.legend()
        plt.grid()
        plt.savefig('Fehlerplot.pdf')
        plt.show()


        # Konvergenz-Plot
        getcontext().prec = 1010
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        pi = Decimal(pi)
        plt.semilogx(data_montecarlo["n"], data_montecarlo["Pi"], color = 'blue', label = "Monte-Carlo")
        plt.plot(data_montecarlo["n"], data_montecarlo["Pi"], color = 'darkblue',   marker = '.', linestyle = '') # Datenpunkte
        plt.semilogx(data_leibniz["n"], data_leibniz["Pi"], color = 'green', label = "Leibniz")
        plt.plot(data_leibniz["n"], data_leibniz["Pi"], color = 'darkgreen',   marker = '.', linestyle = '') # Datenpunkte
        plt.semilogx(data_viete["n"], data_viete["Pi"], color = 'red', label = "Viete")
        plt.plot(data_viete["n"], data_viete["Pi"], color = 'darkred',   marker = '.', linestyle = '') # Datenpunkte
        plt.semilogx(data_chudnovsky["n"], data_chudnovsky["Pi"], color = 'orange', label = "Chudnovsky")
        plt.plot(data_chudnovsky["n"], data_chudnovsky["Pi"], color = 'darkorange',   marker = '.', linestyle = '') # Datenpunkte
        plt.axhline(y=pi, color="purple", label = "$\pi$")
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Schätzung von $\pi$")
        plt.legend()
        plt.grid()
        plt.savefig('Konvergenzplot.pdf')
        plt.show()

        # Laufzeit
        plt.loglog(data_montecarlo["n"], data_montecarlo["Laufzeit"], color = 'blue', label = "Monte-Carlo")
        plt.plot(data_montecarlo["n"], data_montecarlo["Laufzeit"], color = 'darkblue',   marker = '.', linestyle = '') # Datenpunkte
        plt.loglog(data_leibniz["n"], data_leibniz["Laufzeit"], color = 'green', label = "Leibniz")
        plt.plot(data_leibniz["n"], data_leibniz["Laufzeit"], color = 'darkgreen',   marker = '.', linestyle = '') # Datenpunkte
        plt.loglog(data_viete["n"], data_viete["Laufzeit"], color = 'red', label = "Viete")
        plt.plot(data_viete["n"], data_viete["Laufzeit"], color = 'darkred',   marker = '.', linestyle = '') # Datenpunkte
        plt.loglog(data_chudnovsky["n"], data_chudnovsky["Laufzeit"], color = 'orange', label = "Chudnovsky")
        plt.plot(data_chudnovsky["n"], data_chudnovsky["Laufzeit"], color = 'darkorange',   marker = '.', linestyle = '') # Datenpunkte
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Laufzeit in ms")
        plt.legend()
        plt.grid()
        plt.savefig('Laufzeitplot.pdf')
        plt.show()

        # Anzahl Operationen
        plt.loglog(data_montecarlo["n"], data_montecarlo["Operationen"], color = 'blue', label = "Monte-Carlo")
        plt.plot(data_montecarlo["n"], data_montecarlo["Operationen"], color = 'darkblue',   marker = '.', linestyle = '') # Datenpunkte
        plt.loglog(data_leibniz["n"], data_leibniz["Operationen"], color = 'green', label = "Leibniz")
        plt.plot(data_leibniz["n"], data_leibniz["Operationen"], color = 'darkgreen',   marker = '.', linestyle = '') # Datenpunkte
        plt.loglog(data_viete["n"], data_viete["Operationen"], color = 'red', label = "Viete")
        plt.plot(data_viete["n"], data_viete["Operationen"], color = 'darkred',   marker = '.', linestyle = '') # Datenpunkte
        plt.loglog(data_chudnovsky["n"], data_chudnovsky["Operationen"], color = 'orange', label = "Chudnovsky")
        plt.plot(data_chudnovsky["n"], data_chudnovsky["Operationen"], color = 'darkorange',   marker = '.', linestyle = '') # Datenpunkte
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Anzahl der Operationen")
        plt.legend()
        plt.grid()
        plt.savefig('Operationenplot.pdf')
        plt.show()

    if choice == "0":
        print("Programm beendet.")
        sys.exit()



if __name__ == "__main__":
    main()