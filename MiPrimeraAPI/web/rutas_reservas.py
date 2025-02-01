from flask import request, session
import json
import decimal
from __main__ import app
import controlador_reservas

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

@app.route("/reservas",methods=["GET"])
def reservas():
    reservas,code= controlador_reservas.obtener_reservas()
    return json.dumps(reservas, cls = Encoder),code

@app.route("/reserva/<id>",methods=["GET"])
def reserva_por_id(id):
    reserva,code = controlador_reservas.obtener_reserva_por_id(id)
    return json.dumps(reserva, cls = Encoder),code

@app.route("/reservas",methods=["POST"])
def guardar_reserva():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        reserva_json = request.json
        ret,code=controlador_reservas.insertar_reserva(reserva_json["nombre_Cliente"], reserva_json["lugar"], float(reserva_json["precio_reserva"]), reserva_json["foto_comida_reserva"])
    else:
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code

@app.route("/reserva/<id>", methods=["DELETE"])
def eliminar_juego(id):
    ret,code=controlador_reservas.eliminar_reserva(id)
    return json.dumps(ret), code

@app.route("/reservas", methods=["PUT"])
def actualizar_reserva():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        reserva_json = request.json
        ret,code=controlador_reservas.actualizar_reserva(reserva_json["id"],reserva_json["nombre_Cliente"], reserva_json["lugar"], float(reserva_json["precio_reserva"]),reserva_json["foto_comida_reserva"])
    else:
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code