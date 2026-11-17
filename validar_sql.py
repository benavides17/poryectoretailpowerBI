
import sqlite3
from pathlib import Path

# Ubicacion del proyecto
BASE = Path(__file__).resolve().parent
RUTA_DB = BASE / "base_datos" / "retail_ventas.db"

if not RUTA_DB.is_file():
    raise FileNotFoundError(
        f"No se encontro la base de datos: {RUTA_DB}"
    )

# Conectar con SQLite
conexion = sqlite3.connect(RUTA_DB)
cursor = conexion.cursor()

try:
    print("================================")
    print(" VALIDACION BASE DE DATOS SQL")
    print("================================")

    # Consultar las tablas existentes
    cursor.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table'"
    )
    tablas = [fila[0] for fila in cursor.fetchall()]

    print("\nTABLAS ENCONTRADAS:")
    for tabla in tablas:
        print("-", tabla)

    # Validar cada tabla disponible
    for tabla in tablas:
        nombre_seguro = '"' + tabla.replace('"', '""') + '"'

        cursor.execute(
            f"SELECT COUNT(*) FROM {nombre_seguro}"
        )
        print(f"\nRegistros en {tabla}:", cursor.fetchone()[0])

        cursor.execute(
            f"PRAGMA table_info({nombre_seguro})"
        )
        columnas = [fila[1] for fila in cursor.fetchall()]

        if "SALES" in columnas:
            cursor.execute(
                f'SELECT SUM("SALES") FROM {nombre_seguro}'
            )
            total = cursor.fetchone()[0]
            print("Ventas totales:", round(total or 0, 2))

    print("\nVALIDACION SQL FINALIZADA")

finally:
    conexion.close()
