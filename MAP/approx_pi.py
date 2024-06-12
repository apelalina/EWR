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
    getcontext().prec = 50  # Setzt die Präzision für Decimal-Berechnungen
    pi_approx = Decimal(4)
    a_n = Decimal(8) / Decimal(15)
    n = 1
    operations = 0

    start_time = time.time()
    for k in range(1, tol):
        pi_approx = pi_approx - a_n
        n += 1
        a_n = Decimal(8)/Decimal(16 * n * n - 1)
        operations += 3  # 1 Subtraktion, 1 Division, 1 Multiplikation
    end_time = time.time()

    elapsed_time = (end_time - start_time) * 1000
    return pi_approx, operations, elapsed_time

def pi_montecarlo(num_points: int) -> (Decimal, int, float):
    """
    Berechnet eine Näherung von Pi mit der Monte-Carlo-Methode.

    Inputs:
    num_points (int): Anzahl der zufällig generierten Punkte.

    Returns:
    Decimal: Eine Näherung von Pi.
    int: Anzahl der durchgeführten Operationen.
    float: Benötigte Zeit in Millisekunden.
    """
    getcontext().prec = 50  # Setzt die Präzision für Decimal-Berechnungen

    inside_circle = 0
    operations = 0

    start_time = time.time()
    for i in range(1, num_points):
        x = Decimal(random.uniform(-1, 1))
        y = Decimal(random.uniform(-1, 1))
        if x * x + y * y <= 1:
            inside_circle += 1
        operations += 3  # 2 Multiplikationen, 1 Addition

    pi_approx = (Decimal(inside_circle) / Decimal(num_points)) * Decimal(4)
    operations += 2  # 1 Division, 1 Multiplikation

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
    getcontext().prec = 50  # Setzt die Präzision für Decimal-Berechnungen
    a_n = Decimal(np.sqrt(2))
    pi_approx = Decimal(2) * Decimal(2 / a_n)
    operations = 2  # 1 Quadratwurzel, 1 Division, 1 Multiplikation

    start_time = time.time()
    for k in range(1,tol):
        a_n = Decimal(np.sqrt(Decimal(2) + a_n))
        pi_approx = pi_approx * Decimal(2) / a_n
        operations += 3  # 1 Quadratwurzel, 1 Addition, 1 Division
    end_time = time.time()

    elapsed_time = (end_time - start_time) * 1000
    return pi_approx, operations, elapsed_time

def pi_gausslegendre(tol: int) -> (Decimal, int, float):
    """
    Berechnet eine Näherung von Pi mit dem Gauss-Legendre Algorithmus.

    Inputs:
    tol (int): Anzahl der Schleifendurchläufe.

    Returns:
    Decimal: Eine Näherung von Pi.
    int: Anzahl der durchgeführten Operationen.
    float: Benötigte Zeit in Millisekunden.
    """ 
    getcontext().prec = 50  # Setzt die Präzision für Decimal-Berechnungen
    operations = 0
    a_n = Decimal(1)
    b_n = Decimal(1/Decimal(np.sqrt(2)))
    t_n = Decimal(1/4)
    p_n = Decimal(1)

    start_time = time.time()
    for k in range(1,tol):
        a_N = Decimal((a_n+b_n)/2)
        b_n = Decimal(np.sqrt(a_n*b_n))
        t_n = t_n-p_n*Decimal(np.square(a_n-a_N))
        a_n = a_N
        p_n = Decimal(2*p_n)
        pi_approx = Decimal(Decimal(np.square(a_n+b_n))/Decimal(4*t_n))
        operations += 13  # 4 Additionen/Subtraktionen, 6 Multiplikationen, 2 Division, 1 Quadratwurzel
    end_time = time.time()

    elapsed_time = (end_time-start_time) * 1000
    return pi_approx, operations, elapsed_time



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

    num_points = int(input("Bitte die Anzahl der Punkte für die Monte-Carlo-Methode eingeben: "))
    pi_montecarlo_approx, montecarlo_ops, montecarlo_time = pi_montecarlo(num_points)
    print(f"Pi (Monte-Carlo-Methode): {pi_montecarlo_approx}")
    print(f"Anzahl der Operationen (Monte-Carlo-Methode): {montecarlo_ops}")
    print(f"Benötigte Zeit (Monte-Carlo-Methode): {montecarlo_time:.6f} Millisekunden")
    print(f"Fehler (Monte-Carlo-Methode): {error_pi(pi_montecarlo_approx):.100f} (100 Nachkommastellen)")

    toleranz = int(input("Bitte den gewünschten Index des Partialproduktes der Viete-Methode eingeben: "))
    pi_viete_approx, viete_ops, viete_time = pi_viete(toleranz)
    print(f"Pi (Viète-Algorithmus): {pi_viete_approx}")
    print(f"Anzahl der Operationen (Viète-Algorithmus): {viete_ops}")
    print(f"Benötigte Zeit (Viète-Algorithmus): {viete_time:.6f} Millisekunden")
    print(f"Fehler (Viète-Algorithmus): {error_pi(pi_viete_approx):.100f} (100 Nachkommastellen)")

    toleranz = int(input("Bitte die gewünschte Anzahl der Schleifendurchläufe eingeben: "))
    pi_gauss_legendre_approx, gauss_legendre_ops, gauss_legendre_time = pi_gausslegendre(toleranz)
    print(f"Pi (Gauss-Legendre-Algorithmus): {pi_gauss_legendre_approx}")
    print(f"Anzahl der Operationen (Gauss-Legendre-Algorithmus): {gauss_legendre_ops}")
    print(f"Benötigte Zeit (Gauss-Legendre-Algorithmus): {gauss_legendre_time:.6f} Millisekunden")
    print(f"Fehler (Gauss-Legendre-Algorithmus): {error_pi(pi_gauss_legendre_approx):.100f} (100 Nachkommastellen)")

if __name__ == "__main__":
    main()
