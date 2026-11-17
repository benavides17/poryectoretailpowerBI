
import pandas as pd
import sqlite3
from pathlib import Path

# ==========================================
# PROYECTO 1: RETAIL MULTINACIONAL
# CARGA DE DATOS A SQLITE
# ==========================================

# 1. Definir rutas
base = Path(__file__).parent

archivo_csv = base / "datos_procesados" / "ventas_limpias.csv"

carpeta_bd = base / "base_datos"
carpeta_bd.mkdir(exist_ok=True)

ruta_bd = carpeta_bd / "retail_ventas.db"

# 2. Leer los datos limpios
df = pd.read_csv(archivo_csv, encoding="utf-8-sig")

print("===== CARGA DE DATOS EN SQL =====")
print("Registros encontrados:", len(df))

# 3. Crear la base de datos
with sqlite3.connect(ruta_bd) as conexion:

    # Guardar datos en una tabla SQL
    df.to_sql(
        "ventas",
        conexion,
        if_exists="replace",
        index=False
    )

    # 4. Verificar los datos almacenados
    consulta = """
    SELECT
        COUNT(*) AS total_registros,
        ROUND(SUM(SALES), 2) AS ventas_totales
    FROM ventas;
    """

    resultado = pd.read_sql_query(
        consulta,
        conexion
    )

    print("\n===== VERIFICACION SQL =====")
    print(resultado.to_string(index=False))

    # 5. Consultar los cinco paises con mas ventas
    consulta_paises = """
    SELECT
        COUNTRY AS pais,
        ROUND(SUM(SALES), 2) AS total_ventas
    FROM ventas
    GROUP BY COUNTRY
    ORDER BY total_ventas DESC
    LIMIT 5;
    """

    resultado_paises = pd.read_sql_query(
        consulta_paises,
        conexion
    )

    print("\n===== TOP 5 PAISES =====")
    print(resultado_paises.to_string(index=False))

print("\nBase de datos creada en:", ruta_bd)
print("\nPROCESO SQL FINALIZADO CORRECTAMENTE")
