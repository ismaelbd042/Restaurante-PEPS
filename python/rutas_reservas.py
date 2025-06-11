from flask import request, session, make_response
import json
from __main__ import app
import controlador_reservas  
from funciones_auxiliares import Encoder, sanitize_input, prepare_response_extra_headers, validar_session_admin, validar_session_normal

@app.route("/reservas", methods=["GET"])
def reservas():
    if validar_session_normal():
        respuesta, code = controlador_reservas.obtener_reservas()  # Adaptado
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    return response

@app.route("/reservas/<id>", methods=["GET"])
def reserva_por_id(id):
    id = sanitize_input(id)
    if isinstance(id, str) and len(id) < 64:
        if validar_session_normal():
            respuesta, code = controlador_reservas.obtener_reserva_por_id(id)  # Adaptado
        else:
            respuesta = {"status": "Forbidden"}
            code = 403
    else:
        respuesta = {"status": "Bad parameters"}
        code = 401
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    return response

@app.route("/reservas", methods=["POST"])
def guardar_reserva():
    if request.is_json:
        data = request.get_json()
        required_fields = ["cliente", "fecha", "hora", "numero_personas", "observaciones"]
        if all(field in data for field in required_fields):
            if validar_session_admin():
                # Guardar en la base de datos
                respuesta, code = controlador_reservas.insertar_reserva(**data)
            else:
                respuesta = {"status": "Forbidden"}
                code = 403
        else:
            respuesta = {"status": "Bad request: campos faltantes"}
            code = 400
    else:
        respuesta = {"status": "Bad request: contenido no JSON"}
        code = 400

    return make_response(json.dumps(respuesta), code)


@app.route("/reservas/<id>", methods=["DELETE"])
def eliminar_reserva(id):
    if validar_session_admin():
        respuesta, code = controlador_reservas.eliminar_reserva(id)  # Adaptado
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    return response

@app.route("/reservas", methods=["PUT"])
def actualizar_reserva():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        reserva_json = request.json
        if "id" in reserva_json and "nombre" in reserva_json and "descripcion" in reserva_json and "foto" in reserva_json and "ingredientes" in reserva_json:
            id = request.json["id"]
            nombre = sanitize_input(reserva_json["nombre"])
            descripcion = sanitize_input(reserva_json["descripcion"])
            precio = reserva_json["precio"]
            foto = sanitize_input(reserva_json["foto"])
            ingredientes = sanitize_input(reserva_json["ingredientes"])
            if id.isnumeric() and isinstance(nombre, str) and isinstance(descripcion, str) and precio.isnumeric() and isinstance(foto, str) and isinstance(ingredientes, str) and len(nombre) < 128 and len(descripcion) < 512 and len(foto) < 128 and len(ingredientes) < 512:
                id=int(id)
                precio=float(precio)
                if (validar_session_normal()):
                    respuesta, code = controlador_reservas.actualizar_reserva(id, nombre, descripcion, precio, foto, ingredientes) 
                else: 
                    respuesta={"status":"Forbidden"}
                    code=403
            else:
                respuesta={"status":"Bad request"}
                code=401
        else:
            respuesta={"status":"Bad request"}
            code=401
    else:
        respuesta={"status":"Bad request"}
        code=401
    response= make_response(json.dumps(respuesta, cls=Encoder), code)
    return response