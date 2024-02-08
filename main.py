import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime


# Configuración de la conexión a la base de datos
nombre_db = 'pythoncrud'
dsn_name = 'pythonCrud'

# Funciones CRUD
def conectar():
    try:
        connection = pyodbc.connect('DSN={}'.format(dsn_name))
        connection.execute('USE {}'.format(nombre_db))
        return connection
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        return None

def crear_usuario(connection, nombre, apellido, email, fecha_nacimiento, genero):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, apellido, email, fecha_nacimiento, genero) VALUES (?, ?, ?, ?, ?)", nombre, apellido, email, fecha_nacimiento, genero)
        connection.commit()  # Asegúrate de realizar el commit después de la inserción
        cursor.close()
        messagebox.showinfo("Información", "Usuario creado exitosamente.")
        limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear usuario: {e}")

def obtener_usuarios(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        return usuarios
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener usuarios: {e}")
        return None

def actualizar_usuario(connection, user_id, nombre, apellido, email, fecha_nacimiento, genero):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE usuarios SET nombre = ?, apellido = ?, email = ?, fecha_nacimiento = ?, genero = ? WHERE id = ?", nombre, apellido, email, fecha_nacimiento, genero, user_id)
        connection.commit()  # Asegúrate de realizar el commit después de la actualización
        cursor.close()
        messagebox.showinfo("Información", "Usuario actualizado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar usuario: {e}")

def eliminar_usuario(connection, user_id):
    respuesta = messagebox.askokcancel("Confirmar Eliminación", "¿Estás seguro de que quieres eliminar este usuario?")
    if not respuesta:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", user_id)
        connection.commit()  # Asegúrate de realizar el commit después de la eliminación
        cursor.close()
        messagebox.showinfo("Información", "Usuario eliminado exitosamente.")
        limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar usuario: {e}")

# Funciones de la interfaz gráfica
def btn_crear_click():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    email = entry_email.get()
    fecha_nacimiento = entry_fecha_nacimiento.get()
    genero = entry_genero.get()
    if nombre and email and apellido and fecha_nacimiento and genero:
        crear_usuario(conexion, nombre, apellido, email, fecha_nacimiento, genero)
        actualizar_lista_usuarios()
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingrese todos los campos. Son obligatorios.")

def btn_actualizar_click():
    selected_item = tree.selection()
    if selected_item:
        user_id = tree.item(selected_item, 'values')[0]
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        email = entry_email.get()
        fecha_nacimiento = entry_fecha_nacimiento.get()
        genero = entry_genero.get()
        if nombre and email and apellido and fecha_nacimiento and genero:
            actualizar_usuario(conexion, int(user_id), nombre, apellido, email, fecha_nacimiento, genero)
            actualizar_lista_usuarios()
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el nombre y el correo electrónico del usuario.")
    else:
        messagebox.showwarning("Advertencia", "Seleccione un usuario de la lista para actualizar.")

def btn_eliminar_click():
    selected_item = tree.selection()
    if selected_item:
        user_id = tree.item(selected_item, 'values')[0]
        eliminar_usuario(conexion, int(user_id))
        actualizar_lista_usuarios()
    else:
        messagebox.showwarning("Advertencia", "Seleccione un usuario de la lista para eliminar.")

def actualizar_lista_usuarios():
    tree.delete(*tree.get_children())  # Limpiar el Treeview antes de actualizar
    usuarios = obtener_usuarios(conexion)
    if usuarios:
        for usuario in usuarios:
            tree.insert("", tk.END, values=(usuario.id, usuario.nombre, usuario.apellido, usuario.email, usuario.fecha_nacimiento, usuario.genero))


# Nueva función para limpiar campos
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_fecha_nacimiento.delete(0, tk.END)
    entry_genero.set(opciones_genero[0])  # Establece el valor por defecto


# Nueva función para llenar los campos al seleccionar un usuario
def seleccionar_usuario(event):
    selected_item = tree.selection()
    if selected_item:
        usuario_seleccionado = tree.item(selected_item, 'values')
        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_fecha_nacimiento.delete(0, tk.END)
        entry_genero.set(opciones_genero[0])  # Establece el valor por defecto
        if usuario_seleccionado:
            entry_nombre.insert(0, usuario_seleccionado[1])  # Nombre
            entry_apellido.insert(0, usuario_seleccionado[2])  # Apellido
            entry_email.insert(0, usuario_seleccionado[3])   # Email
            entry_fecha_nacimiento.insert(0, usuario_seleccionado[4])  # Fecha Nacimiento
            entry_genero.set(usuario_seleccionado[5])  # Género


def mostrar_calendario(entry_fecha):
    # Crear una ventana emergente para el calendario
    popup = tk.Toplevel(app)
    popup.wm_title("Calendario")

    # Crear un objeto Calendar y asociarlo a la ventana emergente
    cal = Calendar(popup, selectmode="day", year=2024, month=2, day=1)
    cal.pack(pady=20)

    # Función para actualizar la entrada con la fecha seleccionada y cerrar la ventana emergente
    def seleccionar_fecha():
        fecha_seleccionada = cal.get_date()
        fecha_formateada = datetime.strptime(fecha_seleccionada, "%m/%d/%y").strftime("%Y-%m-%d")
        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, fecha_formateada)
        popup.destroy()

    # Botón para seleccionar la fecha
    btn_seleccionar = ttk.Button(popup, text="Seleccionar", command=seleccionar_fecha)
    btn_seleccionar.pack(pady=10)


# Crear la interfaz gráfica
app = tk.Tk()
app.title("CRUD de Usuarios")
app.geometry("1000x600")  # Ajusta el tamaño de la ventana principal
app.configure(bg="#444")  # Cambia el color de fondo de la ventana principal a gris oscuro
# Bloqueamos para que no se pueda cambiar el tamaño de la ventana
app.resizable(0, 0)

# Configuración de estilo
style = ttk.Style()
style.configure("Dark.TLabel", foreground="white", background="#333", font=("Helvetica", 12))
style.configure("Dark.TEntry", fieldbackground="#333", foreground="black", font=("Helvetica", 12))
style.configure("Dark.TButton", foreground="black", background="#FFD700", font=("Helvetica", 12))

# Crear y posicionar widgets
label_nombre = ttk.Label(app, text="Nombre:", style="Dark.TLabel")
label_nombre.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

entry_nombre = ttk.Entry(app, style="Dark.TEntry")
entry_nombre.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

label_apellido = ttk.Label(app, text="Apellido:", style="Dark.TLabel")
label_apellido.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

entry_apellido = ttk.Entry(app, style="Dark.TEntry")
entry_apellido.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

label_email = ttk.Label(app, text="Email:", style="Dark.TLabel")
label_email.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

entry_email = ttk.Entry(app, style="Dark.TEntry")
entry_email.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

label_fecha_nacimiento = ttk.Label(app, text="Fecha nacimiento:", style="Dark.TLabel")
label_fecha_nacimiento.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

# Nuevo campo de entrada de tipo fecha
entry_fecha_nacimiento = ttk.Entry(app, style="Dark.TEntry", foreground="black")
entry_fecha_nacimiento.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

# Botón para mostrar el calendario y seleccionar la fecha
btn_seleccionar_fecha = ttk.Button(app, text="Seleccionar Fecha", command=lambda: mostrar_calendario(entry_fecha_nacimiento), style="Dark.TButton")
btn_seleccionar_fecha.grid(row=3, column=2, padx=10, pady=5, sticky=tk.W)

label_genero = ttk.Label(app, text="Género:", style="Dark.TLabel")
label_genero.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

opciones_genero = ["Masculino", "Femenino"]
entry_genero = ttk.Combobox(app, values=opciones_genero, style="Dark.TCombobox")
entry_genero.set(opciones_genero[0])  # Establece el valor por defecto
entry_genero.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W+tk.E)  # Añade tk.E a sticky para expandir el widget a la derecha

btn_crear = ttk.Button(app, text="Crear Usuario", command=btn_crear_click, style="Dark.TButton")
btn_crear.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky=tk.EW)

# Treeview para mostrar datos de la tabla por columnas
columns = ("ID", "Nombre", "Apellido", "Email", "Fecha Nacimiento", "Género")
tree = ttk.Treeview(app, columns=columns, show="headings", selectmode="browse")
tree.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky=tk.NSEW)

# Configuración de encabezados de columnas
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor=tk.CENTER)  # Ajusta el ancho de las columnas según sea necesario

# Configuración de eventos al seleccionar un elemento en el Treeview
tree.bind("<<TreeviewSelect>>", seleccionar_usuario)

# Nuevo botón para limpiar campos
btn_limpiar = ttk.Button(app, text="Limpiar Campos", command=limpiar_campos, style="Dark.TButton")
btn_limpiar.grid(row=7, column=2, pady=10, padx=10, sticky=tk.EW)  # Ajusta la posición del botón limpiar y sticky

# Ajusta la posición y columnspan de los botones actualizar y eliminar
btn_actualizar = ttk.Button(app, text="Actualizar Usuario", command=btn_actualizar_click, style="Dark.TButton")
btn_actualizar.grid(row=7, column=0, pady=10, padx=10, sticky=tk.EW)  # Ajusta la posición y sticky

btn_eliminar = ttk.Button(app, text="Eliminar Usuario", command=btn_eliminar_click, style="Dark.TButton")
btn_eliminar.grid(row=7, column=1, pady=10, padx=10, sticky=tk.EW)  # Ajusta la posición y sticky

app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=1)
app.columnconfigure(2, weight=1)
app.rowconfigure(6, weight=1)
app.grid_columnconfigure(1, weight=1)  # Añade esta línea para hacer que la columna 1 se expanda y llene el espacio disponible

# Conectar a la base de datos
conexion = conectar()

# Actualizar la lista de usuarios al iniciar la aplicación
if conexion:
    actualizar_lista_usuarios()

# Ejecutar la aplicación
app.mainloop()
