import pandas as pd
import matplotlib.pyplot as plt 
from decimal import Decimal, getcontext
from main import *
from py_logspace import py_logspace

data = pd.read_csv("Experimente/Algorithmenvergleich_500/Algorithmenvergleich_500.csv",
                    converters={"Fehler": Decimal, "Pi": Decimal, "Laufzeit": Decimal, "Operationen": Decimal})
data_chudnovsky = data[data["Algorithmus"] == "chudnovsky"]
data_viete = data[data["Algorithmus"] == "viete"]
data_leibniz = data[data["Algorithmus"] == "leibniz"]
data_montecarlo = data[data["Algorithmus"] == "montecarlo"]

print(data)
for i in range(30):
    data_chudnovsky.iloc[i, 3] = Decimal.log10(data_chudnovsky.iloc[i, 3])
print(data_chudnovsky["Fehler"])

data2 = pd.read_csv("Experimente/chudnovsky_1000_3/pi_chudnovsky_3.csv",
                    converters={"Fehler": Decimal, "Pi": Decimal, "Laufzeit": Decimal, "Operationen": Decimal})
for i in range(30):
    data2.iloc[i, 3] = Decimal.log10(data2.iloc[i, 3])
print(data2["Fehler"])
plt.semilogx(data2["n"], data2["Fehler"])

data3 = pd.read_csv("Experimente/viete_1000_6/pi_viete_6.csv",
                    converters={"Fehler": Decimal, "Pi": Decimal, "Laufzeit": Decimal, "Operationen": Decimal})
for i in range(30):
    data3.iloc[i, 3] = Decimal.log10(data3.iloc[i, 3])
print(data3["Fehler"])
plt.semilogx(data3["n"], data3["Fehler"])

for i in range(30):
    data_montecarlo.iloc[i, 3] = Decimal.log10(data_montecarlo.iloc[i, 3])
print(data_montecarlo["Fehler"])
plt.semilogx(data_montecarlo["n"], data_montecarlo["Fehler"])


for i in range(30):
    data_leibniz.iloc[i, 3] = Decimal.log10(data_leibniz.iloc[i, 3])
print(data_leibniz["Fehler"])
plt.semilogx(data_leibniz["n"], data_leibniz["Fehler"])

#plot_pi(data_chudnovsky, y = "Fehler", linecolor = "orange", pointcolor = "darkorange", label = "Chudnovsky-Algorithmus")
#plot_pi(data_montecarlo, y = "Fehler", linecolor = "blue", pointcolor = "darkblue", label = "Monte-Carlo-Methode")
#plot_pi(data_leibniz, y = "Fehler", linecolor = "green", pointcolor = "darkgreen", label = "Leibniz-Reihe")
#plot_pi(data_viete, y = "Fehler", linecolor = "red", pointcolor = "darkred", label = "Vietes Produktdarstellung")
#plt.savefig('Algorithmenvergleich_Fehlerplot.pdf')
#y_range = py_logspace(start=0, stop=-550, num = 5, basis=10)
#print(y_range)
#print(min(data["Fehler"]))
#plt.yticks(y_range)
plt.show()
