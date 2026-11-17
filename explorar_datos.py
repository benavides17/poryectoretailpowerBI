
import pandas as pd
from pathlib import Path

ruta = Path(__file__).parent / "datos_originales" / "sales_data_sample.csv"

df = pd.read_csv(ruta, encoding="latin1")

print("===== PROYECTO RETAIL =====")
print("Total de filas:", df.shape[0])
print("Total de columnas:", df.shape[1])

print("\nPrimeros 5 registros:")
print(df.head())

print("\nColumnas disponibles:")
print(df.columns.tolist())

# ==========================================
# PASO 3: ANALISIS DE CALIDAD DE DATOS
# ==========================================

print("\n===== VALORES NULOS =====")
print(df.isnull().sum())

print("\n===== REGISTROS DUPLICADOS =====")
print("Filas duplicadas:", df.duplicated().sum())

print("\n===== TIPOS DE DATOS =====")
print(df.dtypes)

print("\n===== RESUMEN ESTADISTICO =====")
print(df[["SALES", "QUANTITYORDERED", "PRICEEACH"]].describe())

print("\n===== PAISES DISPONIBLES =====")
print(df["COUNTRY"].value_counts())

print("\n===== RANGO DE FECHAS =====")
fechas = pd.to_datetime(df["ORDERDATE"], errors="coerce")
print("Fecha inicial:", fechas.min())
print("Fecha final:", fechas.max())
print("Fechas invalidas:", fechas.isna().sum())
