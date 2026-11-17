
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent

archivo_csv = (
    BASE / "datos_procesados"
    / "ventas_transformadas_spark.csv"
)

archivo_json = (
    BASE / "datos_procesados"
    / "ventas_transformadas.json"
)

# Leer datos transformados
df = pd.read_csv(archivo_csv)

# Convertir a JSON
df.to_json(
    archivo_json,
    orient="records",
    indent=2,
    force_ascii=False,
    date_format="iso"
)

print("================================")
print(" GENERACION DE JSON")
print("================================")
print("Registros exportados:", len(df))
print("Archivo generado:", archivo_json)
print("PROCESO JSON FINALIZADO CORRECTAMENTE")
