#import time #Zeitmessung
import random #Zufallszahlen

def pi_leibniz(tol: float):
    pi = 4
    sk = 8./15
    k = 1
    while sk >= tol :
        pi = pi - sk
        k = k + 1
        sk = 8./(16* k * k - 1)
    return pi

def pi_montecarlo(num_points):
    
    inside_circle = 0

    for p in range(num_points):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        if x*x + y*y <= 1:
            inside_circle += 1
    return (inside_circle / num_points) * 4


def main():
    toleranz = float(input("Genauigkeit: "))
    pi1 = pi_leibniz(toleranz)
    print(pi1)
    
    num_points=int(input("Anzahl der Punkte: "))
    pi2=pi_montecarlo(num_points)
    print(pi2)

if __name__ == "__main__":
    main()