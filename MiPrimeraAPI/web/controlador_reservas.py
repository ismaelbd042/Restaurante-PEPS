from __future__ import print_function
from bd import obtener_conexion
import sys

def insertar_reserva(nombre_Cliente, lugar, precio_reserva,foto_comida_reserva):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO reservas(nombre_Cliente, lugar, precio_reserva,foto_comida_reserva) VALUES (%s, %s, %s,%s)",
                       (nombre_Cliente, lugar, precio_reserva,foto_comida_reserva))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret = {"status": "Failure" }
        code=200
        conexion.commit()
        conexion.close()
    except:
        print("Excepcion al insertar una reserva", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def convertir_reserva_a_json(reservas):
    d = {}
    d['id'] = reservas[0]                                           
    d['nombre_Cliente'] = reservas[1]
    d['lugar'] = reservas[2]
    d['precio_reserva'] = reservas[3]
    d['foto_comida_reserva'] = reservas[4]
    return d

def obtener_reservas():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre_Cliente, lugar, precio_reserva,foto_comida_reserva FROM reservas")
            reservas = cursor.fetchall()
            reservasjson=[]
            if reservas:
                for reserva in reservas:
                    reservasjson.append(convertir_reserva_a_json(reserva))
        conexion.close()
        code=200
    except:
        print("Excepcion al obtener las reservas", file=sys.stdout)
        reservasjson=[]
        code=500
    return reservasjson,code

def obtener_reserva_por_id(id):
    reservajson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            #cursor.execute("SELECT id, nombre_Cliente, lugar, precio_reserva,foto_comida_reserva WHERE id = %s", (id,))
            cursor.execute("SELECT id, nombre_Cliente, lugar, precio_reserva,foto_comida_reserva FROM reservas WHERE id =" + id)
            reserva = cursor.fetchone()
            if reserva is not None:
                reservajson = convertir_reserva_a_json(reserva)
        conexion.close()
        code=200
    except:
        print("Excepcion al recuperar un reserva", file=sys.stdout)
        code=500
    return reservajson,code


def eliminar_reserva(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM reservas WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar una reserva", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def actualizar_reserva(id,  nombre_Cliente, lugar, precio_reserva,foto_comida_reserva):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE reservas SET nombre_Cliente = %s, lugar = %s, precio_reserva = %s, foto_comida_reserva=%s WHERE id = %s",
                       ( nombre_Cliente, lugar, precio_reserva,foto_comida_reserva, id))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar una reserva", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code
