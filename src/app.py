import os
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
url = "https://companies-market-cap-copy.vercel.app/index.html"
respuesta = requests.get(url)
contenido = respuesta.text
contenido

soup = BeautifulSoup(contenido,"html.parser")
tabla = soup.find("table")  
tabla

rows = tabla.find_all("tr")
data = []
for row in rows[1:]:  # Saltar la fila de encabezado
    cols = row.find_all("td")
    fecha = cols[0].text.strip()
    ingresos = cols[1].text.strip()
    data.append([fecha, ingresos])
data

df = pd.DataFrame(data, columns=["Fecha", "Ingresos"])
df = df.sort_values("Fecha")
df

def convertir_ingresos(valor):
    if "B" in valor:
        editar_valor = float(valor.replace("B", "").replace("$", "").replace(",", ""))
        return editar_valor
df["Ingresos"] = df["Ingresos"].apply(convertir_ingresos)
df["Ingresos"]

conn = sqlite3.connect("tesla_revenues.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS ingresos (
    fecha TEXT,
    ingresos REAL
)
""")

for index, row in df.iterrows():
    cursor.execute("INSERT INTO ingresos (fecha, ingresos) VALUES (?, ?)", (row["Fecha"], row["Ingresos"]))

conn.commit()
conn.close()

print(f"Podemos realizar varios tipos de visualizacion como por ejemplo: gráficas estáticas, animadas e interactivas, pero voy a fijarlo en modo estática")
plt.figure(figsize=(15, 9))
plt.plot(df["Fecha"], df["Ingresos"], marker='o', label="Ingresos")
plt.title("Ingresos anuales de Tesla")
plt.xlabel("Fecha")
plt.ylabel("Ingresos en billones(USD)")
plt.grid(True)
plt.savefig("revenue_plotwist.png")
plt.show()