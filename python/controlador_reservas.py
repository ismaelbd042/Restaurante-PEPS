from bd import obtener_conexion
from __main__ import app
from funciones_auxiliares import sanitize_input
import os
import pymysql
from flask_wtf.csrf import generate_csrf
from funciones_auxiliares import compare_password, cipher_password, create_session
import datetime as dt

# Función para insertar una nueva reserva en la base de datos
def insertar_reserva(cliente, fecha, hora, numero_personas, observaciones):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO reserva(cliente, fecha, hora, numero_personas, observaciones)
                VALUES (%s, %s, %s, %s, %s)
            """, (sanitize_input(cliente), fecha, hora, numero_personas, sanitize_input(observaciones)))
            
            if cursor.rowcount == 1:
                ret = {"status": "OK"}
            else:
                ret = {"status": "Failure"}
        
        conexion.commit()
        conexion.close()
        code = 200
    except pymysql.MySQLError as e:
        app.logger.error(f"Error al insertar una reserva: {e}")
        ret = {"status": "Failure"}
        code = 500
    return ret, code

# Función para convertir los datos de una reserva en un formato JSON
def convertir_reserva_a_json(reserva):
    d = {
        'id': reserva[0],
        'cliente': sanitize_input(reserva[1]),
        'fecha': reserva[2],
        'hora': reserva[3],
        'numero_personas': reserva[4],
        'observaciones': sanitize_input(reserva[5])
    }
    return d

# Función para obtener todas las reservas de la base de datos
def obtener_reservas():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, cliente, fecha, hora, numero_personas, observaciones FROM reserva")
            reservas = cursor.fetchall()
            reservas_json = []
            if reservas:
                for reserva in reservas:
                    reservas_json.append(convertir_reserva_a_json(reserva))
        
        conexion.close()
        code = 200
    except pymysql.MySQLError as e:
        app.logger.error(f"Error al obtener las reservas: {e}")
        reservas_json = []
        code = 500
    
    return reservas_json, code

# Función para obtener una reserva por ID
def obtener_reserva_por_id(id):
    reserva_json = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, cliente, fecha, hora, numero_personas, observaciones FROM reserva WHERE id = %s LIMIT 1", (id,))
            reserva = cursor.fetchone()
            if reserva is not None:
                reserva_json = convertir_reserva_a_json(reserva)
        
        conexion.close()
        code = 200
    except pymysql.MySQLError as e:
        app.logger.error(f"Error al obtener la reserva con ID {id}: {e}")
        code = 500
    
    return reserva_json, code

# Función para eliminar una reserva de la base de datos
def eliminar_reserva(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM reserva WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret = {"status": "OK"}
            else:
                ret = {"status": "Failure"}
        
        conexion.commit()
        conexion.close()
        code = 200
    except pymysql.MySQLError as e:
        app.logger.error(f"Error al eliminar la reserva con ID {id}: {e}")
        ret = {"status": "Failure"}
        code = 500
    
    return ret, code

# Función para actualizar una reserva en la base de datos
def actualizar_reserva(id, cliente, fecha, hora, numero_personas, observaciones):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE reserva
                SET cliente = %s, fecha = %s, hora = %s, numero_personas = %s, observaciones = %s
                WHERE id = %s
            """, (sanitize_input(cliente), fecha, hora, numero_personas, sanitize_input(observaciones), id))
            
            if cursor.rowcount == 1:
                ret = {"status": "OK"}
            else:
                ret = {"status": "Failure"}
        
        conexion.commit()
        conexion.close()
        code = 200
    except pymysql.MySQLError as e:
        app.logger.error(f"Error al actualizar la reserva con ID {id}: {e}")
        ret = {"status": "Failure"}
        code = 500
    
    return ret, code

