import unittest

IVA_TASA = 0.21  # Definir la tasa de IVA como una constante

def calculariva(importe):
    return importe * IVA_TASA

class TestCalcularIVA(unittest.TestCase):
    def test_calculariva_100(self):
        self.assertEqual(calculariva(100), 21)
    
    def test_calculariva_0(self):
        self.assertEqual(calculariva(0), 0)
    
    def test_calculariva_negativo(self):
        self.assertEqual(calculariva(-100), -21)

if __name__ == '__main__':
    unittest.main()