import mysql.connector
import pickle

class BaseDatos:
    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='cangrejo12',
                database='scandb'
            )
            self.cursor = self.conexion.cursor()
            self.verificar_conexion()
        except mysql.connector.Error as err:
            print(f"Error conectando a la base de datos: {err}")
    
    def verificar_conexion(self):
        """ Verifica si la conexión a la base de datos es correcta. """
        try:
            self.cursor.execute("SELECT DATABASE();")
            resultado = self.cursor.fetchone()
            print(f"Conectado a la base de datos: {resultado[0]}")
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")

    def agregar_usuario(self, nombre, apellido, edad, ocupacion, datos_oculares):
        try:
            if not nombre or not apellido or not edad or not ocupacion or not datos_oculares:
                print("Alguno de los campos está vacío o es inválido.")
                return

            # Serializa los datos oculares antes de guardarlos
            datos_serializados = pickle.dumps(datos_oculares)
            consulta = "INSERT INTO usuarios (nombre, apellido, edad, ocupacion, datos_oculares) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(consulta, (nombre, apellido, edad, ocupacion, datos_serializados))
            self.conexion.commit()

            print(f"Usuario {nombre} {apellido} agregado con éxito.")
        except mysql.connector.Error as e:
            print(f"Error al agregar usuario: {e}")

    def obtener_datos_oculares(self, nombre):
        """ Obtiene los datos oculares de un usuario por su nombre. """
        try:
            consulta = "SELECT datos_oculares FROM usuarios WHERE nombre = %s"
            self.cursor.execute(consulta, (nombre,))
            resultado = self.cursor.fetchone()

            if resultado:
                datos_oculares = pickle.loads(resultado[0])
                return datos_oculares
            else:
                print(f"No se encontraron datos oculares para el usuario: {nombre}")
                return None
        except Exception as e:
            print(f"Error al obtener datos oculares: {e}")
            return None

    # Nueva función para obtener todos los usuarios con sus datos oculares
    def obtener_todos_los_datos_oculares(self):
        """ Obtiene los datos oculares de todos los usuarios registrados. """
        try:
            consulta = "SELECT nombre, ocupacion, datos_oculares FROM usuarios"
            self.cursor.execute(consulta)
            resultados = self.cursor.fetchall()

            if resultados:
                usuarios = []
                for resultado in resultados:
                    nombre = resultado[0]
                    ocupacion = resultado[1]
                    datos_oculares = pickle.loads(resultado[2])
                    usuarios.append({
                        'nombre': nombre,
                        'ocupacion': ocupacion,
                        'datos_oculares': datos_oculares
                    })
                return usuarios
            else:
                print("No se encontraron usuarios registrados.")
                return []
        except Exception as e:
            print(f"Error al obtener los datos de los usuarios: {e}")
            return []

    def cerrar_conexion(self):
        """ Cierra la conexión con la base de datos. """
        try:
            if self.cursor:
                self.cursor.close()
            if self.conexion:
                self.conexion.close()
            print("Conexión con la base de datos cerrada.")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
