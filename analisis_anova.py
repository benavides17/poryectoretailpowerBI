
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import f_oneway, levene

# ANALISIS ANOVA - RETAIL MULTINACIONAL

base = Path(__file__).resolve().parent

archivo = base / "datos_procesados" / "ventas_transformadas_spark.csv"
salida = base / "resultados_anova"
salida.mkdir(exist_ok=True)

print("================================")
print(" ANALISIS ESTADISTICO ANOVA")
print("================================")

# 1. CARGAR DATOS
df = pd.read_csv(archivo)

df["SALES"] = pd.to_numeric(df["SALES"], errors="coerce")
df = df.dropna(subset=["SALES", "PRODUCTLINE"])

print("Registros analizados:", len(df))

# 2. ESTADISTICAS POR CATEGORIA
resumen = (
    df.groupby("PRODUCTLINE")["SALES"]
    .agg(["count", "mean", "std", "sum"])
    .sort_values("mean", ascending=False)
)

print("\nVENTAS POR CATEGORIA:")
print(resumen.round(2))

resumen.to_csv(
    salida / "resumen_categorias.csv",
    encoding="utf-8-sig"
)

# 3. PREPARAR GRUPOS
grupos = [
    datos["SALES"].to_numpy()
    for _, datos in df.groupby("PRODUCTLINE")
    if len(datos) >= 2
]

if len(grupos) < 2:
    raise ValueError("Se necesitan al menos dos categorias")

# 4. PRUEBA DE LEVENE
estadistico_levene, p_levene = levene(
    *grupos,
    center="median"
)

print("\nPRUEBA DE LEVENE")
print("Estadistico:", round(estadistico_levene, 4))
print("Valor p:", p_levene)

# 5. PRUEBA ANOVA
if p_levene < 0.05:
    metodo = "ANOVA de Welch"
    f, p = f_oneway(*grupos, equal_var=False)
else:
    metodo = "ANOVA clasica"
    f, p = f_oneway(*grupos)

print("\nRESULTADOS ANOVA")
print("Metodo:", metodo)
print("Estadistico F:", round(f, 4))
print("Valor p:", p)

if p < 0.05:
    conclusion = (
        "Se rechaza H0: existen diferencias "
        "estadisticamente significativas entre "
        "las medias de al menos dos categorias."
    )
else:
    conclusion = (
        "No se rechaza H0: no hay evidencia "
        "suficiente de diferencias entre medias."
    )

print("\nCONCLUSION:")
print(conclusion)

# 6. GRAFICO
plt.figure(figsize=(11, 6))

resumen["mean"].sort_values().plot(kind="barh")

plt.xlabel("Venta promedio por linea de pedido")
plt.ylabel("Categoria de producto")
plt.title("Ventas promedio por categoria")

plt.tight_layout()
plt.savefig(salida / "grafico_anova.png", dpi=150)
plt.close()

# 7. GUARDAR INFORME
with open(
    salida / "resultado_anova.txt",
    "w",
    encoding="utf-8"
) as reporte:
    reporte.write("ANALISIS ANOVA - RETAIL\n")
    reporte.write(f"Metodo: {metodo}\n")
    reporte.write(f"Estadistico F: {f}\n")
    reporte.write(f"Valor p: {p}\n")
    reporte.write(f"Conclusion: {conclusion}\n")

print("\nANOVA FINALIZADO CORRECTAMENTE")
print("Resultados guardados en:", salida)
