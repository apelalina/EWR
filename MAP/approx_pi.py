def pi_leibniz(tol: float):
    pi = 4
    sk = 8./15
    k = 1
    while sk >= tol :
        pi = pi - sk
        k = k + 1
        sk = 8./(16* k * k - 1)
    return pi

def main():
    toleranz = float(input("Genauigkeit: "))
    pi1 = pi_leibniz(toleranz)
    print(pi1)

if __name__ == "__main__":
    main()