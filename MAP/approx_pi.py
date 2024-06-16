import time # Zeitmessung
import random # Zufallszahlen
from decimal import Decimal, getcontext # Datentyp
import matplotlib.pyplot as plt 

def plot_pi(data):
    plt.plot(data["n"], data["Fehler"])
    plt.show()

def decimal_factorial(n):
   """
   Berechnet die Fakultät einer gegebenen Zahl n unter Verwendung des Decimal-Datentyps.
    
   Inputs:
   n (int): Die Zahl, deren Fakultät berechnet werden soll. Muss eine nicht-negative ganze Zahl sein.
    
   Returns:
   Decimal: Die Fakultät der Zahl n als Decimal-Objekt.
   """  
   getcontext().prec = 1010
    
   result = Decimal('1')

   #Berechnung der Fakultät mit Decimal
   for i in range(1, n + 1):
       result *= Decimal(i)

   return result

def error_pi(calculated_pi: Decimal) -> (Decimal):
    
    getcontext().prec = 1000
    
    pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
   
    fehler = Decimal(pi) - calculated_pi
    
    if fehler < Decimal('0'):
        fehler = Decimal('-1') * fehler
    
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

    for k in range(1,tol+1):
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
    partialsumme = Decimal('0')
    operations = Decimal('0')
    start_time=time.time()

    for k in range(tol+1):
        a = Decimal('-1')**Decimal(k)
        b = decimal_factorial(6*k)
        c = Decimal('545140134')*Decimal(k)+Decimal('13591409')
        d = decimal_factorial(3*k)
        e = decimal_factorial(k)**Decimal('3')
        f = Decimal ('640320')**(Decimal(3)*Decimal(k)+Decimal(3/2))
        partialsumme = partialsumme + (a*b*c)/(d*e*f)
        operations += 23
    
    pi_approx = Decimal('1')/(Decimal('12')*partialsumme)
    operations += 3
    
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
    fehler = error_pi(pi_leibniz_approx)
    print(f"Fehler (Leibniz-Reihe): {fehler:.100f} (100 Nachkommastellen)")
    print(f"Natürlicher Logarithmus des Fehlers (Leibniz-Reihe): {fehler.ln():.50f} (50 Nachkommastellen)")

    toleranz = int(input("Bitte den gewünschten Index des Partialproduktes der Viete-Methode eingeben: "))
    pi_viete_approx, viete_ops, viete_time = pi_viete(toleranz)
    print(f"Pi (Viète-Algorithmus): {pi_viete_approx}")
    print(f"Anzahl der Operationen (Viète-Algorithmus): {viete_ops}")
    print(f"Benötigte Zeit (Viète-Algorithmus): {viete_time:.6f} Millisekunden")
    fehler = error_pi(pi_viete_approx)
    print(f"Fehler (Viète-Algorithmus): {fehler:.100f} (100 Nachkommastellen)")
    print(f"Natürlicher Logarithmus des Fehlers (Viète-Algorithmus): {fehler.ln():.50f} (50 Nachkommastellen)")
    
    toleranz = int(input("Bitte den gewünschten Index der Partialsumme der hypergeometrischen Reihe eingeben: "))
    pi_chudnovsky_approx, chudnovsky_ops, chudnovsky_time = pi_chudnovsky(toleranz)
    print(f"Pi (Chudnovsky-Algorithmus:): {pi_chudnovsky_approx}")
    print(f"Anzahl der Operationen (Chudnovsky-Algorithmus): {chudnovsky_ops}")
    print(f"Benötigte Zeit (Chudnovsky-Algorithmus): {chudnovsky_time:.6f} Millisekunden")
    fehler = error_pi(pi_chudnovsky_approx)
    print(f"Fehler (Chudnovsky-Algorithmus): {fehler:.100f} (100 Nachkommastellen)")
    print(f"Natürlicher Logarithmus des Fehlers (Chudnovsky-Algorithmus): {fehler.ln():.50f} (50 Nachkommastellen)")

if __name__ == "__main__":
    main()
