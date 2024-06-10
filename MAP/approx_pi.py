import numpy as np
import time #Zeitmessung
import random #Zufallszahlen
from decimal import Decimal, getcontext #Datentyp

def pi_leibniz(tol: Decimal) -> Decimal:
    """
    Berechnet eine Näherung von Pi mit der Leibniz-Reihe.

    Inputs:
    tol (Decimal): Toleranz oder Genauigkeit für die Berechnung.

    Returns:
    Decimal: Eine Näherung von Pi.
    """
    getcontext().prec = 50  # Setzt die Präzision für Decimal-Berechnungen
    pi_approx = Decimal(4)
    sk = Decimal(8) / Decimal(15)
    k = 1

    while sk >= tol:
        pi_approx = pi_approx - sk
        k += 1
        sk = Decimal(8./(16* k*k - 1))
        
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

    for i in range(num_points):
        
        x = Decimal(random.uniform(-1, 1))
        y = Decimal(random.uniform(-1, 1))
        if x * x + y * y <= 1:
            inside_circle += 1
    return (Decimal(inside_circle) / Decimal(num_points)) * Decimal(4)

def pi_viete(tol: Decimal) -> Decimal:
    """
    Berechnet eine Näherung von Pi mit dem Viète-Algorithmus.

    Inputs:
    tol (Decimal): Toleranz oder Genauigkeit für die Berechnung.

    Returns:
    Decimal: Eine Näherung von Pi.
    """
    getcontext().prec = 50  # Setzt die Präzision für Decimal-Berechnungen
    a_n = Decimal(np.sqrt(2))
    pi_approx = Decimal(2) / a_n
    k = 1

    for k in range (tol):
        a_n = np.sqrt((Decimal(2) + a_n))
        pi_approx = pi_approx * Decimal(2) / a_n

    return pi_approx


def main():
    """
    Hauptfunktion des Programms.
    """
    toleranz = Decimal(input("Bitte die gewünschte Genauigkeit eingeben: "))
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
