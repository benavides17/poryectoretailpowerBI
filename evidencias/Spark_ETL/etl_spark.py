
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    to_date,
    coalesce,
    sum as spark_sum,
    countDistinct
)
from pathlib import Path
import csv

# ============================================
# PROYECTO: ANALISIS DE VENTAS RETAIL
# ETL UTILIZANDO APACHE SPARK (PYSPARK)
# ============================================

print("========================================")
print(" INICIANDO ETL CON APACHE SPARK")
print("========================================")

# CONFIGURACION
BASE = Path(__file__).resolve().parent

ARCHIVO_ORIGINAL = (
    BASE / "datos_originales" / "sales_data_sample.csv"
)

CARPETA_SALIDA = BASE / "datos_procesados"
CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)

ARCHIVO_FINAL = (
    CARPETA_SALIDA / "ventas_transformadas_spark.csv"
)

if not ARCHIVO_ORIGINAL.exists():
    raise FileNotFoundError(
        f"No se encontro el CSV: {ARCHIVO_ORIGINAL}"
    )

# ============================================
# 1. INICIAR APACHE SPARK
# ============================================

spark = (
    SparkSession.builder
    .master("local[2]")
    .appName("ETL_Retail_Multinacional")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

try:

    # ========================================
    # 2. EXTRACCION
    # ========================================

    print("\nETAPA 1: EXTRACCION")

    df = spark.read.csv(
        str(ARCHIVO_ORIGINAL),
        header=True,
        inferSchema=True
    )

    registros_originales = df.count()

    print("Registros originales:", registros_originales)

    # ========================================
    # 3. TRANSFORMACION
    # ========================================

    print("\nETAPA 2: TRANSFORMACION")

    # Eliminar filas completamente duplicadas
    df = df.dropDuplicates()

    # Eliminar espacios extra en columnas de texto
    for nombre, tipo in df.dtypes:
        if tipo == "string":
            df = df.withColumn(
                nombre,
                trim(col(nombre))
            )

    # Convertir columnas numericas
    columnas_decimales = [
        "SALES",
        "PRICEEACH",
        "MSRP"
    ]

    for nombre in columnas_decimales:
        df = df.withColumn(
            nombre,
            col(nombre).cast("double")
        )

    columnas_enteras = [
        "ORDERNUMBER",
        "QUANTITYORDERED",
        "YEAR_ID"
    ]

    for nombre in columnas_enteras:
        df = df.withColumn(
            nombre,
            col(nombre).cast("int")
        )

    # Convertir fecha
    df = df.withColumn(
        "ORDERDATE",
        coalesce(
            to_date(col("ORDERDATE"), "M/d/yyyy H:mm"),
            to_date(col("ORDERDATE"), "M/d/yyyy"),
            to_date(col("ORDERDATE"), "yyyy-MM-dd")
        )
    )

    # Eliminar registros sin datos esenciales
    df = df.dropna(
        subset=[
            "ORDERNUMBER",
            "ORDERDATE",
            "SALES"
        ]
    )

    # ========================================
    # 4. VALIDACION DE LOS DATOS
    # ========================================

    print("\nVALIDACION DE LOS DATOS")

    registros_finales = df.count()

    resumen = df.agg(
        spark_sum("SALES").alias("ventas_totales"),
        countDistinct("ORDERNUMBER").alias("pedidos"),
        countDistinct("CUSTOMERNAME").alias("clientes")
    ).first()

    ventas_totales = resumen["ventas_totales"]
    total_pedidos = resumen["pedidos"]
    total_clientes = resumen["clientes"]

    print("Registros originales:", registros_originales)
    print("Registros transformados:", registros_finales)

    print("Ventas totales:", round(ventas_totales, 2))
    print("Pedidos unicos:", total_pedidos)
    print("Clientes unicos:", total_clientes)

    print("\nPRIMERAS 5 FILAS:")
    df.show(5, truncate=True)

    # ========================================
    # 5. CARGA
    # ========================================

    print("\nETAPA 3: CARGA")

    # Se utiliza Python CSV para escribir en
    # Windows sin depender de winutils.exe.
    # La transformacion fue realizada con Spark.

    with ARCHIVO_FINAL.open(
        mode="w",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        escritor = csv.writer(archivo)

        # Escribir nombres de columnas
        escritor.writerow(df.columns)

        # Escribir registros procesados
        for fila in df.toLocalIterator():
            escritor.writerow([
                valor if valor is not None else ""
                for valor in fila
            ])

    print("\nArchivo generado correctamente:")
    print(ARCHIVO_FINAL)

    print("\n========================================")
    print(" ETL FINALIZADO CORRECTAMENTE")
    print("========================================")

finally:
    spark.stop()
