"""
In diesem Programm wird die Approximation der Kreiszahl Pi experimentell untersucht. 
Zur Approximation werden folgende Algorithmen genutzt: 
Monte-Carlo-Methode, Leibniz-Reihe, Vietes Produktdarstellung, Chudnovsky-Algorithmus.

pylint 3.1.0
astroid 3.1.0
Python 3.12.4 (tags/v3.12.4:8e8a4ba, Jun  6 2024, 19:30:16) [MSC v.1940 64 bit (AMD64)]
Your code has been rated at 9.93/10
"""

import sys # für Option, das Programm zu beenden
from decimal import Decimal, getcontext # Datentyp
import pandas as pd # Datensätze
import matplotlib.pyplot as plt # Plots
# Algorithmen zur Approximation von Pi:
from approx_pi import pi_leibniz, pi_viete, pi_chudnovsky, pi_montecarlo, error_pi
from py_logspace import py_logspace
from tools_read_save import read_number # pylint: disable=import-error


def experiment_pi(algorithm: str, stop: int, precision = 100):
    """
    Führt ein Experiment zur Approximation der Kreiszahl Pi 
    unter Verwendung eines angegebenen Algorithmus durch.

    Inputs:
    algorithm (str): Algorithmus zur Annäherung von Pi. Optionen: 
                    "montecarlo", "leibniz", "viete", "chudnovsky".
    stop (int): Höchster Eingabeparameter n = 10^stop 
                    (z.B. Index der Partialsumme, Anzahl generierter Punkte, ...)
    precision (int): Mantissenlänge des verwendeten Datentyps (default: 100). 

    Returns:
    pd.DataFrame: Ein Datensatz, der die folgenden Spalten enthält:
        - 'n': 30 verschiedene Eingabeparameter n (z.B. Index der Partialsumme), 
                logarithmisch verteilt zwischen 1 und 10^stop
        - 'Pi': Schätzung von Pi.
        - 'Fehler': Differenz zu einem auf 2000 Nachkommastellen bekannten Pi.
        - 'Operationen': Anzahl der durchgeführten Operationen.
        - 'Laufzeit': Laufzeit in ms für jede Approximation.
    """
    # Fehlermeldung, falls eine ungültige Eingabe aufgerufen wurde
    if algorithm not in ["montecarlo", "leibniz", "viete", "chudnovsky"]:
        raise ValueError("Bitte geben Sie eine der folgenden Optionen als Algorithmus an: "+
                         "montecarlo, leibniz, viete, chudnovsky")

    # Folgende Kriterien sollen erfasst werden:
    indizes = [] # Eingabeparameter n
    pi = [] # Schätzung von Pi
    fehler = [] # Differenz zum wahren Pi
    operations = [] # Anzahl benötigter Operationen
    laufzeiten = [] # Laufzeit in ms

    # Approximation von Pi
    for n in py_logspace(start = 0, stop = stop, num = 30, basis = 10):
        if algorithm == "montecarlo":
            pi_approx, ops, time = pi_montecarlo(n, precision)
        elif algorithm == "leibniz":
            pi_approx, ops, time = pi_leibniz(n, precision)
        elif algorithm == "viete":
            pi_approx, ops, time = pi_viete(n, precision)
        elif algorithm == "chudnovsky":
            pi_approx, ops, time = pi_chudnovsky(n, precision)

        # dabei berechnete Kriterien sammeln
        indizes.append(n)
        pi.append(pi_approx)
        fehler.append(error_pi(pi_approx))
        operations.append(ops)
        laufzeiten.append(time)

    # Berechnete Kriterien zusammenfügen und zurückgeben
    data = pd.DataFrame({
            "n": indizes,
            "Pi": pi,
            "Fehler": fehler,
            "Operationen": operations,
            "Laufzeit": laufzeiten
        })
    return data


def plot_pi(data, y = "Pi", linecolor = "blue", pointcolor = "darkblue", label = ""):
    """
    Plottet verschiedene Metriken der Pi-Annäherung aus einem gegebenen DataFrame.

    Inputs:
    data (pd.DataFrame): Datensatz, der die Daten für die Plots enthält.
    y (str): Die an der y-Achse zu plottende Variable. Optionen:
            - "Pi" (default): Schätzung von Pi in Abhängigkeit vom Eingabeparameter n
            - "Fehler": Differenz zu Pi in Abhängigkeit vom Eingabeparameter n
            - "Laufzeit": Laufzeit in ms in Abhängigkeit vom Eingabeparameter n
            - "Operationen": Anzahl benötigter Operationen in Abhängigkeit vom Eingabeparameter n
            - "Montecarlo": Plottet mehrere Datenreihen, um den stochastischen Charakter der 
                        Monte-Carlo-Methode zu demonstrieren
            - "Laufzeit_Fehler": Differenz zu Pi in Abhängigkeit von Laufzeit in ms
            - "Montecarlo_Standardabweichung": Standardabweichung mehrerer Monte-Carlo-
                        Datenreihen in Abhängigkeit vom Eingabeparameter n
    linecolor (str): Farbe der Linien im Plot. (default: "blue").
    pointcolor (str): Farbe der Punkte im Plot. (default: "darkblue").
    label (str): Legenden-Label für die Punkte in im Plot.

    Returns:
    None
    """
    # Schätzung von Pi in Abhängigkeit vom Eingabeparameter n
    if y == "Pi":
        # nur x-Achse logarithmisch skaliert
        plt.semilogx(data["n"], data["Pi"], color = linecolor)
        plt.plot(data["n"], data["Pi"], color = pointcolor,
                 marker = '.', linestyle = '', label = label)
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Schäzung von $\\pi$")
        plt.grid()
        plt.legend()

    # Differenz zu Pi in Abhängigkeit vom Eingabeparameter n
    if y == "Fehler":
        # doppelt logarithmisch skaliert
        plt.loglog(data["n"], data["Fehler"], color = linecolor)
        plt.plot(data["n"], data["Fehler"], color = pointcolor,
                 marker = '.', linestyle = '', label = label)
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Fehler (Differenz zu $\\pi$)")
        plt.grid()
        plt.legend()

    # Laufzeit in ms in Abhängigkeit vom Eingabeparameter n
    if y == "Laufzeit":
        plt.loglog(data["n"], data["Laufzeit"], color = linecolor)
        plt.plot(data["n"], data["Laufzeit"], color = pointcolor,
                 marker = '.', linestyle = '', label = label)
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Laufzeit in ms")
        plt.grid()
        plt.legend()

    # Anzahl benötigter Operationen in Abhängigkeit vom Eingabeparameter n
    if y == "Operationen":
        plt.loglog(data["n"], data["Operationen"], color = linecolor)
        plt.plot(data["n"], data["Operationen"], color = pointcolor,
                 marker = '.', linestyle = '', label = label)
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("Anzahl der benötigten Operationen")
        plt.grid()
        plt.legend()

    # Plottet mehrere Monte-Carlo-Datenreihen
    if y == "Montecarlo":
        getcontext().prec = 1010
        # Die ersten 1000 Nachkommastellen von Pi
        # pylint: disable=line-too-long
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        # pylint: enable=line-too-long
        pi = Decimal(pi) * Decimal('1')
        plt.scatter(data["n"], data["Pi"], s = 4, color = pointcolor, label = label)
        # "echtes" Pi als Referenz eintragen
        plt.axhline(y=pi, color="red", label = "$\\pi$")
        plt.xlabel("Eingabeparameter n (Anzahl generierter Punkte)")
        plt.ylabel("Schäzung von $\\pi$")
        plt.grid()
        plt.legend(loc='lower right')

    # Differenz zu Pi in Abhängigkeit von Laufzeit in ms
    if y == "Laufzeit_Fehler":
        data_sorted = data.sort_values('Laufzeit')
        plt.loglog(data_sorted["Laufzeit"], data_sorted["Fehler"], color = linecolor)
        plt.plot(data_sorted["Laufzeit"], data_sorted["Fehler"], color = pointcolor,
                 marker = '.', linestyle = 'none', label = label)
        plt.xlabel("Laufzeit in ms")
        plt.ylabel("Differenz zu $\\pi$")
        plt.grid()
        plt.legend()

    # Standardabweichung mehrerer Monte-Carlo-Datenreihen in Abhängigkeit vom Eingabeparameter n
    if y == "Montecarlo_Standardabweichung":
        # Vorbereitung: Standardabweichung berechnen
        grouped = data.groupby('n')
        std_devs = grouped['Pi'].apply(lambda x: float(pd.Series([float(val) for val in x]).std()))
        std_devs_df = std_devs.reset_index(name='Standardabweichung')
        data = data.merge(std_devs_df, on='n')
        # Der Plot selbst:
        plt.figure()
        plt.scatter(data['n'], data['Standardabweichung'], color='darkblue', s = 8,
                    label = "Standardabweichung der Monte-Carlo-Schätzungen")
        plt.xscale('log')
        plt.yscale('log')
        # Achsenbeschriftung manuell setzen:
        plt.yticks([10**i for i in range(-4, 0)])
        plt.xlabel('Eingabeparameter n (Anzahl der Punkte)')
        plt.ylabel('Standardabweichung der Schätzung von $\\pi$')
        plt.grid()
        plt.legend()


def main():
    """
    Hauptfunktion des Programms. 
    Dient der experimentellen Untersuchung der Effizienz und Genauigkeit in der 
    Approximation der Kreiszahl Pi mittels ausgewählter Algorithmen.
    """

    # Nutzereingabe zur Programmsteuerung ----------------------------------------------------------
    print("\nIn diesem Experiment wird die Effizienz und Genauigkeit in der Approximation der "+
          "Kreiszahl Pi mittels ausgewählter Algorithmen untersucht. Bitte wählen Sie eine "+
          "Approximationsmethode:\n")
    print("1. Monte-Carlo-Methode")
    print("2. Leibniz-Reihe")
    print("3. Vietes Produktdarstellung")
    print("4. Chudnovsky-Algorithmus")
    print("5. Alle Algorithmen vergleichen")
    print("6. Mantissenlängen vergleichen")
    print("7. Demonstration eines Minimalbeispiels")
    print("0. Programm beenden")

    # Falls eine falsche Eingabe gemacht wurde, soll die Eingabe wiederholt werden können
    while True:
        choice = input("\nBitte wählen Sie eine Option:\n")
        if choice in ["1", "2", "3", "4", "5", "6", "7", "0"]:
            break
        print("Dies ist keine der angebotenen Optionen.")

    # Monte-Carlo-Methode --------------------------------------------------------------------------
    if choice == "1":
        # einführende Beschreibung
        print("\nApproximation von Pi mit der Monte-Carlo-Methode\n")
        print("Dabei wird Pi mithilfe eines Zufallsexperiments geschätzt. "+
              "Je öfter das Zufallsexperiment wiederholt wird, desto genauer ist die "+
              "Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für "+
              "mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des "+
              "Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für 30 "+
              "Eingabewerte zwischen 1 und 10^k\n")

        # Parametereingabe durch den Nutzer
        stop = read_number("Bitte die Anzahl der Zufallsexperimente für die "+
                           "Monte-Carlo-Methode eingeben: 10^", data_type = int, lower_limit = 0)
        precision = read_number("Mantissenlänge der Zahlendarstellung: ",
                                data_type = int, lower_limit = 1, upper_limit = 2001)

        # Berechnung der Datenreihen (10x)
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

        # 10 Datenreihen berechnen, zusammenfügen und abspeichern
        i = 0
        for df in [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10]:
            i += 1
            df = experiment_pi("montecarlo", stop, precision)
            df["Versuchsreihe"] = i # neue Spalte, damit Versuchsreihen unterscheidbar bleiben
        data = pd.concat([data1, data2, data3, data4, data5, data6, data7, data8, data9, data10])

        data.to_csv("pi_montecarlo_" + str(stop) + ".csv") # Datensatz exportieren
        print("Die Ergebnisse wurden in " + "pi_montecarlo_" + str(stop) +
              ".csv im Arbeitsverzeichnis gespeichert.\n")

        # Betrachtung des stochastischen Charakters von Monte-Carlo
        print("\nDa es sich bei der Monte-Carlo-Methode um ein stochastisches Verfahren handelt, "+
              "wurde das von Ihnen spezifizierte Experiment 10 Mal wiederholt:")
        plot_pi(data, "Montecarlo", label = "Schätzung von $\\pi$ nach Monte-Carlo")
        plt.savefig('Montecarlo_Konvergenzplot.pdf')
        plt.show()
        print("In der Abbildung ist jedoch erkennbar, dass die verschiedenen Durchgänge für große "+
              "n immer ähnlichere Ergebnisse liefern. Dies zeigt sich auch in der Betrachtung der "+
              "Standardabweichungen über die 10 Versuchsreihen:")
        plot_pi(data, y = "Montecarlo_Standardabweichung")
        plt.savefig('MonteCarlo_Standardabweichungen.pdf')
        plt.show()
        print("Deshalb wird nachfolgend zur Übersichtlichkeit nur noch eine einzige "+
              "Datenreihe dargestellt.\n")

        # Fehlerplot
        plot_pi(data1, "Fehler", label = "Monte-Carlo-Methode")
        plt.savefig('Montecarlo_Fehlerplot.pdf')
        plt.show()

        # Laufzeitplot
        plot_pi(data1, "Laufzeit", label="Monte-Carlo-Methode")
        plt.savefig('Montecarlo_Laufzeitplot.pdf')
        plt.show()

        # Operationenplot
        plot_pi(data1, "Operationen", label="Monte-Carlo-Methode")
        plt.savefig('Montecarlo_Operationenplot.pdf')
        plt.show()

        # Laufzeit-Fehler-Plot
        plot_pi(data1, "Laufzeit_Fehler", label="Monte-Carlo-Methode")
        plt.savefig('Montecarlo_Laufzeit_Fehlerplot.pdf')
        plt.show()

        print("\nAlle Plots wurden im Arbeitsverzeichnis gespeichert.\n")

    # Leibniz-Reihe --------------------------------------------------------------------------------
    elif choice == "2":
        # einführende Beschreibung
        print("\nApproximation von Pi mittels der Leibniz-Reihe\n")
        print("Die Leibniz-Reihe ist eine Folge von Partialsummen, die im Unendlichen gegen "+
              "Pi/4 konvergiert. Je größer der Index der berechneten Partialsumme, desto genauer "+
              "die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für "+
              "mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des "+
              "Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für "+
              "30 Eingabewerte zwischen 1 und 10^k\n")

        # Parametereingabe durch den Nutzer
        stop = read_number("Bitte den höchsten Index der Partialsumme der Leibniz-Reihe "+
                           "eingeben: 10^",
                           data_type = int, lower_limit = 0)
        precision = read_number("Mantissenlänge der Zahlendarstellung: ", data_type = int,
                            lower_limit = 1, upper_limit = 2001)

        # Experiment durchführen und Daten abspeichern
        data = experiment_pi("leibniz", stop, precision)
        data.to_csv("pi_leibniz_" + str(stop) + ".csv")
        print("Die Ergebnisse wurden in " + "pi_leibniz_" + str(stop) + ".csv im "+
              "Arbeitsverzeichnis gespeichert.\n")

        # Konvergenzplot
        plot_pi(data, "Pi", label = "$\\pi$ nach Leibniz-Approximation")
        getcontext().prec = 1010
        # Die ersten 1000 Nachkommastellen von Pi
        # pylint: disable=line-too-long
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        # pylint: enable=line-too-long
        pi = Decimal(pi) * Decimal('1')
        plt.axhline(y=pi, color="red", label = "$\\pi$")
        plt.legend()
        plt.savefig('Leibniz_Konvergenzplot.pdf')
        plt.show()

        # Fehlerplot
        plot_pi(data, "Fehler", label = "Leibniz-Approximation")
        plt.savefig('Leibniz_Fehlerplot.pdf')
        plt.show()

        # Laufzeitplot
        plot_pi(data, "Laufzeit", label="Leibniz-Approximation")
        plt.savefig('Leibniz_Laufzeitplot.pdf')
        plt.show()

        # Operationenplot
        plot_pi(data, "Operationen", label="Leibniz-Approximation")
        plt.savefig('Leibniz_Operationenplot.pdf')
        plt.show()

        # Laufzeit-Fehler-Plot
        plot_pi(data, "Laufzeit_Fehler", label="Leibniz-Approximation")
        plt.savefig('Leibniz_Laufzeit_Fehlerplot.pdf')
        plt.show()

        print("\nAlle Plots wurden im Arbeitsverzeichnis gespeichert.\n")

    # Vietes Produktdarstellung --------------------------------------------------------------------
    elif choice == "3":
        # einführende Beschreibung
        print("\nApproximation von Pi mittels Vietes Produktdarstellung\n")
        print("Vietes Produktdarstellung der Kreiszahl Pi nutzt ein unendliches Produkt, was "+
              "gegen Pi/2 konvergiert. Je größer der Index des berechneten Partialprodukts, "+
              "desto genauer die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für "+
              "mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des "+
              "Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für 30 "+
              "Eingabewerte zwischen 1 und 10^k\n")

        # Parametereingabe durch den Nutzer
        stop = read_number("Bitte den höchsten Index des Partialprodukts für Vietes "+
                           "Produktdarstellung eingeben: 10^", data_type = int, lower_limit = 0)
        precision = read_number("Mantissenlänge der Zahlendarstellung: ", data_type = int,
                                lower_limit = 1, upper_limit = 2001)

        # Experiment durchführen und Daten abspeichern
        data = experiment_pi("viete", stop, precision)
        data.to_csv("pi_viete_" + str(stop) + ".csv")
        print("Die Ergebnisse wurden in " + "pi_viete_" + str(stop) + ".csv im "+
              "Arbeitsverzeichnis gespeichert.\n")

        # Konvergenzplot
        plot_pi(data, "Pi", label = "$\\pi$ nach Viete-Approximation")
        getcontext().prec = 1010
        # Die ersten 1000 Nachkommastellen von Pi
        # pylint: disable=line-too-long
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        # pylint: enable=line-too-long
        pi = Decimal(pi) * Decimal('1')
        plt.axhline(y=pi, color="red", label = "$\\pi$")
        plt.legend()
        plt.savefig('Viete_Fehlerplot.pdf')
        plt.show()

        # Fehlerplot
        plot_pi(data, "Fehler", label = "Viete-Approximation")
        plt.savefig('Viete_Fehlerplot.pdf')
        plt.show()

        # Laufzeitplot
        plot_pi(data, "Laufzeit", label="Viete-Approximation")
        plt.savefig('Viete_Laufzeitplot.pdf')
        plt.show()

        # Operationenplot
        plot_pi(data, "Operationen", label="Viete-Approximation")
        plt.savefig('Viete_Operationenplot.pdf')
        plt.show()

        # Laufzeit-Fehler-Plot
        plot_pi(data, "Laufzeit_Fehler", label="Viete-Approximation")
        plt.savefig('Viete_Laufzeit_Fehlerplot.pdf')
        plt.show()

        print("\nAlle Plots wurden im Arbeitsverzeichnis gespeichert.\n")

    # Chudnovsky-Algorithmus -----------------------------------------------------------------------
    elif choice == "4":
        # einführende Beschreibung
        print("\nApproximation von Pi mittels Chudnovsky-Algorithmus\n")
        print("Der Chudnovsky-Algorithmus basiert auf der Konvergenz einer verallgemeinerten "+
              "hypergeometrischen Reihe gegen 1/Pi. Je größer der Index der berechneten "+
              "Partialsumme, desto genauer die Schätzung von Pi.")
        print("In diesem Experiment werden die Laufzeit und die Approximationsgenauigkeit für "+
              "mehrere Eingabewerte verglichen. Zuerst wird der höchste Eingabewert des "+
              "Experiments als Zehnerpotenz (10^k) erwartet. Das Programm approximiert Pi für 30 "+
              "Eingabewerte zwischen 1 und 10^k\n")

        # Parametereingabe durch den Nutzer
        stop = read_number("Bitte den höchsten Index der Partialsumme für den "+
                           "Chudnovsky-Algorithmus eingeben: 10^", data_type = int, lower_limit = 0)
        precision = read_number("Mantissenlänge der Zahlendarstellung: ", data_type = int,
                                lower_limit = 1, upper_limit = 2001)

        # Experiment durchführen und Daten exportieren
        data = experiment_pi("chudnovsky", stop, precision)
        data.to_csv("pi_chudnovsky_" + str(stop) + ".csv")
        print("Die Ergebnisse wurden in " + "pi_chudnovsky_" + str(stop) + ".csv im "+
              "Arbeitsverzeichnis gespeichert.\n")

        # Konvergenzplot
        plot_pi(data, "Pi", label = "$\\pi$ nach Chudnovsky")
        getcontext().prec = 1010
        # Die ersten 1000 Nachkommastellen von Pi
        # pylint: disable=line-too-long
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        # pylint: enable=line-too-long
        pi = Decimal(pi) * Decimal('1')
        plt.axhline(y=pi, color="red", label = "$\\pi$")
        plt.legend()
        plt.savefig('Chudnovsky_Konvergenzplot.pdf')
        plt.show()

        # Fehlerplot
        plot_pi(data, "Fehler", label = "Chudnovsky-Algorithmus")
        plt.savefig('Chudnovsky_Fehlerplot.pdf')
        plt.show()

        # Laufzeitplot
        plot_pi(data, "Laufzeit", label="Chudnovsky-Algorithmus")
        plt.savefig('Chudnovsky_Laufzeitplot.pdf')
        plt.show()

        # Operationenplot
        plot_pi(data, "Operationen", label="Chudnovsky-Algorithmus")
        plt.savefig('Chudnovsky_Operationenplot.pdf')
        plt.show()

        # Laufzeit-Fehler-Plot
        plot_pi(data, "Laufzeit_Fehler", label="Chudnovsky-Algorithmus")
        plt.savefig('Chudnovsky_Laufzeit_Fehlerplot.pdf')
        plt.show()

        print("\nAlle Plots wurden im Arbeitsverzeichnis gespeichert.\n")

    # Vergleich aller Algorithmen ------------------------------------------------------------------
    elif choice == "5":
        print("\nVergleich der Algorithmen: Monte-Carlo-Methode, Leibniz-Reihe, "+
              "Vietes Produktdarstellung, Chudnovsky-Algorithmus \n")

        # Parametereingabe: n für alle Algorithmen
        stop_montecarlo = read_number("Bitte die Anzahl der Zufallsexperimente für die "+
                                      "Monte-Carlo-Methode eingeben: 10^", 
                                      data_type = int, lower_limit = 0)
        stop_leibniz = read_number("Bitte den höchsten Index der Partialsumme der "+
                                   "Leibniz-Reihe eingeben: 10^", 
                                   data_type = int, lower_limit = 0)
        stop_viete = read_number("Bitte den höchsten Index des Partialprodukts für "+
                                 "Vietes Produktdarstellung eingeben: 10^", 
                                 data_type = int, lower_limit = 0)
        stop_chudnovsky = read_number("Bitte den höchsten Index der Partialsumme für den "+
                                      "Chudnovsky-Algorithmus eingeben: 10^", 
                                      data_type = int, lower_limit = 0)

        # Parametereingabe: Mantissenlänge des verwendeten Datentyps
        precision = read_number("Mantissenlänge der Zahlendarstellung: ",
                                data_type = int, lower_limit = 1, upper_limit = 2001)

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
        data = pd.concat([data_montecarlo, data_leibniz, data_viete, data_chudnovsky])

        # Daten abspeichern
        data.to_csv("Algorithmenvergleich_" + str(precision) + ".csv")
        print("Die Ergebnisse wurden in " + "Algorithmenvergleich" + str(precision) +
              ".csv im Arbeitsverzeichnis gespeichert.\n")

        # Konvergenzplot
        plot_pi(data_montecarlo, y = "Pi",
                linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Pi",
                linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Pi",
                linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Pi",
                linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        getcontext().prec = 1010
        # Die ersten 1000 Nachkommastellen von Pi
        # pylint: disable=line-too-long
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        # pylint: enable=line-too-long
        pi = Decimal(pi) * Decimal('1')
        plt.axhline(y=pi, color="slategrey", label = "$\\pi$")
        plt.grid()
        plt.legend()
        plt.savefig('Algorithmenvergleich_Konvergenzplot.pdf')
        plt.show()

        # Fehlerplot
        plot_pi(data_montecarlo, y = "Fehler",
                linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Fehler",
                linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Fehler",
                linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Fehler",
                linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Algorithmenvergleich_Fehlerplot.pdf')
        plt.show()

        # Laufzeitplot
        plot_pi(data_montecarlo, y = "Laufzeit",
                linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Laufzeit",
                linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Laufzeit",
                linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Laufzeit",
                linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Algorithmenvergleich_Laufzeitplot.pdf')
        plt.show()

        # Operationenplot
        plot_pi(data_montecarlo, y = "Operationen",
                linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Operationen",
                linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Operationen",
                linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Operationen",
                linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        # Kurven für O(n) und O(n^2) einfügen
        getcontext().prec = 1010
        x_vec = [1, max(data["n"])]
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
        plot_pi(data_montecarlo, y = "Laufzeit_Fehler",
                linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Laufzeit_Fehler",
                linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Laufzeit_Fehler",
                linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Laufzeit_Fehler",
                linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Algorithmenvergleich_Laufzeit-Fehler-Plot.pdf')
        plt.show()

        # Fehlerplot, logarithmische Skala
        print("Fehlerplot: Für sehr kleine Fehler kann die Achsenskalierung von "+
              "matplotlib fehlerhaft sein. Deshalb wird abschließend noch der Logarithmus "+
              "zur Basis 10 des Fehlers graphisch dargestellt.")
        print("Berechne log10(Fehler), Monte-Carlo.")
        # Logarithmus zur Basis 10 des Fehlers
        for i in range(30):
            data_montecarlo.iloc[i, 2] = Decimal.log10(data_montecarlo.iloc[i, 2])
        print("Berechne log10(Fehler), Leibniz.")
        for i in range(30):
            data_leibniz.iloc[i, 2] = Decimal.log10(data_leibniz.iloc[i, 2])
        print("Berechne log10(Fehler), Viete.")
        for i in range(30):
            data_viete.iloc[i, 2] = Decimal.log10(data_viete.iloc[i, 2])
        print("Berechne log10(Fehler), Chudnovsky.")
        for i in range(30):
            data_chudnovsky.iloc[i, 2] = Decimal.log10(data_chudnovsky.iloc[i, 2])
        # der Plot selbst
        plt.semilogx(data_montecarlo["n"], data_montecarlo["Fehler"], color = "blue")
        plt.plot(data["n"], data["Fehler"],
                 color = "darkblue",   marker = '.', linestyle = '',
                 label = "Monte-Carlo-Methode")
        plt.semilogx(data_leibniz["n"], data_leibniz["Fehler"], color = "green")
        plt.plot(data_leibniz["n"], data_leibniz["Fehler"],
                 color = "darkgreen",   marker = '.', linestyle = '',
                 label = "Leibniz-Reihe")
        plt.semilogx(data_viete["n"], data_viete["Fehler"], color = "red")
        plt.plot(data_viete["n"], data_viete["Fehler"],
                 color = "darkred",   marker = '.', linestyle = '',
                 label = "Vietes Produktdarstellung")
        plt.semilogx(data_chudnovsky["n"], data_chudnovsky["Fehler"], color = "orange")
        plt.plot(data_chudnovsky["n"], data_chudnovsky["Fehler"],
                 color = "darkorange",   marker = '.', linestyle = '',
                 label = "Chudnovsky-Algorithmus")
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("$\\log_{10}$(Fehler)")
        plt.legend()
        plt.grid()
        plt.savefig('Algorithmenvergleich_Fehlerplot_log10.pdf')
        plt.show()

        print("\nAlle Plots wurden im Arbeitsverzeichnis gespeichert.\n")

    # Vergleich verschiedener Mantissenlängen ------------------------------------------------------
    elif choice == "6":

        # Algorithmus auswählen
        print("\nFür welchen Algorithmus möchten Sie verschiedene Mantissenlängen vergleichen?")
        while True:
            algorithm = input("Algorithmus (montecarlo, leibniz, viete, chudnovsky): ")
            if algorithm not in ["montecarlo", "leibniz", "viete", "chudnovsky"]:
                print("Bitte geben Sie eine der folgenden Optionen als Algorithmus an: "+
                      "montecarlo, leibniz, viete, chudnovsky")
            else:
                break

        # Eingabeparameter
        if algorithm == "montecarlo":
            stop = read_number("Bitte die Anzahl der Zufallsexperimente für die "+
                               "Monte-Carlo-Methode eingeben: 10^", 
                               data_type = int, lower_limit = 0)
            legend_title = "Monte-Carlo-Methode"
        elif algorithm == "leibniz":
            stop = read_number("Bitte den höchsten Index der Partialsumme der "+
                               "Leibniz-Reihe eingeben: 10^", 
                               data_type = int, lower_limit = 0)
            legend_title = "Leibniz-Reihe"
        elif algorithm == "viete":
            stop = read_number("Bitte den höchsten Index des Partialprodukts für "+
                               "Vietes Produktdarstellung eingeben: 10^",
                               data_type = int, lower_limit = 0)
            legend_title = "Vietes Produktdarstellung"
        elif algorithm == "chudnovsky":
            stop = read_number("Bitte den höchsten Index der Partialsumme für den "+
                               "Chudnovsky-Algorithmus eingeben: 10^",
                               data_type = int, lower_limit = 0)
            legend_title = "Chudnovsky-Algorithmus"

        # Mantissenlängen
        print("\nBitte geben Sie 5 verschiedene Mantissenlängen an, die sie vergleichen möchten.")
        precision1 = read_number("1. Mantissenlänge der Zahlendarstellung: ",
                                 data_type = int, lower_limit = 1, upper_limit = 2001)
        precision2 = read_number("2. Mantissenlänge der Zahlendarstellung: ",
                                 data_type = int, lower_limit = 1, upper_limit = 2001)
        precision3 = read_number("3. Mantissenlänge der Zahlendarstellung: ",
                                 data_type = int, lower_limit = 1, upper_limit = 2001)
        precision4 = read_number("4. Mantissenlänge der Zahlendarstellung: ",
                                 data_type = int, lower_limit = 1, upper_limit = 2001)
        precision5 = read_number("5. Mantissenlänge der Zahlendarstellung: ",
                                 data_type = int, lower_limit = 1, upper_limit = 2001)
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
        print("Die Ergebnisse wurden in " + "Mantissenvergleich_" + str(algorithm) +
              ".csv im Arbeitsverzeichnis gespeichert.")

        # Plots
        print("\nDie Auswirkungen verschiedener Mantissenlängen sind nun im Fehler- "+
              "und Laufzeitplot erkennbar:")

        # Fehlerplot
        plot_pi(data1, y = "Fehler", linecolor = "red", pointcolor = "darkred",
                label = "Mantissenlänge " + str(precision1))
        plot_pi(data2, y = "Fehler", linecolor = "orange", pointcolor = "darkorange",
                label = "Mantissenlänge " + str(precision2))
        plot_pi(data3, y = "Fehler", linecolor = "green", pointcolor = "darkgreen",
                label = "Mantissenlänge " + str(precision3))
        plot_pi(data4, y = "Fehler", linecolor = "blue", pointcolor = "darkblue",
                label = "Mantissenlänge " + str(precision4))
        plot_pi(data5, y = "Fehler", linecolor = "darkviolet", pointcolor = "purple",
                label = "Mantissenlänge " + str(precision5))
        plt.legend(title = legend_title)
        plt.savefig("Mantissenvergleich_Fehlerplot_" + str(algorithm) + ".pdf")
        plt.show()

        # Laufzeitplot
        plot_pi(data1, y = "Laufzeit", linecolor = "red", pointcolor = "darkred",
                label = "Mantissenlänge " + str(precision1))
        plot_pi(data2, y = "Laufzeit", linecolor = "orange", pointcolor = "darkorange",
                label = "Mantissenlänge " + str(precision2))
        plot_pi(data3, y = "Laufzeit", linecolor = "green", pointcolor = "darkgreen",
                label = "Mantissenlänge " + str(precision3))
        plot_pi(data4, y = "Laufzeit", linecolor = "blue", pointcolor = "darkblue",
                label = "Mantissenlänge " + str(precision4))
        plot_pi(data5, y = "Laufzeit", linecolor = "darkviolet", pointcolor = "purple",
                label = "Mantissenlänge " + str(precision5))
        plt.legend(title = legend_title)
        plt.savefig("Mantissenvergleich_Laufzeitplot_" + str(algorithm) + ".pdf")
        plt.show()

        # Fehlerplot, logarithmische Skala
        print("Fehlerplot: Für sehr kleine Fehler kann die Achsenskalierung von "+
              "matplotlib fehlerhaft sein. Deshalb wird abschließend noch der "+
              "Logarithmus zur Basis 10 des Fehlers graphisch dargestellt.")
        # Logarithmus zur Basis 10 berechnen
        print("Berechne log10(Fehler), Mantissenlänge " + str(precision1))
        for i in range(30):
            data1.iloc[i, 2] = Decimal.log10(data1.iloc[i, 2])
        print("Berechne log10(Fehler), Mantissenlänge " + str(precision2))
        for i in range(30):
            data2.iloc[i, 2] = Decimal.log10(data2.iloc[i, 2])
        print("Berechne log10(Fehler), Mantissenlänge " + str(precision3))
        for i in range(30):
            data3.iloc[i, 2] = Decimal.log10(data3.iloc[i, 2])
        print("Berechne log10(Fehler), Mantissenlänge " + str(precision4))
        for i in range(30):
            data4.iloc[i, 2] = Decimal.log10(data4.iloc[i, 2])
        print("Berechne log10(Fehler), Mantissenlänge " + str(precision5))
        for i in range(30):
            data5.iloc[i, 2] = Decimal.log10(data5.iloc[i, 2])
        # der Plot selbst
        plt.semilogx(data1["n"], data1["Fehler"], color = "red")
        plt.plot(data1["n"], data1["Fehler"], color = "darkred",
                 marker = '.', linestyle = '', label = "Mantissenlänge " + str(precision1))
        plt.semilogx(data2["n"], data2["Fehler"], color = "orange")
        plt.plot(data2["n"], data2["Fehler"], color = "darkorange",
                 marker = '.', linestyle = '', label = "Mantissenlänge " + str(precision2))
        plt.semilogx(data3["n"], data3["Fehler"], color = "green")
        plt.plot(data3["n"], data3["Fehler"], color = "darkgreen",
                 marker = '.', linestyle = '', label = "Mantissenlänge " + str(precision3))
        plt.semilogx(data4["n"], data4["Fehler"], color = "blue")
        plt.plot(data4["n"], data4["Fehler"], color = "darkblue",
                 marker = '.', linestyle = '', label = "Mantissenlänge " + str(precision4))
        plt.semilogx(data5["n"], data5["Fehler"], color = "darkviolet")
        plt.plot(data5["n"], data5["Fehler"], color = "purple",
                 marker = '.', linestyle = '', label = "Mantissenlänge " + str(precision5))
        plt.xlabel("Eingabeparameter n")
        plt.ylabel("$\\log_{10}$(Fehler)")
        plt.legend(title = legend_title)
        plt.grid()
        plt.savefig('Mantissenvergleich_Fehlerplot_log10.pdf')
        plt.show()

        print("\nAlle Plots wurden im Arbeitsverzeichnis gespeichert.\n")

    # Demonstration eines Minimalbeispiels ---------------------------------------------------------
    elif choice == "7":
        # Einführender Text
        # pylint: disable=line-too-long
        print("\nIn diesem Programm wird die Approximation der Kreiszahl Pi experimentell untersucht. Zur Approximation werden folgende Algorithmen genutzt: Monte-Carlo-Methode, Leibniz-Reihe, Vietes Produktdarstellung, Chudnovsky-Algorithmus.")
        print("\nBei der Monte-Carlo-Methode wird Pi mithilfe eines Zufallsexperiments geschätzt. Je öfter das Zufallsexperiment wiederholt wird (n), desto genauer ist die Schätzung von Pi.")
        print("\nDie Leibniz-Reihe ist eine Folge von Partialsummen, die im Unendlichen gegen Pi/4 konvergiert. Je größer der Index der berechneten Partialsumme (n), desto genauer die Schätzung von Pi.")
        print("\nVietes Produktdarstellung der Kreiszahl Pi nutzt ein unendliches Produkt, was gegen Pi/2 konvergiert. Je größer der Index des berechneten Partialprodukts (n), desto genauer die Schätzung von Pi.")
        print("\nDer Chudnovsky-Algorithmus basiert auf der Konvergenz einer verallgemeinerten hypergeometrischen Reihe gegen 1/Pi. Je größer der Index der berechneten Partialsumme (n), desto genauer die Schätzung von Pi.")
        # pylint: disable=line-too-long

        # Eingabeparameter wählen
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
        print("Die Ergebnisse wurden in " +
              "Minimalbeispiel_Algorithmenvergleich.csv im Arbeitsverzeichnis gespeichert.\n")

        # Plots
        # Konvergenzplot
        plot_pi(data_montecarlo, y = "Pi",
                linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Pi",
                linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Pi",
                linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Pi",
                linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        getcontext().prec = 1010
        # Die ersten 1000 Nachkommastellen von Pi
        # pylint: disable=line-too-long
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        # pylint: enable=line-too-long
        pi = Decimal(pi) * Decimal('1')
        plt.axhline(y=pi, color="slategrey", label = "$\\pi$")
        plt.grid()
        plt.legend()
        plt.savefig('Algorithmenvergleich_Konvergenzplot.pdf')
        plt.show()

        # Fehlerplot
        plot_pi(data_montecarlo, y = "Fehler",
                linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Fehler",
                linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Fehler",
                linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Fehler",
                linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Minimalbeispiel_Fehlerplot.pdf')
        plt.show()

        # Laufzeitplot
        plot_pi(data_montecarlo, y = "Laufzeit",
                linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Laufzeit",
                linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Laufzeit",
                linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Laufzeit",
                linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Minimalbeispiel_Laufzeitplot.pdf')
        plt.show()

        # Operationenplot
        plot_pi(data_montecarlo, y = "Operationen",
                linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Operationen",
                linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Operationen",
                linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Operationen",
                linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Minimalbeispiel_Operationenplot.pdf')
        plt.show()

        # Laufzeit-Fehler-Plot
        plot_pi(data_montecarlo, y = "Laufzeit_Fehler",
                linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
        plot_pi(data_leibniz, y = "Laufzeit_Fehler",
                linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
        plot_pi(data_viete, y = "Laufzeit_Fehler",
                linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
        plot_pi(data_chudnovsky, y = "Laufzeit_Fehler",
                linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
        plt.savefig('Minimalbeispiel_Laufzeit-Fehler-Plot.pdf')
        plt.show()

        # Mantissenlänge
        print("\nAuch die Mantissenlänge des verwendeten Datentyps hat einen Einfluss "+
              "auf die Genauigkeit der Ergebnisse.")
        print("Die bisherigen Berechnungen wurden mit einer Mantissenlänge von "+
              "150 durchgeführt.")
        print("Je länger die Mantisse des verwendeten Datentyps, desto genauer die "+
              "Berechnung, aber auch desto länger die Laufzeit.")
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
        print("Die Ergebnisse wurden in " +
              "Minimalbeispiel_Mantissenvergleich.csv im Arbeitsverzeichnis gespeichert.\n")

        # Fehlerplot
        plot_pi(data1, y = "Fehler", linecolor = "red", pointcolor = "darkred",
                label = "Mantissenlänge " + str(precision1))
        plot_pi(data2, y = "Fehler", linecolor = "orange", pointcolor = "darkorange",
                label = "Mantissenlänge " + str(precision2))
        plot_pi(data3, y = "Fehler", linecolor = "green", pointcolor = "darkgreen",
                label = "Mantissenlänge " + str(precision3))
        plot_pi(data4, y = "Fehler", linecolor = "blue", pointcolor = "darkblue",
                label = "Mantissenlänge " + str(precision4))
        plot_pi(data5, y = "Fehler", linecolor = "darkviolet", pointcolor = "purple",
                label = "Mantissenlänge " + str(precision5))
        plt.legend(title = "Vietes Produktdarstellung")
        plt.savefig('Minimalbeispiel_Mantissenlängen_Fehler.pdf')
        plt.show()

        # Laufzeitplot
        plot_pi(data1, y = "Laufzeit", linecolor = "red", pointcolor = "darkred",
                label = "Mantissenlänge " + str(precision1))
        plot_pi(data2, y = "Laufzeit", linecolor = "orange", pointcolor = "darkorange",
                label = "Mantissenlänge " + str(precision2))
        plot_pi(data3, y = "Laufzeit", linecolor = "green", pointcolor = "darkgreen",
                label = "Mantissenlänge " + str(precision3))
        plot_pi(data4, y = "Laufzeit", linecolor = "blue", pointcolor = "darkblue",
                label = "Mantissenlänge " + str(precision4))
        plot_pi(data5, y = "Laufzeit", linecolor = "darkviolet", pointcolor = "purple",
                label = "Mantissenlänge " + str(precision5))
        plt.legend(title = "Vietes Produktdarstellung")
        plt.savefig('Minimalbeispiel_Mantissenlängen_Laufzeit.pdf')
        plt.show()

        print("Alle Abbildungen wurden im Arbeitsverzeichnis gespeichert.")

    # Option Programmende --------------------------------------------------------------------------
    elif choice == "0":
        print("Programm beendet.")
        sys.exit()


if __name__ == "__main__":
    main()
