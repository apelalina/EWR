import numpy as np
import time # Zeitmessung
import random # Zufallszahlen
from decimal import Decimal, getcontext # Datentyp

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
    for k in range(tol-1):
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
    for i in range(num_points-1):
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
    for k in range(tol-1):
        a_n = Decimal(np.sqrt(Decimal(2) + a_n))
        pi_approx = pi_approx * Decimal(2) / a_n
        operations += 3  # 1 Quadratwurzel, 1 Addition, 1 Division
    end_time = time.time()

    elapsed_time = (end_time - start_time) * 1000
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

if __name__ == "__main__":
    main()
