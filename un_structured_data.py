import psycopg2
import pandas as pd
import json
from datetime import datetime

# Paso 1: Crear la base de datos y la tabla desde Python
def create_database_and_table():
    try:
        # Conexión al servidor PostgreSQL (sin especificar una base de datos)
        conn = psycopg2.connect(
            user="postgres",  # Usuario predeterminado
            password="postgres",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True  # Necesario para crear una base de datos
        cursor = conn.cursor()

        # Crear la base de datos "tarea2" si no existe
        cursor.execute("SELECT datname FROM pg_database WHERE datname='tarea2';")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE tarea2;")
            print("Base de datos 'tarea2' creada correctamente.")
        else:
            print("La base de datos 'tarea2' ya existe.")

        # Cerrar la conexión inicial
        cursor.close()
        conn.close()

        # Conectar a la nueva base de datos
        conn = psycopg2.connect(
            database="tarea2",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Crear la tabla "tabla2" si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tabla2 (
            event_id VARCHAR(36) PRIMARY KEY,
			timestamp VARCHAR(20),
			source_ip VARCHAR(15),
			destination_ip VARCHAR(15),
			attack_type VARCHAR(50)
        );
        """)
        print("Tabla 'tabla2' creada correctamente.")

        # Confirmar cambios y cerrar la conexión
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error al crear la base de datos o la tabla: {e}")

# Paso 2: Insertar datos estructurados en la tabla
def insert_tarea2():
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            database="tarea2",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        df = pd.read_csv('ai_ml_cybersecurity_dataset.csv')

        # Insertar los datos fila por fila
        for index, row in df.head(10).iterrows():
            cur.execute(
            "INSERT INTO tabla2 (event_id, timestamp, source_ip, destination_ip, attack_type) VALUES (%s, %s, %s, %s, %s)",
            (row['Event ID'], row['Timestamp'], row['Source IP'], row['Destination IP'], row['Attack Type'])
    )

        # Confirmar cambios y cerrar la conexión
        conn.commit()
        print("Datos estructurados insertados correctamente.")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error al insertar datos estructurados: {e}")

# Ejecutar todas las funciones
if __name__ == "__main__":
    create_database_and_table()  # Crear base de datos y tabla
    insert_tarea2()     # Insertar datos estructurados
