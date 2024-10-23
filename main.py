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

# Definimos las acciones que realizara antes de verificar_retina() antes de invocarlo
def verificar_retina():
    ventana_verificar = Toplevel()
    ventana_verificar.title("Verificación de Retina Automática")
    centrar_ventana(ventana_verificar, 950, 600)  # Opción para centrar pantalla
    try:
        ventana_verificar.iconbitmap("imagenes/loss.ico")
        ventana_verificar.configure(bg='#342d5a')
    except Exception as e:
        print(f"Error al cargar el icono: {e}")

    # Cargar la imagen de fondo
    imagen_fondo = Image.open("imagenes/fondo.png")
    imagen_fondo = imagen_fondo.resize((960, 600), Image.LANCZOS)  # Ajusta el tamaño al de la ventana
    fondo = ImageTk.PhotoImage(imagen_fondo)

    # Crear un Label para la imagen de fondo
    label_fondo = Label(ventana_verificar, image=fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)  # Expande la imagen para cubrir toda la ventana
    label_fondo.image = fondo  # Para evitar que Python elimine la imagen de la memoria

    label_instrucciones = Label(ventana_verificar, text="Mira a la cámara para comenzar la verificación automática", font=("Times New Roman", 27), bg='#342d5a', fg='white')
    label_instrucciones.pack(pady=20)

    # Función para capturar imagen y realizar la verificación
    def realizar_verificacion():
        usuarios = db.obtener_todos_los_datos_oculares()
        if not usuarios:
            messagebox.showerror("Error", "No se encontraron usuarios registrados.")
            ventana_verificar.destroy()
            mostrar_menu()
            return

        cap = cv2.VideoCapture(1)
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
                for usuario in usuarios:
                    fotos_almacenadas = usuario['datos_oculares']
                    for ojo_guardado in fotos_almacenadas:
                        similitud = comparar_imagenes(ojo_actual, ojo_guardado)
                        if similitud >= 0.85:  # Umbral de similitud
                            cap.release()
                            cv2.destroyAllWindows()
                            ventana_verificar.destroy()
                            mensaje_bienvenida(usuario['nombre'], usuario['ocupacion'])
                            return
            if time.time() - inicio_tiempo > 20:  # Límite de tiempo de 20 segundos
                cap.release()
                cv2.destroyAllWindows()
                ventana_verificar.destroy()
                messagebox.showwarning("Verificación", "No hubo coincidencias con los datos registrados.")
                mostrar_menu()
                return

            cv2.imshow("Verificación en Tiempo Real", frame)
            cv2.waitKey(1)

    realizar_verificacion()

    ventana_verificar.protocol("WM_DELETE_WINDOW", lambda: [ventana_verificar.destroy(), mostrar_menu()])
    ventana_verificar.mainloop()

# Definimos las funciones de captura y verificación de imágenes
def detectar_ojo(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    ojos = eye_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in ojos:
        ojo = frame[y:y+h, x:x+w]
        return cv2.resize(ojo, (100, 100))  # Redimensionamos para normalizar el tamaño
    return None

def capturar_imagen(nombre_usuario, apellido_usuario, edad_usuario, ocupacion_usuario, ventana_actual):
    if not nombre_usuario.strip() or not apellido_usuario.strip() or not edad_usuario.strip() or not ocupacion_usuario:
        messagebox.showwarning("Entrada Vacía", "Por favor, completa todos los campos.")
        return

    datos_existentes = db.obtener_datos_oculares(nombre_usuario)
    if datos_existentes:
        messagebox.showwarning("Usuario Existente", f"El usuario '{nombre_usuario}' ya está registrado.")
        return

    fotos = []
    max_captures = 4
    cap = cv2.VideoCapture(1)
    cv2.namedWindow("Registro de Ojos")
    cv2.resizeWindow("Registro de Ojos", 50, 50)

    if not cap.isOpened():
        messagebox.showerror("Error", "Hubo un error al abrir la cámara.")
        return

    messagebox.showinfo("Captura", "Capturando imágenes de tu ojo. Por favor, asegúrate de estar cerca de la cámara.")
    captured_encodings = 0

    while captured_encodings < max_captures:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "No se pudo capturar el cuadro.")
            break

        ojo = detectar_ojo(frame)
        if ojo is not None:
            for i in range(5, 0, -1):
                countdown_frame = frame.copy()
                cv2.putText(countdown_frame, f"Capturando en {i}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow(f"Captura de retina - {nombre_usuario}", countdown_frame)
                cv2.waitKey(1000)
            cv2.imshow(f"Captura de retina - {nombre_usuario}", ojo)
            cv2.waitKey(500)
            captured_encodings += 1
            fotos.append(ojo)
            messagebox.showinfo("Captura Exitosa", f"Imagen {captured_encodings} de {max_captures} capturada correctamente.")
        else:
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
    
    # Configurar la cámara si es necesario
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Cambiar a 1080p si lo deseas
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
                    if similitud >= 0.50:  # Umbral de similitud
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
    area.geometry("950x600")
    
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
