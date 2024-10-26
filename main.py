#-.-.-.MAIN.PY-.-.-.-.--.-.-:IMPORTACIONES!-.-.-.--.--.-.-.-.--
import os
import tkinter as tk 
from tkinter import ttk
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import pickle
import time
from base import BaseDatos
from skimage.metrics import structural_similarity as ssim 

#-..-..-.-COMIENZA LAS INTERFACES-.-.-.-.-.
root = tk.Tk()
root.withdraw()

db = BaseDatos() #ESTABLECE ANTES LA CONECCIÓN CON LA BASE DE DATOS!

#-.-.-.--.-ENLISTAMOS TODAS LAS ACTIVIDADES QUE HARA EL USUARIO EN SU DIA A DIA.-.-.-.-.-.-.

actividades = {
    "Analista en Sistemas": [
        "Revisión de reportes         -7:00 am-",
        "Análisis de requerimientos   -9:00 am-",
        "Planificación de mejoras     -12:00 pm-",
        "Documentación                -13:00 pm-",
        "Monitoreo de sistemas        -18:10 pm-"
    ],
    "Diseñador": [
        "Creación de bocetos           -7:00 am-",
        "Diseño de interfaces          -9:30 am-",
        "Revisión de feedback          -13:00 pm-",
        "Colaboración con desarrollo   -14:00 pm-"
    ],
    "Desarrollador": [
        "Desarrollo de nuevas funcionalidades   -12:20 pm-",
        "Corrección de errores                  -14:00 pm-",
        "Revisión de código                     -18:00 pm-",
        "Implementación de pruebas              -19:40 pm-"
    ],
    "Tester": [
        "Pruebas de software                  -14:00 pm-",
        "Generación de reportes de errores    -16:00 pm-",
        "Automatización de pruebas            -17:50 pm-",
        "Revisión de correcciones             -19:00 pm-"
    ],
    "Encargados de limpieza": [
        "Limpieza en la segunda planta edificio 3      -7:00 am-",
        "Limpieza en la area de comida en anexo        -12:00 pm-",
        "Limpieza del baño primera plan                -2:00 pm-"
    ]
}
#-.-.-.--.-DEFINIMOS LOS HORARIOS DE ENTRADA Y SALIDA DE LOS USUARIOS!-.-.-.-.-.-.

horarios_entrada = {
    "Analista en Sistemas": "07:00",
    "Diseñador": "07:00",
    "Desarrollador": "12:00",
    "Tester": "14:00",
    "Encargados de limpieza": "7:00"
}
horarios_salida = {
    "Analista en Sistemas": "20:00",
    "Diseñador": "15:00",
    "Desarrollador": "21:00",
    "Tester": "20:00",
    "Encargados de limpieza": "14:00"
}

#-.--.--.CODIGO PARA HACER QUE LAS INTERFACES SE CENTREN--..-.--

def centrar_ventana(ventana, width, height):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    ventana.geometry(f'{width}x{height}+{x}+{y}')

def animar_boton(boton):
    def on_enter(event):
        boton.config(width=420, height=410, bg="#1f1a3b")  # CAMBIA EL TAMAÑO AL ACERCAR EL CURSOR AL BOTON
    def on_leave(event):
        boton.config(width=400, height=400, bg="SystemButtonFace")  # CUANDO EL CURSOR SE ALEJE REGRESA A SU TAMAÑO ORIGINAL.
    boton.bind("<Enter>", on_enter)
    boton.bind("<Leave>", on_leave)

#-.-.-.-.MOSTRARA UNA INTERFAZ CON UN VIDEO DE NUESTRO PROYECTO.-.-.-.-.-.-.

def mostrar_logo():
    logo_window = tk.Toplevel()
    logo_window.title("SCANEYE")
    centrar_ventana(logo_window, 1280, 700)
    try:
        logo_window.iconbitmap("imagenes/loss.ico")
    except Exception as e:
        print(f"Error al cargar el icono: {e}")
    video_label = tk.Label(logo_window)
    video_label.pack()

    cap = cv2.VideoCapture('imagenes/VIDEOINTRO1.mp4') #USAMOS CV2 AL IGUAL QUE CUANDO ACTIVAMOS AL CAMARA!

    def reproducir_video(): #CREAMO UNA FUNCIÓN ENCARGADA EN LA REPRODUCCIÓN DEL VIDEO
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame)
            frame_tk = ImageTk.PhotoImage(frame_pil)
            video_label.config(image=frame_tk)
            video_label.image = frame_tk
            logo_window.after(10, reproducir_video) # ESCRIBIMOS CUANTO QUEREMOS QUE DURE EL VIDEO
        else:
            cap.release()
            logo_window.destroy()
            mostrar_menu()

    reproducir_video()
    logo_window.mainloop()

#-.--.-.CREAMOS UN MENU, EN EL QUE EL USUARIO PODRA INTERACTUAR CON EL -..-.-.-.-.--.

def mostrar_menu():
    menu = Toplevel()
    menu.title("SCANEYE, LA CLAVE ESTA EN TUS OJOS")
    centrar_ventana(menu, 960, 600)
    
    try:
        menu.iconbitmap("imagenes/loss.ico") 
    except Exception as e:
        print(f"Error al cargar el icono: {e}")
    
    # DEFINIMOS UNA IMAGEN COMO FONDO
    imagen_fondo = Image.open("imagenes/fondo.png")
    imagen_fondo = imagen_fondo.resize((960, 600), Image.LANCZOS)  #AJUSTAMOS EL TAMAÑO DE LA INTERFAZ
    fondo = ImageTk.PhotoImage(imagen_fondo)

    # IMPLEMENTAMOS LA IMAGEN PARA CREAR UN LABEL EN EL QUE SE MOSTRARA LA IMAGEN
    label_fondo = Label(menu, image=fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)  # EXPANDE LA IMAGEN
    label_fondo.image = fondo  # EVITA QUE PYTHON PIERDA LA IMAGEN

    # COLOCAMOS LOS WIDGETS EN EL FONDO
    label = Label(menu, text="SCANEYE TE DA LA BIENVENIDA \n Elige la opción que desees", font=("Technovier Bold", 26), bg='#342d5a', fg='white')
    label.pack(pady=15)

    # CARGAMOS LAS IAMGENES PARA LUEGO IMPLEMENTARLAS EN EL BOTON
    imagen_ojo = Image.open("imagenes/scane.png")
    imagen_ojo = imagen_ojo.resize((410, 400), Image.LANCZOS)
    icono_ojo = ImageTk.PhotoImage(imagen_ojo)

    imagen_scan = Image.open("imagenes/verif.png")
    imagen_scan = imagen_scan.resize((410, 400), Image.LANCZOS)
    icono_scan = ImageTk.PhotoImage(imagen_scan)

    # CREAMOS COMO FUNCIONARAN LOS BOTONES EN EL MENU, UBICANDOLOS, AGREGANDO LA IMAGEN Y UN TAMAÑO AL BOTON
    # TAMBIEN A QUE INTERFAZ TE REDIGIRA CADA BOTON
    boton_registrar = Button(menu, image=icono_ojo, compound="top", width=410, height=400, command=lambda: [menu.withdraw(), registrar_retina()],
                         bg='#5d3b94', borderwidth=0, highlightthickness=0)
    boton_registrar.image = icono_ojo
    boton_registrar.pack(side=LEFT, padx=(50, 10))

    boton_verificar = Button(menu, image=icono_scan, compound="top", width=410, height=400, command=lambda: [menu.withdraw(), capturar_imagen_verificacion(menu)],
                         bg='#5d3b94', borderwidth=0, highlightthickness=0)
    boton_verificar.image = icono_scan
    boton_verificar.pack(side=LEFT, padx=(10, 20))

    # APLICAMOS LA ANIMACION A LOS BOTONES
    animar_boton(boton_registrar)
    animar_boton(boton_verificar)

    menu.protocol("WM_DELETE_WINDOW", root.destroy)
    menu.mainloop()

#-.-.-.- CONFIGURAMOS LA INTERFAZ DE REGISTRO -.-.-.-.-.-.-.-.

def registrar_retina():  
    ventana_registro = Toplevel()
    ventana_registro.title("Registro de Retina")
    centrar_ventana(ventana_registro, 950, 600)
    try:
        ventana_registro.iconbitmap("imagenes/loss.ico")
        ventana_registro.configure(bg='#342d5a')
    except Exception as e:
        print(f"Error al cargar el icono: {e}")
    
    # CARGAMOS NUEVAMENTE LA IMAGEN DE FONDO
    imagen_fondo = Image.open("imagenes/fondo.png")
    imagen_fondo = imagen_fondo.resize((960, 600), Image.LANCZOS) 
    fondo = ImageTk.PhotoImage(imagen_fondo)

    # APLICAMOS EL FONDO
    label_fondo = Label(ventana_registro, image=fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1) 
    label_fondo.image = fondo  

    Label(ventana_registro, text="SCANEYE te da la bienvenida! \n Ingresa tus datos para registrarte", font=("Times New Roman", 27), bg='#342d5a', fg='white').pack(pady=10)

    # CREAMOS EL PRIMER CUADRO DE TEXTO, NOMBRE, ESTABLECIENDO EL TIPO DE LETRA, COLOR Y TAMAÑO
    Label(ventana_registro, text="SU NOMBRE:", font=("Times New Roman", 15), bg='#342d5a', fg='white').pack(pady=(10, 0))
    entrada_nombre = Entry(ventana_registro, width=30, font=("Times New Roman", 18))
    entrada_nombre.pack(pady=10)

    # CREAMOS EL DE APELLIDO
    Label(ventana_registro, text="SU APELLIDO:", font=("Times New Roman", 15), bg='#342d5a', fg='white').pack(pady=(10, 0))
    entrada_apellido = Entry(ventana_registro, width=30, font=("Times New Roman", 18))
    entrada_apellido.pack(pady=10)
    
    # CREAMOS EL DE EDAD
    Label(ventana_registro, text="SU EDAD:", font=("Times New Roman", 15), bg='#342d5a', fg='white').pack(pady=(10, 0))
    entrada_edad = Entry(ventana_registro, width=30, font=("Times New Roman", 18))
    entrada_edad.pack(pady=10)

    #CREAMOS UN SELECCIONADOS, EN EL QUE EL USUARIO PODRA ELEGIR UE OCUPACIÓN REALIZA EN EL TRABAJO
    Label(ventana_registro, text="ELIGE TU OCUPACIÓN:", font=("Times New Roman", 15), bg='#342d5a', fg='white').pack(pady=(10, 0))
    ocupaciones = ["Analista en Sistemas", "Diseñador", "Desarrollador", "Tester", "Servicios de Limpieza"]
    ocupacion_seleccionada = StringVar()
    ocupacion_seleccionada.set(ocupaciones[0])
    menu_ocupacion = OptionMenu(ventana_registro, ocupacion_seleccionada, *ocupaciones)
    menu_ocupacion.pack(pady=10)

    # AGREGAMOS IMAGENES PARA QUE LOS BOTONES SEAN MÁS DINAMICOS
    imagen_capturar = Image.open("imagenes/B2.png").resize((100, 50))  # AJUSTAMOS UN TAMAÑO
    render_capturar = ImageTk.PhotoImage(imagen_capturar)

    imagen_regresar = Image.open("imagenes/B1.png").resize((100, 50))  # AJUSTAMOS UN TAMAÑO
    render_regresar = ImageTk.PhotoImage(imagen_regresar)

    # REDIMENCIONAMOS LOS BOTONES Y AGREGAMOS LA FUNCION DE LAS IMAGENES
    boton_capturar = Button(ventana_registro, image=render_capturar, command=lambda: capturar_imagen(
        entrada_nombre.get(), entrada_apellido.get(), entrada_edad.get(), ocupacion_seleccionada.get(), ventana_registro))
    boton_capturar.pack(side=LEFT, padx=10, pady=10)

    boton_regresar = Button(ventana_registro, image=render_regresar, command=lambda: [ventana_registro.destroy(), mostrar_menu()])
    boton_regresar.pack(side=RIGHT, padx=10, pady=10)

    ventana_registro.protocol("WM_DELETE_WINDOW", lambda: [ventana_registro.destroy(), mostrar_menu()])
    ventana_registro.mainloop()

# DEFINIMOS LAS ACCIONES QUE REALIZARA verificar_retina() ANTES DE INVOCARLO
def verificar_retina():
    ventana_verificar = Toplevel()
    ventana_verificar.title("Verificación de Retina Automática")
    centrar_ventana(ventana_verificar, 950, 600)  # Opción para centrar pantalla
    try:
        ventana_verificar.iconbitmap("imagenes/loss.ico")
        ventana_verificar.configure(bg='#342d5a')
    except Exception as e:
        print(f"Error al cargar el icono: {e}")

    # CARGA UNA IMAGEN DE FONDO
    imagen_fondo = Image.open("imagenes/fondo.png")
    imagen_fondo = imagen_fondo.resize((960, 600), Image.LANCZOS)  # AJUSTAMOS EL TAMAÑO
    fondo = ImageTk.PhotoImage(imagen_fondo)

    # CREAMOS NUEVAMENTE EL LABEL PARA LA IMAGEN
    label_fondo = Label(ventana_verificar, image=fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.image = fondo 

    #CREAMOS UN LABEL PARA INSTRUIR AL USUARIO 
    label_instrucciones = Label(ventana_verificar, text="Mira a la cámara para comenzar la verificación automática", font=("Times New Roman", 27), bg='#342d5a', fg='white')
    label_instrucciones.pack(pady=20)

    # CREAMOS LA FUNCIÓN PARA CAPTURAR Y VERIFICAR LA IMAGEN
    def realizar_verificacion():

        # OBTENEMOS TODOS LOS DATOS ALMACENADOS EN LA BASE DE DATOS
        usuarios = db.obtener_todos_los_datos_oculares()

        # SI NO HAY NINGUN USUARIO REGISTRADO MOSTRARA UN MENSAJE
        if not usuarios:
            messagebox.showerror("Error", "No se encontraron usuarios registrados.")
            ventana_verificar.destroy()
            mostrar_menu() #AL VER QUE NO HAY USUARIOS TE REDIRIGE AL MENU
            return
        
        # CONFIGURAMOS A LA CAMARA DE CAMO STUDIO
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():

            # SI NO PUEDE ABRIR LA CAMARA TE MOSTRARA UN ERROR
            messagebox.showerror("Error", "Hubo un error al abrir la cámara.")
            return
        
        # INFORMA AL USURIO UE EMPIEZA YA LA VERIFICACION PARA QUE ESTE PREPARADO!
        messagebox.showinfo("Verificación", "Verificando en tiempo real. Mira a la cámara.")
        inicio_tiempo = time.time() # GUARDA EL TIEMPO EN QUE SE INICIA LA VERIFICACIÓN

        # INICIAMOS UN BUCLE PARA CAPTURAR CUADROS DEL OJO EN TIEMPO REAL
        while True:
            ret, frame = cap.read() # CAPTURA UN CUADRO DE LA CAMARA
            if not ret:

                # SI NO ENCUENTRA UN CUADRO, MOSTRARA UN MENSAJE DE ERROR
                messagebox.showerror("Error", "No se pudo capturar el cuadro.")
                break

            # EMPEZAMOS LA FUNCIÓN DE DETECTAR EL OJO EN EL CUADRO
            ojo_actual = detectar_ojo(frame)
            if ojo_actual is not None:

                # COMPARA LOS OJOS CAPTURADOS CON LOS DEMAS DE CADA USUARIO
                for usuario in usuarios:
                    fotos_almacenadas = usuario['datos_oculares']
                    for ojo_guardado in fotos_almacenadas:

                        # COMPARA TODAS LAS IMAGENES DE LOS OJOS, BUSCANDO LAS SIMILITUDES ENTRE USUARIOS
                        similitud = comparar_imagenes(ojo_actual, ojo_guardado)
                        if similitud >= 0.80:  # CREAMOS UN UMBRAL DE SIMILITUD, ENTRE 0.05 A 0.50 DEJA ACCEDER A CUALQUIERA, PERO ENTRE 0.85 A 0.90 ES MAS ESTRICTO EN LA COMPARACIÓN
                            cap.release()
                            cv2.destroyAllWindows() 
                            ventana_verificar.destroy()
                            
                            # MOSTRAMOS UN MENSAJE DE BIENVENIDA AL USUARIO
                            mensaje_bienvenida(usuario['nombre'], usuario['ocupacion'])
                            return
            
            # SI PASA MAS DE 20 SEGUNDOS EL PORCESO DE VERIFICACIÓN TERMINA
            if time.time() - inicio_tiempo > 20:  # DEFINIMOS UN TIEMPO DE 20 SEGUNDOS
                cap.release()
                cv2.destroyAllWindows()
                ventana_verificar.destroy()

                # MOSTRAMOS UN MENSAJE DE ADVERTENCIA DE NO HUBO COINCIDENCIAS
                messagebox.showwarning("Verificación", "No hubo coincidencias con los datos registrados.")
                mostrar_menu() # Y TE VOLVERA AL MENU PRINCIPAL
                return
            
            # MUESTRA EL VIDEO DE LA CAMAR EN TIEMPO REAL
            cv2.imshow("Verificación en Tiempo Real", frame)
            cv2.waitKey(1)

    # INICIA LA VERIFICACION CUANDO SE ABRA LA VENTANA 
    realizar_verificacion()

    # SI EL USUARIO DECIDE SALIR DE LA VENTANA DE VERIFICACION, TE REGRESARA AL MENU
    ventana_verificar.protocol("WM_DELETE_WINDOW", lambda: [ventana_verificar.destroy(), mostrar_menu()])
    ventana_verificar.mainloop() # MANTENEMOS LA VENTANA ABIERTA

# CREAMOS LA FUNCION PARA DETECTAR EL OJO
def detectar_ojo(frame):

    # CONVERTIMOS LA IMAGEN CAPTURADA A ESCALA DE GRISES, LO CUAL FACILITARA LA VERIFICACION
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # CARGAMOS UN CLASIFICADOR HaarsCascade PREENTRENADO, PARA DETECTAR ZONAS ESPECIFICAS DEL OJO
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # DETECTAMOS TODAS LAS REGIONES DEL OJO DE CADA IMAGEN
    ojos = eye_cascade.detectMultiScale(gray, 1.3, 5)

    # SI DETECTA UN OJO, CORTAMOS LA IMAGEN PARA QUE SOLAMENTE SE VEA EL OJO
    for (x, y, w, h) in ojos:
        ojo = frame[y:y+h, x:x+w]
        return cv2.resize(ojo, (100, 100))  # REDIMENCIONAMOS EL TAMAÑO DE LA IMAGEN QUE TENDRA EL OJO
    
    # SI NO TE DETECTA UN OJO, REGRESA UN NONE
    return None

# CREAMOS LA FUNCIÓN PARA CAPTURAR LA IMAGENES DE NUEVOS USARIOS Y ENVIAR LOS REGISTROS A LA BASE DE DATOS
def capturar_imagen(nombre_usuario, apellido_usuario, edad_usuario, ocupacion_usuario, ventana_actual):

    # VALIDAMOS QUE TODOS LOS CAMPOS ESTEN LLENOS Y NO ESTEN VACIOS
    if not nombre_usuario.strip() or not apellido_usuario.strip() or not edad_usuario.strip() or not ocupacion_usuario:
        messagebox.showwarning("Entrada Vacía", "Por favor, completa todos los campos.")
        return
    
    # CREAMOS UNA VERIFICACION, EN QUE NO HAYA DATOS SIMILARES EN NOMBRE Y APELLIDO
    datos_existentes = db.obtener_datos_oculares(nombre_usuario)
    if datos_existentes:
        messagebox.showwarning("Usuario Existente", f"El usuario '{nombre_usuario}' ya está registrado.")
        return
    
    # INICIAMOS EL PROCESO PARA PODER ALMACENAR LAS IMAGENES
    fotos = []   # CREAMOS UNA LISTA PARA LAS FOTOS
    max_captures = 4   # ESTABLECEMOS CUANTAS FOTOS SE VAN A TOMAR
    cap = cv2.VideoCapture(1)   # ABRE LA CAMARA DE CAMO STUDIO
    cv2.namedWindow("Registro de Ojos")    # CREAMOS UNA VENTANA PARA QUE PUEDA VISUALIZAR COMO QUEDARAN LAS IMAGENES
    cv2.resizeWindow("Registro de Ojos", 50, 50)  # LE DAMOS UN TAMAÑO PEQUEÑO A LA VENTANA

    # SE VERIFICA SI HAY ACCESO O NO A LA CAMARA
    if not cap.isOpened():
        messagebox.showerror("Error", "Hubo un error al abrir la cámara.")
        return
    
    # GENERAMOS UNA NOTIFICACIÓN PARA QUE EL USUARIO ESTE PREPARADO
    messagebox.showinfo("Captura", "Capturando imágenes de tu ojo. Por favor, asegúrate de estar cerca de la cámara.")
    captured_encodings = 0   # SE CREA UN CONTADOR DE IMAGENES

    # GENERAMOS UN CICLO DE CAPTURA DE IMAGENES, HASTA ACABAR LA CANTIDAD DE CAPTURAS PROPUESTAS
    while captured_encodings < max_captures:
        ret, frame = cap.read() # EMPEZARA A CAPTURAR EL CUADRO DE LA CAMARA
        if not ret:
            messagebox.showerror("Error", "No se pudo capturar el cuadro.")
            break

        # INTENTA DETECTAR EL OJO EN EL CUADRO CAPTURADO
        ojo = detectar_ojo(frame)
        if ojo is not None:

            # CREAMOS UNA CUENTA REGRESIVA
            for i in range(5, 0, -1):
                countdown_frame = frame.copy()
                cv2.putText(countdown_frame, f"Capturando en {i}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow(f"Captura de retina - {nombre_usuario}", countdown_frame)
                cv2.waitKey(1000)   # SE ESPERA UN SEGUNDO ENTRE CADA NUMERO DE LA CUENTA REGRESIVA

            cv2.imshow(f"Captura de retina - {nombre_usuario}", ojo) # MOSTRAREMOS LA IMAGEN DEL OJO, EN LA VENTANA PEQUEÑA
            cv2.waitKey(500)  # ESPERAMOS 5 milisegundos ANTES DE CONTINUAR EL PROCESO
            captured_encodings += 1  # AUMENTAMOS EL CONTADOR DE LAS IMAGENES CAPTURADAS, HASTA LLEGAR A LA ULTIMA FOTO ( EN ESTE CASO A LA 4)
            fotos.append(ojo)  # AGREGAMOS LAS IMAGENES A LA LISTA
            messagebox.showinfo("Captura Exitosa", f"Imagen {captured_encodings} de {max_captures} capturada correctamente.")
        else:

            # SI NO SE ENCUENTRA EL OJO, MOSTRAREMOS UNA ADVERTENCIAS
            messagebox.showwarning("No Se Detectó un Ojo", "Intenta de nuevo, asegúrate de estar en una buena posición.")
            continue

    cap.release()
    cv2.destroyAllWindows()
    ventana_actual.destroy()

    if len(fotos) == max_captures:
        datos_serializados = pickle.dumps(fotos)
        db.agregar_usuario(nombre_usuario, apellido_usuario, edad_usuario, ocupacion_usuario, datos_serializados)
        messagebox.showinfo("Registro Completo", f"Usuario '{nombre_usuario} {apellido_usuario}' registrado exitosamente.")
    else:
        messagebox.showwarning("Registro Incompleto", "No se capturaron suficientes imágenes. Intenta de nuevo.")

    mostrar_menu()

def comparar_imagenes(imagen1, imagen2):
    # Convertimos las imágenes a escala de grises si es necesario
    if len(imagen1.shape) == 3:
        imagen1 = cv2.cvtColor(imagen1, cv2.COLOR_BGR2GRAY)
    if len(imagen2.shape) == 3:
        imagen2 = cv2.cvtColor(imagen2, cv2.COLOR_BGR2GRAY)
    
    # Calculamos la similitud estructural (SSIM)
    score, _ = ssim(imagen1, imagen2, full=True)
    return score

def capturar_imagen_verificacion(ventana_actual):
    # Obtener todos los usuarios registrados con sus datos oculares
    datos_usuarios = db.obtener_todos_los_datos_oculares()  # Obtener todos los datos de los usuarios
    
    if not datos_usuarios:
        messagebox.showerror("Verificación", "No hay usuarios registrados para verificar.")
        ventana_actual.destroy()
        mostrar_menu()
        return
    
    cap = cv2.VideoCapture(1)
    
    # CONFIGURAMOS LA CAMRA DE CAMO STUDIO DEPENDIENTEMENTE LA CALIDAD DEL LENTE
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # DE MOMENTO DEJAMOS 1080p
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    if not cap.isOpened():
        messagebox.showerror("Error", "Hubo un error al abrir la cámara.")
        return

    messagebox.showinfo("Verificación", "Verificando en tiempo real. Mira a la cámara.")

    inicio_tiempo = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "No se pudo capturar el cuadro.")
            break

        ojo_actual = detectar_ojo(frame)
        if ojo_actual is not None:
            for usuario in datos_usuarios:
                fotos_almacenadas = pickle.loads(usuario['datos_oculares'])  # Deserializamos las imágenes almacenadas
                for ojo_guardado in fotos_almacenadas:
                    similitud = comparar_imagenes(ojo_actual, ojo_guardado)
                    if similitud >= 0.65:  # Umbral de similitudes
                        cap.release()
                        cv2.destroyAllWindows()
                        ventana_actual.destroy()
                        mensaje_bienvenida(usuario['nombre'], usuario['ocupacion'])  # Mostrar bienvenida con nombre y ocupación
                        return
        if time.time() - inicio_tiempo > 20:
            cap.release()
            cv2.destroyAllWindows()
            ventana_actual.destroy()
            messagebox.showwarning("Verificación", "No hubo coincidencias con los datos registrados.")
            mostrar_menu()
            return

        cv2.imshow("Verificación en Tiempo Real", frame)
        cv2.waitKey(1)

def mensaje_bienvenida(nombre_usuario, ocupacion_usuario):
    messagebox.showinfo("Bienvenido", f"Bienvenido, {nombre_usuario}!")
    abrir_area_trabajo(nombre_usuario, ocupacion_usuario)

def abrir_area_trabajo(nombre_usuario, ocupacion_usuario):
    area = Toplevel()
    area.title(f"Área de Trabajo - {nombre_usuario}")
    centrar_ventana(area, 960, 600)
    
    try: 
        area.iconbitmap("imagenes/loss.ico")
    except Exception as e:
        print(f"Error al cargar el icono: {e}")

    label = Label(area, text=f"Actividades de Trabajo de {ocupacion_usuario}", font=("Technovier Bold", 20))
    label.pack(pady=20)

    # Obtener hora actual para verificar la entrada
    hora_actual = datetime.now().strftime("%H:%M")
    hora_entrada_correcta = horarios_entrada.get(ocupacion_usuario)
    hora_salida_correcta = horarios_salida.get(ocupacion_usuario)

    # Verificar si la persona llegó temprano, a tiempo o tarde
    entrada_label = Label(area, text=f"Hora de Entrada: {hora_actual}")
    entrada_label.pack()

    if hora_actual < hora_entrada_correcta:
        entrada_label.config(fg="green")
    elif hora_actual == hora_entrada_correcta:
        entrada_label.config(fg="orange")
    else:
        entrada_label.config(fg="red")

    salida_label = Label(area, text=f"Hora de Salida: {hora_salida_correcta}", fg="black")
    salida_label.pack()

    # Crear la tabla de actividades
    tabla_frame = Frame(area)
    tabla_frame.pack(pady=20)

    tabla = ttk.Treeview(tabla_frame, columns=("Actividad"), show="headings", height=10)
    tabla.heading("Actividad", text="Actividades del Día")
    tabla.column("Actividad", width=400)

    # Agregar las actividades según la ocupación
    actividades_usuario = actividades.get(ocupacion_usuario, actividades["Encargados de limpieza"])
    for actividad in actividades_usuario:
        tabla.insert("", "end", values=(actividad,))

    tabla.pack()

    area.protocol("WM_DELETE_WINDOW", lambda: [area.destroy(), mostrar_menu()])
    area.mainloop()

# Iniciar directamente en el hilo principal
if __name__ == "__main__":
    mostrar_logo()
    root.mainloop()
