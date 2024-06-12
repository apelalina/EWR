import time # Zeitmessung
import random # Zufallszahlen
from decimal import Decimal, getcontext # Datentyp
import numpy as np

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
    pi_approx = Decimal('4')
    a_n = Decimal('8') / Decimal('15')
    n = Decimal('1')
    operations = Decimal('1')

    start_time = time.time()
    for k in range(1, tol):
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
    getcontext().prec = 50  # Setzt die Präzision für Decimal-Berechnungen
    a_n = Decimal(np.sqrt(2))
    pi_approx = Decimal(2) * Decimal(2 / a_n)
    operations = 2  # 1 Quadratwurzel, 1 Division, 1 Multiplikation

    start_time = time.time()
    for k in range(1,tol):
        a_n = Decimal((Decimal(2).sqrt() + a_n))
        pi_approx = pi_approx * Decimal(2) / a_n
        operations += 3  # 1 Quadratwurzel, 1 Addition, 1 Division
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
    s=12
    a_n=Decimal((13591409)/Decimal(640320**Decimal(3/2)))
    operations += 3
    for k in range(1,tol): 
        a_n = a_n + Decimal(((-1)**k) * (6*k) * (545140134*k + 13591409))/Decimal()
    
    
    
    
def main():
    """
    Hauptfunktion des Programms.
    """
    toleranz = int(input("Bitte den gewünschten Index der Partialsumme der Leibniz-Reihe eingeben: "))
    pi_leibniz_approx, leibniz_ops, leibniz_time = pi_leibniz(toleranz)
    print(f"Pi (Leibniz-Reihe): {pi_leibniz_approx}")
    print(f"Anzahl der Operationen (Leibniz-Reihe): {leibniz_ops}")
    print(f"Benötigte Zeit (Leibniz-Reihe): {leibniz_time:.6f} Millisekunden")

    num_points = int(input("Bitte die Anzahl der Punkte für die Monte-Carlo-Methode eingeben: "))
    pi_montecarlo_approx, montecarlo_ops, montecarlo_time = pi_montecarlo(num_points)
    print(f"Pi (Monte-Carlo-Methode): {pi_montecarlo_approx}")
    print(f"Anzahl der Operationen (Monte-Carlo-Methode): {montecarlo_ops}")
    print(f"Benötigte Zeit (Monte-Carlo-Methode): {montecarlo_time:.6f} Millisekunden")

    toleranz = int(input("Bitte den gewünschten Index des Partialproduktes der Viete-Methode eingeben: "))
    pi_viete_approx, viete_ops, viete_time = pi_viete(toleranz)
    print(f"Pi (Viète-Algorithmus): {pi_viete_approx}")
    print(f"Anzahl der Operationen (Viète-Algorithmus): {viete_ops}")
    print(f"Benötigte Zeit (Viète-Algorithmus): {viete_time:.6f} Millisekunden")

    toleranz = int(input("Bitte die gewünschte Anzahl der Schleifendurchläufe eingeben: "))
    pi_gauss_legendre_approx, gauss_legendre_ops, gauss_legendre_time = pi_gausslegendre(toleranz)
    print(f"Pi (Gauss-Legendre-Algorithmus): {pi_gauss_legendre_approx}")
    print(f"Anzahl der Operationen (Gauss-Legendre-Algorithmus): {gauss_legendre_ops}")
    print(f"Benötigte Zeit (Gauss-Legendre-Algorithmus): {gauss_legendre_time:.6f} Millisekunden")

if __name__ == "__main__":
    main()
