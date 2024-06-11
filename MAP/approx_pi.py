import numpy as np
import time #Zeitmessung
import random #Zufallszahlen
from decimal import Decimal, getcontext #Datentyp

def pi_leibniz(tol: int) -> Decimal:

    """
    Berechnet eine Näherung von Pi mit der Leibniz-Reihe.

    Inputs:
    tol (int): Toleranz oder Genauigkeit für die Berechnung.

    Returns:
    Decimal: Eine Näherung von Pi.
    """

    getcontext().prec = 50  # Setzt die Präzision für Decimal-Berechnungen
    pi_approx = Decimal(4)
    a_n = Decimal(8) / Decimal(15)
    n = 1

    for k in range(tol-1):
        pi_approx = pi_approx - a_n
        n += 1
        a_n = Decimal(8)/Decimal(16* n*n - 1)
        
    return pi_approx

def pi_montecarlo(num_points: int) -> Decimal:
 
    """
    Berechnet eine Näherung von Pi mit der Monte-Carlo-Methode.

    Inputs:
    num_points (int): Anzahl der zufällig generierten Punkte.

    Returns:
    Decimal: Eine Näherung von Pi.
    """
 
    getcontext().prec = 50  # Setzt die Präzision für Decimal-Berechnungen

    inside_circle = 0

    for i in range(num_points-1):
        
        x = Decimal(random.uniform(-1, 1))
        y = Decimal(random.uniform(-1, 1))
        if x * x + y * y <= 1:
            inside_circle += 1
    return (Decimal(inside_circle /num_points)) * Decimal(4)

def pi_viete(tol: int) -> Decimal:

    """
    Berechnet eine Näherung von Pi mit dem Viète-Algorithmus.

    Inputs:
    tol (int): Toleranz oder Genauigkeit für die Berechnung.

    Returns:
    Decimal: Eine Näherung von Pi.
    """

    getcontext().prec = 50 # Setzt die Präzision für Decimal-Berechnungen
    a_n = Decimal(np.sqrt(2))
    pi_approx = Decimal(2) * Decimal(2/a_n)

    for k in range (tol-1):
        a_n = Decimal(np.sqrt(Decimal(2) + a_n))
        pi_approx = pi_approx * Decimal(2) / a_n

    return pi_approx


def main():
    """
    Hauptfunktion des Programms.
    """
    toleranz = int(input("Bitte die gewünschte Genauigkeit eingeben: "))
    pi_leibniz_approx = pi_leibniz(toleranz)
    print(f"Pi (Leibniz-Reihe): {pi_leibniz_approx}")

    num_points = int(input("Bitte die Anzahl der Punkte für die Monte-Carlo-Methode eingeben: "))
    pi_montecarlo_approx = pi_montecarlo(num_points)
    print(f"Pi (Monte-Carlo-Methode): {pi_montecarlo_approx}")
    
    toleranz = int(input("Bitte die gewünschte Genauigkeit eingeben: "))
    pi_viete_approx = pi_viete(toleranz)
    print(f"Pi (Viète-Algorithmus): {pi_viete_approx}")

if __name__ == "__main__":
    main()
