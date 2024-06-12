import time # Zeitmessung
import random # Zufallszahlen
from decimal import Decimal, getcontext # Datentyp
import numpy as np

def error_pi(calculated_pi: Decimal) -> (Decimal):
    getcontext().prec = 1010
    pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
    fehler = Decimal(pi) - calculated_pi
    if fehler < Decimal('0'):
        return Decimal('-1') * fehler
    else:
        return fehler


def pi_leibniz(tol: int) -> (Decimal, int, float):
    """
    Berechnet eine Näherung von Pi mit der Leibniz-Reihe.

    Inputs:
    tol (int): Index der Partialsumme der Leibniz-Reihe.

    Returns:
    Decimal: Eine Näherung von Pi.
    int: Anzahl der durchgeführten Operationen.
    float: Benötigte Zeit in Millisekunden.
    """
    start_time = time.time()
    getcontext().prec = 50  # Setzt die Präzision für Decimal-Berechnungen
    pi_approx = Decimal('4')
    a_n = Decimal('8') / Decimal('15')
    n = Decimal('1')
    operations = Decimal('1')

    for k in range(tol):
        pi_approx = pi_approx - a_n
        n += Decimal('1')
        a_n = Decimal('8') / (Decimal('16')* Decimal(n) * Decimal(n) - Decimal('1'))
        operations += Decimal('6')
    end_time = time.time()

    elapsed_time = (end_time - start_time) * 1000
    return pi_approx, operations, elapsed_time

def pi_viete(tol: int) -> (Decimal, int, float):
    """
    Berechnet eine Näherung von Pi mit dem Viète-Algorithmus.

    Inputs:
    tol (int): Index des Partialproduktes.

    Returns:
    Decimal: Eine Näherung von Pi.
    int: Anzahl der durchgeführten Operationen.
    float: Benötigte Zeit in Millisekunden.
    """
    start_time = time.time()
    getcontext().prec = 50  # Setzt die Präzision für Decimal-Berechnungen
    a_n = Decimal('2').sqrt()
    pi_approx = Decimal('2') * Decimal('2')/ a_n
    operations = Decimal('3')

    for k in range(1,tol):
        a=Decimal('2') + a_n
        a_n = Decimal(a).sqrt()
        pi_approx = pi_approx * (Decimal(2) / a_n)
        operations += Decimal('4') 
    end_time = time.time()

    elapsed_time = (end_time - start_time) * 1000
    return pi_approx, operations, elapsed_time

def pi_chudnovsky(tol: int) -> (Decimal, int, float):
    """
    Berechnet eine Näherung von Pi mit dem Chudnovsky-Algorithmus.

    Inputs:
    tol (int): Index der Partialsumme der verallgemeinerten, hypergeometrischen Reihe.

    Returns:
    Decimal: Eine Näherung von Pi.
    int: Anzahl der durchgeführten Operationen.
    float: Benötigte Zeit in Millisekunden.
    """ 
    getcontext().prec = 50 # Setzt die Präzision für Decimal-Berechnungen
    operations = 0

def main():
    """
    Hauptfunktion des Programms.
    """
    toleranz = int(input("Bitte den gewünschten Index der Partialsumme der Leibniz-Reihe eingeben: "))
    pi_leibniz_approx, leibniz_ops, leibniz_time = pi_leibniz(toleranz)
    print(f"Pi (Leibniz-Reihe): {pi_leibniz_approx}")
    print(f"Anzahl der Operationen (Leibniz-Reihe): {leibniz_ops}")
    print(f"Benötigte Zeit (Leibniz-Reihe): {leibniz_time:.6f} Millisekunden")
    print(f"Fehler (Leibniz-Reihe): {error_pi(pi_leibniz_approx):.100f} (100 Nachkommastellen)")

    toleranz = int(input("Bitte den gewünschten Index des Partialproduktes der Viete-Methode eingeben: "))
    pi_viete_approx, viete_ops, viete_time = pi_viete(toleranz)
    print(f"Pi (Viète-Algorithmus): {pi_viete_approx}")
    print(f"Anzahl der Operationen (Viète-Algorithmus): {viete_ops}")
    print(f"Benötigte Zeit (Viète-Algorithmus): {viete_time:.6f} Millisekunden")
    print(f"Fehler (Viète-Algorithmus): {error_pi(pi_viete_approx):.100f} (100 Nachkommastellen)")

if __name__ == "__main__":
    main()
