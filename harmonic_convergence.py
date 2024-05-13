import numpy as np
from py_logspace import py_logspace

def vorwärts_summation(start, stop, num, basis, data_type):
    
    #Indexliste der Folgeglieder
    liste = py_logspace(start, stop, num, basis)
    result = []
    
    #Berechnung
    for i in range(num):
        
        k=liste[i]
        
        #Berechnung Folgeglieder
        partialsumme=data_type(0)
        x=0
        while x<k:
            partialsumme=partialsumme+data_type((1/(x+1)))
            x += 1
        result.append(partialsumme)
        
    return(result)

def kahan_summation(start, stop, num, basis, data_type):
    
    #Indexliste der Folgeglieder
    liste = py_logspace(start, stop, num, basis)
    
    #Berechnung
    for i in range(num):
        
        k=liste[i]
        
        #Berechnung Folgeglieder
        partialsumme=0
        x=0
        kompensation=0
        while x<k:
            
            vorläufige_partialsumme=partialsumme+(1/(x+1))
            
            if abs(sum) >= abs(1/(x+1)):
                kompensation += (partialsumme - vorläufige_partialsumme) + x
                
            else:
                kompensation += (x - vorläufige_partialsumme) + x
            
            partialsumme = vorläufige_partialsumme + kompensation
            liste[i]=partialsumme
    
    return(liste)
            
def main():
    """Hauptfunktion des Programms"""

    # Definition der Variablen
    start = input("Start: ")
    while True:
        try:
            start = int(start)
            break
        except ValueError:
            start = input("Bitte geben Sie eine ganze Zahl ein. Start: ")
    
    stop = input("Stop: ")
    while True:
        try:
            stop = int(stop)
            break
        except ValueError:
            stop = input("Bitte geben Sie eine ganze Zahl ein. Stop: ")

    num = input("Num: ")
    while True:
        try:
            num = int(num)
            if num >= 2:
                break
            else:
                num = input("Bitte geben Sie eine Zahl >= 2 ein. Num: ")
        except ValueError:
            num = input("Bitte geben Sie eine ganze Zahl ein. Num: ")
    
    basis = input("Basis: ")
    while True:
        try:
            basis = int(basis)
            break
        except ValueError:
            basis = input("Bitte geben Sie eine ganze Zahl ein. Basis: ")

    try:
        # Beispielaufrufe für die Funktionen
        result_vorwärts_float16 = vorwärts_summation(np.float16)
        print("Vorwärtssummation mit np.float16:", result_vorwärts_float16)

        result_vorwärts_float32 = vorwärts_summation(np.float32)
        print("Vorwärtssummation mit np.float32:", result_vorwärts_float32)

        result_vorwärts_float64 = vorwärts_summation(np.float64)
        print("Vorwärtssummation mit np.float64:", result_vorwärts_float64)

        result_kahan_float16 = kahan_summation(np.float16)
        print("Kahansummation mit np.float16:", result_kahan_float16)

        result_kahan_float32 = kahan_summation(np.float32)
        print("Kahansummation mit np.float32:", result_kahan_float32)

        result_kahan_float64 = kahan_summation(np.float64)
        print("Kahansummation mit np.float64:", result_kahan_float64)
        
    except ValueError:
        print("Funktionsaufruf gescheitert. Bitte neu aufrufen.")
      

if __name__ == "__main__":
    main()
