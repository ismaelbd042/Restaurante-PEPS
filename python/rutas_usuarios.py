from __future__ import print_function
from __main__ import app
from flask import request, make_response
import json
import sys
from funciones_auxiliares import Encoder, sanitize_input, delete_session
import controlador_usuarios

@app.route("/login", methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        login_json = request.json
        if "username" in login_json and "password" in login_json:
            username = sanitize_input(login_json['username'])
            password = sanitize_input(login_json['password'])
            if isinstance(username, str) and isinstance(password, str) and len(username) < 50 and len(password) < 50:
                respuesta, code = controlador_usuarios.login_usuario(username, password)
            else:
                respuesta = {"status": "Bad parameters"}
                code = 401
        else:
            respuesta = {"status": "Bad request"}
            code = 401
    else:
        respuesta = {"status": "Bad request"}
        code = 401
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    return response

@app.route("/registro", methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        login_json = request.json
        if "username" in login_json and "password" in login_json and "profile" in login_json and "email" in login_json:
            username = sanitize_input(login_json['username'])
            password = sanitize_input(login_json['password'])
            profile = sanitize_input(login_json['profile'])
            email = sanitize_input(login_json['email'])
            if isinstance(username, str) and isinstance(password, str) and isinstance(profile, str) and len(username) < 50 and len(password) < 50:
                respuesta, code = controlador_usuarios.alta_usuario(username, password, profile, email)
            else:
                respuesta = {"status": "Bad parameters"}
                code = 401
        else:
            respuesta = {"status": "Bad request"}
            code = 401
    else:
        respuesta = {"status": "Bad request"}
        code = 401
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    return response

@app.route("/logout", methods=['GET'])
def logout():
    try:
        delete_session()
        ret = {"status": "OK"}
        code = 200
    except:
        ret = {"status": "ERROR"}
        code = 500
    response = make_response(json.dumps(ret), code)
    return response

