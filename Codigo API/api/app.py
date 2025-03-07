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
    nombre_cliente = db.Column(db.String(255), nullable=False)
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

@app.route("/reservas", methods=["GET"])
@jwt_required()
def listar_reservas():
    reservas = Reserva.query.all()
    reservas_json = [
        {
            "id": r.id,
            "nombre_cliente": r.nombre_cliente,
            "id_mesa": r.id_mesa,
            "fecha": str(r.fecha),
            "hora": str(r.hora),
            "lugar": r.lugar,
            "precio_reserva": float(r.precio_reserva),
            "estado": r.estado
        }
        for r in reservas
    ]
    return jsonify(reservas_json)

# Obtener datos de una reserva por ID
@app.route("/reserva/<int:id>", methods=["GET"])
@jwt_required()
def obtener_reserva(id):
    reserva = Reserva.query.get(id)
    if reserva:
        return jsonify({
            "id": reserva.id,
            "nombre_cliente": reserva.nombre_cliente,
            "id_mesa": reserva.id_mesa,
            "fecha": str(reserva.fecha),
            "hora": str(reserva.hora),
            "lugar": reserva.lugar,
            "precio_reserva": float(reserva.precio_reserva),
            "estado": reserva.estado
        })
    else:
        return jsonify({"message": "Reserva no encontrada"}), 404

# Crear nueva reserva
@app.route("/reserva", methods=["POST"])
def crear_reserva():
    data = request.json

    # Extraer datos del cuerpo de la solicitud
    nombre_cliente = data.get("nombre_cliente")
    lugar = data.get("lugar")
    precio_reserva = data.get("precio_reserva")
    foto_comida_reserva = data.get("foto_comida_reserva")
    fecha = data.get("fecha")
    hora = data.get("hora")

    # Validar que los datos requeridos estén presentes
    if not nombre_cliente or not lugar or not precio_reserva or not foto_comida_reserva or not fecha or not hora:
        return jsonify({"status": "ERROR", "message": "Todos los campos son requeridos"}), 400

    # Crear nueva reserva
    nueva_reserva = Reserva(
        nombre_cliente=nombre_cliente,
        lugar=lugar,
        precio_reserva=precio_reserva,
        foto_comida_reserva=foto_comida_reserva,
        fecha=datetime.datetime.strptime(fecha, '%Y-%m-%d').date(),
        hora=datetime.datetime.strptime(hora, '%H:%M').time()
    )

    # Añadir la nueva reserva a la base de datos
    db.session.add(nueva_reserva)
    db.session.commit()

    # Retornar una respuesta exitosa
    return jsonify({"status": "OK", "message": "Reserva creada correctamente"}), 201

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
