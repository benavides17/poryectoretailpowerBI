
import pandas as pd
from pathlib import Path

# 1. Rutas del proyecto
base = Path(__file__).parent
entrada = base / "datos_originales" / "sales_data_sample.csv"
salida = base / "datos_procesados" / "ventas_limpias.csv"

salida.parent.mkdir(parents=True, exist_ok=True)

# 2. Extraer los datos originales
df = pd.read_csv(entrada, encoding="latin1")

print("===== ETL: LIMPIEZA DE VENTAS =====")
print("Registros originales:", len(df))

# 3. Eliminar duplicados exactos
df = df.drop_duplicates().copy()

# 4. Convertir fechas correctamente
df["ORDERDATE"] = pd.to_datetime(
    df["ORDERDATE"], errors="coerce"
)

# 5. Limpiar espacios en columnas de texto
columnas_texto = df.select_dtypes(
    include=["object", "str"]
).columns

for columna in columnas_texto:
    df[columna] = df[columna].str.strip()

# 6. Completar campos geográficos opcionales
for columna in ["STATE", "TERRITORY"]:
    df[columna] = df[columna].fillna("No especificado")

# No inventamos direcciones ni códigos postales
# Los valores faltantes se conservan

# 7. Crear columnas para análisis temporal
df["ANIO"] = df["ORDERDATE"].dt.year
df["MES"] = df["ORDERDATE"].dt.month
df["TRIMESTRE"] = df["ORDERDATE"].dt.quarter
df["ANIO_MES"] = df["ORDERDATE"].dt.strftime("%Y-%m")

# 8. Crear identificador único de línea de venta
df["ID_LINEA_VENTA"] = (
    df["ORDERNUMBER"].astype(str)
    + "-"
    + df["ORDERLINENUMBER"].astype(str)
)

# 9. Validaciones
assert df["ORDERDATE"].notna().all(), "Existen fechas invalidas"
assert df["ID_LINEA_VENTA"].is_unique, "Hay IDs repetidos"
assert df["SALES"].notna().all(), "Existen ventas vacias"

# 10. Exportar datos procesados
df.to_csv(
    salida,
    index=False,
    encoding="utf-8-sig",
    date_format="%Y-%m-%d"
)

print("\n===== RESULTADO =====")
print("Registros procesados:", len(df))
print("Columnas finales:", len(df.columns))
print("Ventas totales:", round(df["SALES"].sum(), 2))
print("Archivo generado:", salida)
print("\nETL FINALIZADO CORRECTAMENTE")
