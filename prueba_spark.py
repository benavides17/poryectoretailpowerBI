
from pyspark.sql import SparkSession

print("INICIANDO APACHE SPARK...", flush=True)

spark = (
    SparkSession.builder
    .master("local[2]")
    .appName("PruebaRetail")
    .getOrCreate()
)

print("VERSION:", spark.version, flush=True)
print("FILAS:", spark.range(10).count(), flush=True)

spark.stop()

print("PRUEBA FINALIZADA", flush=True)
