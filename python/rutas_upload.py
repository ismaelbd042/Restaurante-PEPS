from __future__ import print_function
from __main__ import app
from flask import request, make_response
import os
import json
import sys
from funciones_auxiliares import validar_session_normal  # Asegúrate de que esta función esté en funciones_auxiliares.py

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if validar_session_normal():  # Mantén la validación de sesión
            f = request.files['fichero']  # Archivo recibido en la solicitud
            user_input = request.form.get("nombre")  # Obtiene el nombre proporcionado en el formulario
            basepath = os.path.dirname(__file__)  # Ruta del archivo actual
            upload_path = os.path.join(basepath, '/apache/static', user_input)  # Ruta completa para guardar el archivo
            print('lugar' + upload_path, file=sys.stdout)  # Solo para debugging
            f.save(upload_path)  # Guarda el archivo en la ruta indicada
            respuesta = {"status": "OK"}
            code = 200
        else:
            respuesta = {"status": "Forbidden"}
            code = 403
    except Exception as e:
        print(f"Error al intentar cargar el archivo: {e}", file=sys.stderr)
        respuesta = {"status": "ERROR"}
        code = 500
    response = make_response(json.dumps(respuesta), code)
    return response

