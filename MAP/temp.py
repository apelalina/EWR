import pandas as pd
import matplotlib.pyplot as plt 
from decimal import Decimal, getcontext
from main import *

getcontext().prec = 2002

data = pd.read_csv("Experimente/Mantissenvergleich_Chudnovsky_2000/Mantissenvergleich_Chudnovsky.csv",
                    converters={"Fehler": Decimal, "Pi": Decimal, "Laufzeit": Decimal, "Operationen": Decimal})

print(data)

data1 = data[data["Mantissenlänge" == str(400)]]
data2 = data[data["Mantissenlänge" == str(800)]]
data3 = data[data["Mantissenlänge" == str(1200)]]
data4 = data[data["Mantissenlänge" == str(1600)]]
data5 = data[data["Mantissenlänge" == str(2000)]]

print("Berechne log10(Fehler), Mantissenlänge " + str(400))
for i in range(30):
    data1.iloc[i, 3] = Decimal.log10(data1.iloc[i, 3])
print("Berechne log10(Fehler), Mantissenlänge " + str(800))
for i in range(30):
    data2.iloc[i, 3] = Decimal.log10(data2.iloc[i, 3])
print("Berechne log10(Fehler), Mantissenlänge " + str(1200))
for i in range(30):
    data3.iloc[i, 3] = Decimal.log10(data3.iloc[i, 3])
print("Berechne log10(Fehler), Mantissenlänge " + str(1600))
for i in range(30):
    data4.iloc[i, 3] = Decimal.log10(data4.iloc[i, 3])
print("Berechne log10(Fehler), Mantissenlänge " + str(2000))
for i in range(30):
    data5.iloc[i, 3] = Decimal.log10(data5.iloc[i, 3])
        
plt.semilogx(data1["n"], data1["Fehler"], color = "red")
plt.plot(data1["n"], data1["Fehler"], color = "darkred",   marker = '.', linestyle = '', label = "Monte-Carlo-Methode")
plt.semilogx(data2["n"], data2["Fehler"], color = "orange")
plt.plot(data2["n"], data2["Fehler"], color = "darkorange",   marker = '.', linestyle = '', label = "Leibniz-Reihe")
plt.semilogx(data3["n"], data3["Fehler"], color = "green")
plt.plot(data3["n"], data3["Fehler"], color = "darkgreen",   marker = '.', linestyle = '', label = "Vietes Produktdarstellung")
plt.semilogx(data4["n"], data4["Fehler"], color = "blue")
plt.plot(data4["n"], data4["Fehler"], color = "darkblue",   marker = '.', linestyle = '', label = "Chudnovsky-Algorithmus")
plt.semilogx(data5["n"], data5["Fehler"], color = "darkviolet")
plt.plot(data5["n"], data5["Fehler"], color = "purple",   marker = '.', linestyle = '', label = "Chudnovsky-Algorithmus")
plt.xlabel("Eingabeparameter n")
plt.ylabel("$\log_{10}$(Fehler)")
plt.legend(title = "Chudnovsky-Algorithmus")
plt.grid()
plt.savefig('Mantissenvergleich_Fehlerplot_log10.pdf')
plt.show()
