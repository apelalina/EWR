import time # Zeitmessung
import random # Zufallszahlen
from decimal import Decimal, getcontext # Datentyp
import matplotlib.pyplot as plt 
    
def plot_pi(data, y = "Fehler"):

    if y == "Fehler":
        plt.loglog(data["n"], data["Fehler"])
        plt.plot(data["n"], data["Fehler"], color = 'darkblue',   marker = '.', linestyle = '') # Datenpunkte
        plt.xlabel("Index der Partialsumme")
        plt.ylabel("Differenz zu $\pi$")

    if y == "Pi":
        getcontext().prec = 1010
        pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
        pi = Decimal(pi) * Decimal('1')

        plt.semilogx(data["n"], data["Pi"])
        plt.plot(data["n"], data["Pi"], color = 'darkblue',   marker = '.', linestyle = '', label = "Approximation von $\pi$") # Datenpunkte
        plt.xlabel("Index der Partialsumme")
        plt.ylabel("Wert der Partialsumme")
        plt.axhline(y=pi, color="red", label = "$\pi$")
        plt.legend()

    plt.show()

def error_pi(calculated_pi: Decimal) -> (Decimal):
    
    getcontext().prec = 1010
    
    pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989'
   
    fehler = Decimal(pi) * Decimal('1') - calculated_pi * Decimal('1')
    
    if fehler < Decimal('0'):
        fehler = Decimal('-1')  * fehler

    return fehler

def decimal_factorial(n) -> Decimal: 
   """
   Berechnet die Fakultät einer gegebenen Zahl n unter Verwendung des Decimal-Datentyps.
    
   Inputs:
   n (int): Die Zahl, deren Fakultät berechnet werden soll. Muss eine nicht-negative ganze Zahl sein.
    
   Returns:
   Decimal: Die Fakultät der Zahl n als Decimal-Objekt.
   """

   result = Decimal('1')

   #Berechnung der Fakultät mit Decimal
   for i in range(1, n + 1):
       result *= Decimal(i) * Decimal('1') 

   return result

def pi_leibniz(index: int, precision = 50) -> Decimal:
    """
    Berechnet eine Näherung von Pi mit der Leibniz-Reihe.

    Inputs:
    index (int): Index der Partialsumme der Leibniz-Reihe.
    precision (int): Mantissenlänge des Datentyps Decimal. (default: 50)

    Returns:
    Decimal: Eine Näherung von Pi.
    Decimal: Anzahl der durchgeführten Operationen.
    Decimal: Benötigte Zeit in Millisekunden.
    """
    start_time = time.time()
    getcontext().prec = precision
    pi_approx = Decimal('4')
    a_n = Decimal('8') / (Decimal('15') * Decimal('1'))
    n = Decimal('1') 
    operations = Decimal('2')

    while n <= index :
        pi_approx = pi_approx - a_n
        n += Decimal('1')
        a_n = Decimal('8') / (Decimal('16') * Decimal('1') * (Decimal(n) * Decimal('1')) * (Decimal(n) * Decimal('1')) - Decimal('1'))
        operations += Decimal('9')
    end_time = time.time()

    elapsed_time = ((Decimal(end_time) * Decimal('1')) - (Decimal(start_time) * Decimal('1'))) * (Decimal('1000') * Decimal('1'))
    return pi_approx, operations, elapsed_time

def pi_montecarlo(num_points, precision = 50) -> Decimal:
    """
    Berechnet eine Näherung von Pi mit dem Monte-Carlo-Algorithmus.
    
    Inputs:
    index (int): Anzahl der zufällig generierten Punkte.
    precision (int): Mantissenlänge des Datentyps Decimal. (default: 50)

    Returns:
    Decimal: Eine Näherung von Pi.
    Decimal: Anzahl der durchgeführten Operationen.
    Decimal: Benötigte Zeit in Millisekunden.
    """    
    start_time = time.time()   
    getcontext().prec = precision
    inside_circle = Decimal('0') 
    operations = Decimal('0')
    for p in range(num_points):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        if x * x + y * y <= 1:
            inside_circle += Decimal('1')
            operations += Decimal('5')
    pi_approx = ((inside_circle * Decimal('1')) / (Decimal(num_points) * Decimal('1'))) * Decimal('4')
    operations += Decimal('4')
    end_time = time.time()
    elapsed_time = ((Decimal(end_time) * Decimal('1')) - (Decimal(start_time) * Decimal('1'))) * (Decimal('1000') * Decimal('1'))
    return pi_approx, operations, elapsed_time


def pi_viete(index: int, precision = 50) -> Decimal:
    """
    Berechnet eine Näherung von Pi mit dem Viète-Algorithmus.

    Inputs:
    index (int): Index des Partialproduktes.
    precision (int): Mantissenlänge des Datentyps Decimal. (default: 50)

    Returns:
    Decimal: Eine Näherung von Pi.
    Decimal: Anzahl der durchgeführten Operationen.
    Decimal: Benötigte Zeit in Millisekunden.
    """
    start_time = time.time()
    getcontext().prec = precision
    a_n = Decimal('2').sqrt()
    pi_approx = Decimal('2') * (Decimal('2') / a_n)
    operations = Decimal('3')

    for k in range(2,index+1):
        a = Decimal('2')+ a_n
        a_n = Decimal(a).sqrt()
        pi_approx = pi_approx * (Decimal('2') / a_n)
        operations += Decimal('4')
    end_time = time.time()

    elapsed_time = ((Decimal(end_time) * Decimal('1')) - (Decimal(start_time) * Decimal('1'))) * (Decimal('1000') * Decimal('1'))
    return pi_approx, operations, elapsed_time

def pi_chudnovsky(index: int, precision = 50) -> Decimal:
    """
    Berechnet eine Näherung von Pi mit dem Chudnovsky-Algorithmus.

    Inputs:
    index (int): Index der Partialsumme der verallgemeinerten, hypergeometrischen Reihe.
    precision (int): Mantissenlänge des Datentyps Decimal. (default: 50)

    Returns:
    Decimal: Eine Näherung von Pi.
    int: Anzahl der durchgeführten Operationen.
    float: Benötigte Zeit in Millisekunden.
    """ 
    getcontext().prec = precision
    partialsumme = Decimal('0')
    operations = Decimal('0')
    start_time=time.time()

    for k in range(index+1):
        a_k = Decimal('-1') ** (Decimal(k) * Decimal('1'))
        b_k = decimal_factorial(6*k) * Decimal('1')
        operations += Decimal(6*k)
        c_k = (Decimal('545140134') * Decimal('1')) * (Decimal(k) * Decimal('1')) + Decimal('13591409') 
        d_k = decimal_factorial(3*k) * Decimal('1')
        operations += Decimal(3*k)
        e_k = (decimal_factorial(k) * Decimal('1')) ** Decimal('3')
        operations += Decimal(k)
        f_k = (Decimal('640320') * Decimal('1'))**(Decimal(3)*(Decimal(k)*Decimal('1'))+(Decimal(3/2)*Decimal('1')))
        partialsumme = partialsumme + (a_k * b_k * c_k) / (d_k * e_k * f_k)
        operations += Decimal('22') * Decimal('1')
    
    pi_approx = Decimal('1') / (Decimal('12') * Decimal('1') * partialsumme)
    operations += Decimal('3')
    
    end_time = time.time()
    elapsed_time = (Decimal(end_time) * Decimal('1') - Decimal(start_time) * Decimal('1')) * Decimal('1000') * Decimal('1')
    return pi_approx, operations, elapsed_time

    

def main():
    """
    Hauptfunktion des Programms.
    """

    index = int(input("Bitte den gewünschten Index der Partialsumme der Leibniz-Reihe eingeben: "))
    precision = int(input("Bitte die gewünschte Präzision für die Leibniz-Reihe eingeben: "))
    pi_leibniz_approx, leibniz_ops, leibniz_time = pi_leibniz(index, precision)
    print(f"Pi (Leibniz-Reihe): {pi_leibniz_approx}")
    print(f"Anzahl der Operationen (Leibniz-Reihe): {leibniz_ops}")
    print(f"Benötigte Zeit (Leibniz-Reihe): {leibniz_time:.6f} Millisekunden")
    fehler = error_pi(pi_leibniz_approx)
    print(f"Fehler (Leibniz-Reihe): {fehler:.100f} (100 Nachkommastellen)")
    print(f"Natürlicher Logarithmus des Fehlers (Leibniz-Reihe): {fehler.ln():.50f} (50 Nachkommastellen)")

    num_points = int(input("Bitte die Anzahl der Punkte für die Monte-Carlo-Methode eingeben: "))
    precision = int(input("Bitte die gewünschte Präzision für die Monte-Carlo-Methode eingeben: "))
    pi_montecarlo_approx, montecarlo_ops, montecarlo_time = pi_montecarlo(num_points, precision)
    print(f"Pi (Monte-Carlo-Methode): {pi_montecarlo_approx}")
    print(f"Anzahl der Operationen (Monte-Carlo-Methode): {montecarlo_ops}")
    print(f"Benötigte Zeit (Monte-Carlo-Methode): {montecarlo_time:.6f} Millisekunden")
    fehler = error_pi(pi_montecarlo_approx)
    print(f"Fehler (Monte-Carlo-Algorithmus): {fehler:.100f} (100 Nachkommastellen)")
    print(f"Natürlicher Logarithmus des Fehlers (Monte-Carlo-Algorithmus): {fehler.ln():.50f} (50 Nachkommastellen)")
    
    index = int(input("Bitte den gewünschten Index des Partialproduktes eingeben: "))
    precision = int(input("Bitte die gewünschte Präzision für den Viète-Algorithmus eingeben: "))
    pi_viete_approx, viete_ops, viete_time = pi_viete(index, precision)
    print(f"Pi (Viète-Algorithmus): {pi_viete_approx}")
    print(f"Anzahl der Operationen (Viète-Algorithmus): {viete_ops}")
    print(f"Benötigte Zeit (Viète-Algorithmus): {viete_time:.6f} Millisekunden")
    fehler = error_pi(pi_viete_approx)
    print(f"Fehler (Viète-Algorithmus): {fehler:.100f} (100 Nachkommastellen)")
    print(f"Natürlicher Logarithmus des Fehlers (Viète-Algorithmus): {fehler.ln():.50f} (50 Nachkommastellen)")
    
    index = int(input("Bitte den gewünschten Index der Partialsumme der hypergeometrischen Reihe eingeben: "))
    precision = int(input("Bitte die gewünschte Präzision für den Chudnovsky-Algorithmus eingeben: "))
    pi_chudnovsky_approx, chudnovsky_ops, chudnovsky_time = pi_chudnovsky(index, precision)
    print(f"Pi (Chudnovsky-Algorithmus): {pi_chudnovsky_approx}")
    print(f"Anzahl der Operationen (Chudnovsky-Algorithmus): {chudnovsky_ops}")
    print(f"Benötigte Zeit (Chudnovsky-Algorithmus): {chudnovsky_time:.6f} Millisekunden")
    fehler = error_pi(pi_chudnovsky_approx)
    print(f"Fehler (Chudnovsky-Algorithmus): {fehler:.100f} (100 Nachkommastellen)")
    print(f"Natürlicher Logarithmus des Fehlers (Chudnovsky-Algorithmus): {fehler.ln():.50f} (50 Nachkommastellen)")


if __name__ == "__main__":
    main()

