import pandas as pd
import matplotlib.pyplot as plt 
from decimal import Decimal, getcontext
from main import *


getcontext().prec = 2002

data = pd.read_csv("Experimente/Algorithmenvergleich_2001/Algorithmenvergleich_2001.csv",
                    converters={"Fehler": Decimal, "Pi": Decimal, "Laufzeit": Decimal, "Operationen": Decimal})


export = pd.DataFrame({
    "Algorithmus": data["Algorithmus"],
    "n": data["n"],
    "Fehler (log10)": data["Fehler"],
    "Laufzeit (ms)": data["Laufzeit"],
    "Operationen": data["Operationen"]
})


for i in range(30*4):
    export.iloc[i, 2] = Decimal.log10(export.iloc[i, 2])

getcontext().prec = 15
export["Fehler (log10)"] = export["Fehler (log10)"] * Decimal('1')
export["Laufzeit (ms)"] = export["Laufzeit (ms)"] * Decimal('1')
export["Operationen"] = export["Operationen"] * Decimal('1')

export.to_csv("Datensatz.csv")


exit()

getcontext().prec = 2002

data = pd.read_csv("Experimente/Mantissenvergleich_Chudnovsky_2000/Mantissenvergleich_Chudnovsky.csv",
                    converters={"Fehler": Decimal, "Pi": Decimal, "Laufzeit": Decimal, "Operationen": Decimal})

print(data)

data1 = data[data["Mantissenlänge"] == 400]
data2 = data[data["Mantissenlänge"] == 800]
data3 = data[data["Mantissenlänge"] == 1200]
data4 = data[data["Mantissenlänge"] == 1600]
data5 = data[data["Mantissenlänge"] == 2000]

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
plt.plot(data1["n"], data1["Fehler"], color = "darkred",   marker = '.', linestyle = '', label = "Mantissenlänge 400")
plt.semilogx(data2["n"], data2["Fehler"], color = "orange")
plt.plot(data2["n"], data2["Fehler"], color = "darkorange",   marker = '.', linestyle = '', label = "Mantissenlänge 800")
plt.semilogx(data3["n"], data3["Fehler"], color = "green")
plt.plot(data3["n"], data3["Fehler"], color = "darkgreen",   marker = '.', linestyle = '', label = "Mantissenlänge 1200")
plt.semilogx(data4["n"], data4["Fehler"], color = "blue")
plt.plot(data4["n"], data4["Fehler"], color = "darkblue",   marker = '.', linestyle = '', label = "Mantissenlänge 1600")
plt.semilogx(data5["n"], data5["Fehler"], color = "darkviolet")
plt.plot(data5["n"], data5["Fehler"], color = "purple",   marker = '.', linestyle = '', label = "Mantissenlänge 2000")
plt.xlabel("Eingabeparameter n")
plt.ylabel("$\log_{10}$(Fehler)")
plt.legend(title = "Chudnovsky-Algorithmus")
plt.grid()
plt.savefig('Mantissenvergleich_Fehlerplot_log10.pdf')
plt.show()
