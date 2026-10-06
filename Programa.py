from datetime import datetime
import unittest
import sys
# =========================
# PACIENTE
# =========================

class Paciente:
    def __init__(self, dni, nombre, edad, sintoma):
        self.dni = dni
        self.nombre = nombre
        self.edad = edad
        self.sintoma = sintoma

    def dni_oculto(self):
        return "*****" + self.dni[-3:]

# =========================
# REGISTRO
# =========================

class Registro:
    def __init__(self):
        self.citas = []

    def agregar(self, paciente, fecha, hora):
        if len(self.citas) == 3:
            raise ValueError("Solo se permiten 3 citas.")
        self.citas.append((paciente, fecha, hora))

    def existe_dni(self, dni):
        return any(p.dni == dni for p, _, _ in self.citas)

    def mostrar(self):
        if not self.citas:
            print("\nNo hay citas.")
            return

        for i, (p, fecha, hora) in enumerate(self.citas, 1):
            print(f"""
CITA {i}
DNI: {p.dni_oculto()}
Nombre: {p.nombre}
Edad: {p.edad}
Síntoma: {p.sintoma}
Fecha: {fecha}
Hora: {hora}
""")


# =========================
# VALIDACIONES
# =========================

def validar_dni(dni):
    if len(dni) != 8 or not dni.isdigit():
        raise ValueError("El DNI debe tener 8 números.")
    return dni


def validar_nombre(nombre):
    if not nombre.strip() or not all(c.isalpha() or c.isspace() for c in nombre):
        raise ValueError("Ingrese un nombre válido.")
    return nombre


def validar_edad(edad):
    if not edad.isdigit() or not 1 <= int(edad) <= 99:
        raise ValueError("La edad debe estar entre 1 y 99.")
    return int(edad)


def validar_fecha(fecha):
    try:
        f = datetime.strptime(fecha, "%d/%m/%Y")
        if f.year != 2026:
            raise ValueError
        return fecha
    except ValueError:
        raise ValueError("Use una fecha válida de 2026.")


def validar_hora(hora):
    try:
        return datetime.strptime(hora, "%H:%M").strftime("%I:%M %p")
    except ValueError:
        raise ValueError("Use HH:MM.")


def validar_sintoma(sintoma):
    if not sintoma.strip():
        raise ValueError("El síntoma no puede estar vacío.")
    return sintoma


def pedir(mensaje, validar):
    while True:
        try:
            return validar(input(mensaje))
        except ValueError as e:
            print("Error:", e)


# =========================
# REGISTRAR CITA
# =========================

def registrar_cita(registro):
    print("\n--- REGISTRO DE CITA ---")

    while True:
        dni = pedir("DNI: ", validar_dni)

        if not registro.existe_dni(dni):
            break

        print("Ese DNI ya tiene una cita.")

    nombre = pedir("Nombre: ", validar_nombre)
    edad = pedir("Edad: ", validar_edad)
    sintoma = pedir("Síntoma: ", validar_sintoma)
    fecha = pedir("Fecha (dd/mm/2026): ", validar_fecha)
    hora = pedir("Hora (HH:MM): ", validar_hora)

    registro.agregar(
        Paciente(dni, nombre, edad, sintoma),
        fecha,
        hora
    )

    print("✓ Cita registrada.")


def registrar_citas(registro):
    disponibles = 3 - len(registro.citas)

    if not disponibles:
        print("Ya se registraron las 3 citas.")
        return

    while True:
        try:
            cantidad = int(input(f"¿Cuántas citas? (1-{disponibles}): "))
            if 1 <= cantidad <= disponibles:
                break
        except ValueError:
            pass

        print("Ingrese una cantidad válida.")

    for _ in range(cantidad):
        registrar_cita(registro)


# =========================
# FILTRO DE ADULTOS
# =========================

def mostrar_adultos(registro):
    pacientes = [p for p, _, _ in registro.citas]
    adultos = list(filter(lambda p: p.edad >= 18, pacientes))

    print("\n--- PACIENTES ADULTOS ---")

    if not adultos:
        print("No hay pacientes adultos.")
        return

    for p in adultos:
        print(f"{p.dni_oculto()} | {p.nombre} | {p.edad} años")


# =========================
# PROGRAMA
# =========================

def main():
    registro = Registro()

    while True:
        print("""
========================
    SISTEMA RURAL - PE
========================
1. Registrar cita
2. Ver citas
3. Ver pacientes adultos
4. Salir
""")

        opcion = input("Opción: ")

        if opcion == "1":
            registrar_citas(registro)
        elif opcion == "2":
            registro.mostrar()
        elif opcion == "3":
            mostrar_adultos(registro)
        elif opcion == "4":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida.")


# =========================
# PRUEBAS UNITTEST
# =========================

class TestSistema(unittest.TestCase):

    def test_dni(self):
        self.assertEqual(validar_dni("12345678"), "12345678")

    def test_dni_mal(self):
        with self.assertRaises(ValueError):
            validar_dni("123")

    def test_nombre(self):
        self.assertEqual(validar_nombre("Ana Perez"), "Ana Perez")

    def test_nombre_mal(self):
        with self.assertRaises(ValueError):
            validar_nombre("Ana123")

    def test_edad(self):
        self.assertEqual(validar_edad("20"), 20)

    def test_edad_mal(self):
        with self.assertRaises(ValueError):
            validar_edad("100")

    def test_fecha(self):
        self.assertEqual(validar_fecha("15/10/2026"), "15/10/2026")

    def test_hora(self):
        self.assertEqual(validar_hora("14:30"), "02:30 PM")

    def test_registro(self):
        r = Registro()
        r.agregar(Paciente("12345678", "Ana", 20, "Fiebre"),
                  "15/10/2026", "02:30 PM")
        self.assertEqual(len(r.citas), 1)

    def test_adultos(self):
        pacientes = [
            Paciente("12345678", "Ana", 20, "Fiebre"),
            Paciente("87654321", "Luis", 16, "Tos")
        ]
        adultos = list(filter(lambda p: p.edad >= 18, pacientes))
        self.assertEqual(len(adultos), 1)


# =========================
# EJECUCIÓN
# =========================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]])
    else:
        main()