import pandas as pd
import matplotlib.pyplot as plt 
from decimal import Decimal, getcontext
from main import *

getcontext().prec = 2002


# Standardabweichungen Monte-Carlo -------------------------------------------------------

data = pd.read_csv("Experimente/montecarlo_4-6/pi_montecarlo_6.csv",
                    converters={"Fehler": Decimal, "Pi": Decimal, "Laufzeit": Decimal, "Operationen": Decimal})

grouped = data.groupby('n')
std_devs = grouped['Pi'].apply(lambda x: float(pd.Series([float(val) for val in x]).std()))
std_devs_df = std_devs.reset_index(name='Standardabweichung')
data = data.merge(std_devs_df, on='n')

plt.figure()
plt.scatter(data['n'], data['Standardabweichung'], color='darkblue', s = 8, label = "Standardabweichung der Monte-Carlo-Schätzungen")
plt.xscale('log')
plt.yscale('log')
plt.yticks([10**i for i in range(-4, 0)])
plt.xlabel('Eingabeparameter n (Anzahl der Punkte)')
plt.ylabel('Standardabweichung der Schätzung von $\pi$')
plt.grid()
plt.legend()

plt.savefig('MonteCarlo_Standardabweichungen.pdf')
plt.show()

plt.close()

# Fehlerplot Algorithmenvergleich -----------------------------------------------------------

data = pd.read_csv("Experimente/Algorithmenvergleich_2000/Algorithmenvergleich_2000.csv",
                    converters={"Fehler": Decimal, "Pi": Decimal, "Laufzeit": Decimal, "Operationen": Decimal})
data_chudnovsky = data[data["Algorithmus"] == "chudnovsky"]
data_viete = data[data["Algorithmus"] == "viete"]
data_leibniz = data[data["Algorithmus"] == "leibniz"]
data_montecarlo = data[data["Algorithmus"] == "montecarlo"]

for i in range(30):
    data_montecarlo.iloc[i, 3] = Decimal.log10(data_montecarlo.iloc[i, 3])

for i in range(30):
    data_leibniz.iloc[i, 3] = Decimal.log10(data_leibniz.iloc[i, 3])

for i in range(30):
    data_viete.iloc[i, 3] = Decimal.log10(data_viete.iloc[i, 3])

for i in range(30):
    data_chudnovsky.iloc[i, 3] = Decimal.log10(data_chudnovsky.iloc[i, 3])

plt.semilogx(data_montecarlo["n"], data_montecarlo["Fehler"], color = "blue")
plt.plot(data["n"], data["Fehler"], color = "darkblue",   marker = '.', linestyle = '', label = "Monte-Carlo-Methode")

plt.semilogx(data_leibniz["n"], data_leibniz["Fehler"], color = "green")
plt.plot(data_leibniz["n"], data_leibniz["Fehler"], color = "darkgreen",   marker = '.', linestyle = '', label = "Leibniz-Reihe")

plt.semilogx(data_viete["n"], data_viete["Fehler"], color = "red")
plt.plot(data_viete["n"], data_viete["Fehler"], color = "darkred",   marker = '.', linestyle = '', label = "Vietes Produktdarstellung")

plt.semilogx(data_chudnovsky["n"], data_chudnovsky["Fehler"], color = "orange")
plt.plot(data_chudnovsky["n"], data_chudnovsky["Fehler"], color = "darkorange",   marker = '.', linestyle = '', label = "Chudnovsky-Algorithmus")

plt.xlabel("Eingabeparameter n")
plt.ylabel("$\log_{10}$(Fehler)")

plt.legend()
plt.grid()

plt.savefig('Algorithmenvergleich_Fehlerplot_2000.pdf')
plt.show()

