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
        plt.semilogx(data["n"], data["Pi"], color = linecolor, label = label)
        plt.plot(data["n"], data["Pi"], color = pointcolor,   marker = '.', linestyle = '')
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Schäzung von $\pi$")
        plt.axhline(y=pi, color="red", label = "$\pi$")
        plt.grid()
        plt.legend()

    if y == "Fehler":
        plt.loglog(data["n"], data["Fehler"], color = linecolor, label = label)
        plt.plot(data["n"], data["Fehler"], color = linecolor,   marker = '.', linestyle = '') # Datenpunkte mit Linien
        plt.xlabel("Index der Partialsumme")
        plt.ylabel("Fehler (Differenz zu $\pi$)")
        plt.grid()
        plt.legend()

    if y == "Laufzeit":
        plt.loglog(data["n"], data["Laufzeit"])
        plt.plot(data["n"], data["Laufzeit"], color = 'darkblue',   marker = '.', linestyle = '') # Datenpunkte mit Linien
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Laufzeit in ms")
        plt.grid()
        plt.legend()

    if y == "Operationen":
        plt.loglog(data["n"], data["Operationen"])
        plt.plot(data["n"], data["Operationen"], color = 'darkblue',   marker = '.', linestyle = '') # Datenpunkte mit Linien
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Anzahl der benötigten Operationen")
        plt.grid()
        plt.legend()
    
    if y == "Montecarlo":
        getcontext().prec = 1010
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        pi = Decimal(pi) * Decimal('1')
        plt.scatter(data["n"], data["Pi"], s = 4, color = "darkblue", label = "Schätzung von $\pi$ nach Monte-Carlo")
        plt.axhline(y=pi, color="red", label = "$\pi$")
        plt.xlabel("Eingabeparameter n (Anzahl generierter Punkte)")
        plt.ylabel("Schäzung von $\pi$")
        plt.grid()
        plt.legend(loc='lower right')
    
    if y == "Laufzeit_Fehler":
        data_sorted = data.sort_values('Laufzeit')
        plt.loglog(data_sorted["Laufzeit"], data_sorted["Fehler"])
        plt.plot(data_sorted["Laufzeit"], data_sorted["Fehler"], color = 'darkblue',   marker = '.', linestyle = 'none')
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

        print("\nDa es sich bei der Monte-Carlo-Methode um ein stochastisches Verfahren handelt, wurde das von Ihnen spezifizierte Experiment 10 Mal wiederholt.")
        
        plot_pi(data, "Montecarlo")
        plt.savefig('Konvergenzplot_MonteCarlo.pdf')
        plt.show()

        print("In der Abbildung ist jedoch erkennbar, dass die verschiedenen Durchgänge für große n immer ähnlichere Ergebnisse liefern. Deshalb wird nachfolgend zur Übersichtlichkeit nur noch eine einzige Datenreihe dargestellt.\n")

        plot_pi(data1, "Fehler")
        plt.savefig('Fehlerplot_MonteCarlo.pdf')
        plt.show()

        plot_pi(data1, "Laufzeit")
        plt.savefig('Laufzeitplot_MonteCarlo.pdf')
        plt.show()

        plot_pi(data1, "Operationen")
        plt.savefig('MonteCarlo_Operationenplot.pdf')
        plt.show()

        plot_pi(data1, "Laufzeit_Fehler")
        plt.savefig('MonteCarlo_Laufzeitfehlerplot.pdf')
        plt.show()

        print("\nAlle Plots wurden im Arbeitsverzeichnis gespeichert.\n")




    if choice == "2":
        print("\nApproximation von Pi mittels der Leibniz-Reihe\n")
        print("Die Leibniz-Reihe ist eine Folge von Partialsummen, die im Unendlichen gegen Pi konvergiert. Je größer der Index der berechneten Partialsumme, desto genauer die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für 20 Eingabewerte zwischen 1 und 10^k\n")

        stop = read_number("Bitte den höchsten Index der Partialsumme der Leibniz-Reihe eingeben: 10^", data_type = int, lower_limit = 0)
        
        print("\nDie Approximation von Pi mit der Leibniz-Reihe ergab folgende Ergebnisse:") 
        data = experiment_leibniz(stop)

        plot_pi(data, "Pi")
        plt.show()


    if choice == "3":
        print("\nApproximation von Pi mittels Vietas Produktdarstellung\n")
        print("Vietas Produktdarstellung der Kreiszahl Pi nutzt ein unendliches Produkt, was gegen Pi konvergiert. Je größer der Index des berechneten Partialprodukts, desto genauer die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für 20 Eingabewerte zwischen 1 und 10^k\n")

        stop = read_number("Bitte den höchsten Index des Partialprodukts für Vietas Produktdarstellung eingeben: 10^", data_type = int, lower_limit = 0)
        
        print("\nDie Approximation von Pi mittels Vietas Produktdarstellung ergab folgende Ergebnisse:")    
        data = experiment_viete(stop)
        print(data)

        plot_pi(data, "Pi")


    if choice == "4":
        print("\nApproximation von Pi mittels Chudnovsky-Algorithmus\n")
        print("Der Chudnovsky-Algorithmus basiert auf der Konvergenz einer verallgemeinerten hypergeometrischen Reihe gegen Pi/4. Je größer der Index der berechneten Partialsumme, desto genauer die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für 20 Eingabewerte zwischen 1 und 10^k\n")

        stop = read_number("Bitte den höchsten Index der Partialsumme für den Chudnovsky-Algorithmus eingeben: 10^", data_type = int, lower_limit = 0)

        print("\nDie Approximation von Pi mittels Vietas Produktdarstellung ergab folgende Ergebnisse:")    
        data = experiment_chudnovsky(stop)
        print(data)

        plot_pi(data, "Pi")


    if choice == "5":
        stop_montecarlo = read_number("Bitte die Anzahl der Zufallsexperimente für die Monte-Carlo-Methode eingeben: 2^", data_type = int, lower_limit = 0)
        stop_leibniz = read_number("Bitte den höchsten Index der Partialsumme der Leibniz-Reihe eingeben: 10^", data_type = int, lower_limit = 0)
        stop_viete = read_number("Bitte den höchsten Index des Partialprodukts für Vietas Produktdarstellung eingeben: 10^", data_type = int, lower_limit = 0)
        stop_chudnovsky = read_number("Bitte den höchsten Index der Partialsumme für den Chudnovsky-Algorithmus eingeben: 10^", data_type = int, lower_limit = 0)

        precision = read_number("Mantissenlänge der Zahlendarstellung: ", data_type = int, lower_limit = 1, upper_limit = 1000)

        data_montecarlo = experiment_montecarlo(stop_montecarlo, precision)
        print(data_montecarlo)
        data_leibniz = experiment_leibniz(stop_leibniz, precision)
        print(data_leibniz)
        data_viete = experiment_viete(stop_viete, precision)
        print(data_viete)
        data_chudnovsky = experiment_chudnovsky(stop_chudnovsky, precision)
        print(data_chudnovsky)

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