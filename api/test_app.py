import unittest
from app import app 
from flask import json

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configura el entorno de prueba"""
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def test_login(self):
        """Prueba de inicio de sesión con credenciales correctas"""
        response = self.client.post('/login', json={
            'usuario': 'admin',
            'clave': '1234'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful', response.get_data(as_text=True))

    def test_login_fallido(self):
        """Prueba de login con credenciales incorrectas"""
        response = self.client.post('/login', json={
            'usuario': 'admin',
            'clave': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)

    def test_registro(self):
        """Prueba de registro de usuario"""
        response = self.client.post('/register', json={
            'usuario': 'nuevo_usuario',
            'clave': 'password123',
            'perfil': 'cliente'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Registration successful', response.get_data(as_text=True))

    def test_subir_archivo(self):
        """Prueba de subida de archivos"""
        data = {
            'file': (open('test_file.txt', 'rb'), 'test_file.txt')
        }
        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)

    def test_ver_archivos(self):
        """Prueba de visualización de archivos"""
        response = self.client.get('/files')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)  # Debe devolver una lista

    def test_pedir_mesa(self):
        """Prueba de reserva de una mesa"""
        response = self.client.post('/reservar', json={
            'id_cliente': 1,
            'id_mesa': 1,
            'fecha': '2025-06-12',
            'hora': '19:00'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Reserva confirmada', response.get_data(as_text=True))

    def test_calcular_iva(self):
        """Prueba del cálculo del IVA"""
        response = self.client.post('/calcular-iva', json={'precio': 100, 'iva': 21})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['precio_final'], 121)  # 100 + 21% IVA

if __name__ == '__main__':
    unittest.main()
