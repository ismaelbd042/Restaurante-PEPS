from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import datetime

# Configuración de Flask y Base de Datos
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@mariadb/peps"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "supersecreto"
app.config["UPLOAD_FOLDER"] = "uploads"

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Crear carpeta de uploads si no existe
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Modelo de Usuarios
class Usuario(db.Model):
    __tablename__ = "usuarios"
    usuario = db.Column(db.String(100), primary_key=True)
    clave = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(100), nullable=False)
    fechaUltimoAcceso = db.Column(db.Date)

# Modelo de Reservas
class Reserva(db.Model):
    __tablename__ = "reservas"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, nullable=False)
    id_mesa = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    lugar = db.Column(db.String(255), nullable=False)
    precio_reserva = db.Column(db.Numeric(9,2), nullable=False)
    estado = db.Column(db.String(50), default="pendiente")

# Rutas de autenticación
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = data.get("usuario")
    clave = data.get("clave")

    user = Usuario.query.filter_by(usuario=usuario, clave=clave).first()
    if user:
        token = create_access_token(identity=usuario, expires_delta=datetime.timedelta(hours=1))
        return jsonify({"message": "Inicio de sesión exitoso", "token": token}), 200
    return jsonify({"message": "Credenciales incorrectas"}), 401

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    usuario = data.get("usuario")
    clave = data.get("clave")

    if Usuario.query.get(usuario):
        return jsonify({"message": "Usuario ya existe"}), 400

    nuevo_usuario = Usuario(usuario=usuario, clave=clave, perfil="cliente", fechaUltimoAcceso=datetime.date.today())
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuario registrado correctamente"}), 201

@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "Sesión cerrada"}), 200

# Subida de archivos
@app.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No se envió ningún archivo"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    return jsonify({"message": "Archivo subido exitosamente"}), 201

# Listar archivos subidos
@app.route("/files", methods=["GET"])
@jwt_required()
def list_files():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return jsonify(files)

# Descargar un archivo específico
@app.route("/files/<filename>", methods=["GET"])
@jwt_required()
def get_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# Reservar mesa
@app.route("/reservar", methods=["POST"])
@jwt_required()
def reservar():
    data = request.json
    id_cliente = data.get("id_cliente")
    id_mesa = data.get("id_mesa")
    fecha = data.get("fecha")
    hora = data.get("hora")
    lugar = data.get("lugar")
    precio_reserva = data.get("precio_reserva")

    nueva_reserva = Reserva(
        id_cliente=id_cliente,
        id_mesa=id_mesa,
        fecha=fecha,
        hora=hora,
        lugar=lugar,
        precio_reserva=precio_reserva
    )

    db.session.add(nueva_reserva)
    db.session.commit()
    return jsonify({"message": "Reserva creada correctamente"}), 201

# Calcular IVA
@app.route("/calcular_iva", methods=["POST"])
def calcular_iva():
    data = request.json
    monto = data.get("monto")
    if monto is None or monto < 0:
        return jsonify({"message": "Monto inválido"}), 400

    iva = monto * 0.21
    total = monto + iva
    return jsonify({"iva": iva, "total": total})

# Inicializar la base de datos
with app.app_context():
    db.create_all()

# Ejecutar la API
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
