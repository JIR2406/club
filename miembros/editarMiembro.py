import customtkinter as ctk
from tkinter import messagebox

class EditarMiembroScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.current_student = None
        self.create_widgets()
        
    def create_widgets(self):
        """Crea todos los componentes de la interfaz"""
        # Título
        ctk.CTkLabel(
            self.frame,
            text="Editar Miembro",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        # Panel de búsqueda
        search_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        # Campo de búsqueda
        self.search_var = ctk.StringVar()
        ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Buscar por código, nombre o apellido...",
            width=300
        ).pack(side="left", padx=(0, 10))
        
        # Botones de búsqueda
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            width=100,
            command=self.buscar_estudiantes
        ).pack(side="left", padx=5)
        
        # Lista de resultados
        self.results_frame = ctk.CTkScrollableFrame(self.frame, height=150)
        self.results_frame.pack(fill="x", padx=20, pady=10)
        
        # Formulario de edición
        self.form_frame = ctk.CTkFrame(self.frame)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botones de acción
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Guardar Cambios",
            command=self.guardar_cambios
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancelar",
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=self.cerrar
        ).pack(side="left", padx=10)
        
        # Inicialmente ocultar el formulario
        self.mostrar_formulario(False)
    
    def buscar_estudiantes(self):
        """Busca estudiantes en la base de datos"""
        termino = self.search_var.get().strip()
        
        # Limpiar resultados anteriores
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        if not termino:
            messagebox.showwarning("Búsqueda vacía", "Ingrese un código o nombre para buscar")
            return
        
        # Obtener resultados de la base de datos
        resultados = self.obtener_estudiantes_db(termino)
        
        if not resultados:
            ctk.CTkLabel(
                self.results_frame,
                text="No se encontraron estudiantes",
                font=ctk.CTkFont(size=12)
            ).pack(pady=10)
            return
        
        # Mostrar resultados
        for estudiante in resultados:
            student_frame = ctk.CTkFrame(self.results_frame)
            student_frame.pack(fill="x", pady=2)
            
            # Mostrar información básica
            info_text = f"{estudiante['codigo_estudiante']} - {estudiante['nombre']} {estudiante['apPat']}"
            if estudiante.get('apMat'):
                info_text += f" {estudiante['apMat']}"
            
            ctk.CTkLabel(
                student_frame,
                text=info_text,
                font=ctk.CTkFont(size=12)
            ).pack(side="left", padx=10)
            
            # Botón de selección
            ctk.CTkButton(
                student_frame,
                text="Seleccionar",
                width=100,
                command=lambda e=estudiante: self.cargar_estudiante(e)
            ).pack(side="right", padx=5)
    
    def cargar_estudiante(self, estudiante):
        """Carga los datos del estudiante en el formulario"""
        self.current_student = estudiante
        self.mostrar_formulario(True)
        
        # Limpiar formulario primero
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        
        # Crear formulario de edición con apellidos separados
        self.crear_formulario_edicion()
        
        # Cargar datos
        self.cargar_datos_formulario(estudiante)
    
    def crear_formulario_edicion(self):
        """Crea los campos del formulario de edición con apellidos separados"""
        # Configurar grid
        self.form_frame.grid_columnconfigure(1, weight=1)
        row = 0
        
        # Código (no editable)
        ctk.CTkLabel(self.form_frame, text="Código:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.codigo_label = ctk.CTkLabel(self.form_frame, text="", font=ctk.CTkFont(size=12))
        self.codigo_label.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        row += 1
        
        # Nombre
        ctk.CTkLabel(self.form_frame, text="Nombre(s):").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.nombre_entry = ctk.CTkEntry(self.form_frame)
        self.nombre_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Apellido Paterno
        ctk.CTkLabel(self.form_frame, text="Apellido Paterno:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.apPat_entry = ctk.CTkEntry(self.form_frame)
        self.apPat_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Apellido Materno
        ctk.CTkLabel(self.form_frame, text="Apellido Materno:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.apMat_entry = ctk.CTkEntry(self.form_frame)
        self.apMat_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Correo
        ctk.CTkLabel(self.form_frame, text="Correo:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.correo_entry = ctk.CTkEntry(self.form_frame)
        self.correo_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Teléfono
        ctk.CTkLabel(self.form_frame, text="Teléfono:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.telefono_entry = ctk.CTkEntry(self.form_frame)
        self.telefono_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Carrera
        ctk.CTkLabel(self.form_frame, text="Carrera:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.carrera_entry = ctk.CTkEntry(self.form_frame)
        self.carrera_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Semestre
        ctk.CTkLabel(self.form_frame, text="Semestre:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.semestre_entry = ctk.CTkEntry(self.form_frame)
        self.semestre_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Estado
        ctk.CTkLabel(self.form_frame, text="Estado:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.estado_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=["Inscrito", "No inscrito", "Graduado", "Baja temporal"]
        )
        self.estado_combobox.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
    
    def cargar_datos_formulario(self, estudiante):
        """Carga los datos del estudiante en los campos del formulario"""
        self.codigo_label.configure(text=estudiante['codigo_estudiante'])
        self.nombre_entry.insert(0, estudiante['nombre'])
        self.apPat_entry.insert(0, estudiante.get('apPat', ''))
        self.apMat_entry.insert(0, estudiante.get('apMat', ''))
        self.correo_entry.insert(0, estudiante['correo'])
        self.telefono_entry.insert(0, estudiante.get('telefono', ''))
        self.carrera_entry.insert(0, estudiante.get('carrera', ''))
        self.semestre_entry.insert(0, str(estudiante.get('semestre', '')))
        self.estado_combobox.set(estudiante.get('estado_inscripcion', 'Inscrito'))
    
    def guardar_cambios(self):
        """Guarda los cambios del estudiante"""
        if not self.current_student:
            messagebox.showwarning("Error", "No hay ningún estudiante seleccionado")
            return
        
        # Validar campos obligatorios
        if not all([
            self.nombre_entry.get().strip(),
            self.apPat_entry.get().strip(),
            self.correo_entry.get().strip()
        ]):
            messagebox.showwarning("Error", "Nombre, apellido paterno y correo son campos obligatorios")
            return
        
        # Preparar datos actualizados
        datos_actualizados = {
            'id_estudiante': self.current_student['id_estudiante'],
            'nombre': self.nombre_entry.get().strip(),
            'apPat': self.apPat_entry.get().strip(),
            'apMat': self.apMat_entry.get().strip() or None,
            'correo': self.correo_entry.get().strip(),
            'telefono': self.telefono_entry.get().strip() or None,
            'carrera': self.carrera_entry.get().strip() or None,
            'semestre': int(self.semestre_entry.get()) if self.semestre_entry.get().strip() else None,
            'estado_inscripcion': self.estado_combobox.get()
        }
        
        # Aquí iría el código para actualizar en la base de datos
        try:
            # Ejemplo de consulta SQL:
            # query = """UPDATE estudiantes SET 
            #            nombre = %s, apPat = %s, apMat = %s, correo = %s,
            #            telefono = %s, carrera = %s, semestre = %s,
            #            estado_inscripcion = %s
            #            WHERE id_estudiante = %s"""
            # params = (datos_actualizados['nombre'], datos_actualizados['apPat'], ...)
            # self.db_cursor.execute(query, params)
            # self.db_connection.commit()
            
            messagebox.showinfo("Éxito", "Los cambios se guardaron correctamente")
            self.cerrar()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los cambios: {str(e)}")
    
    def mostrar_formulario(self, mostrar):
        """Muestra u oculta el formulario"""
        if mostrar:
            self.form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        else:
            self.form_frame.pack_forget()
    
    def obtener_estudiantes_db(self, termino):
        """Obtiene estudiantes de la base de datos (simulado)"""
        # Ejemplo con datos dummy - reemplazar con consulta real a MySQL
        estudiantes = [
            {
                'id_estudiante': 1,
                'codigo_estudiante': 'EST-2023-001',
                'nombre': 'Juan',
                'apPat': 'Pérez',
                'apMat': 'Gómez',
                'correo': 'juan@example.com',
                'telefono': '5551234567',
                'fecha_nacimiento': '2000-01-15',
                'carrera': 'Ingeniería en Sistemas',
                'semestre': 5,
                'estado_inscripcion': 'Inscrito'
            },
            {
                'id_estudiante': 2,
                'codigo_estudiante': 'EST-2023-002',
                'nombre': 'María',
                'apPat': 'García',
                'apMat': 'López',
                'correo': 'maria@example.com',
                'telefono': '5559876543',
                'fecha_nacimiento': '1999-05-20',
                'carrera': 'Medicina',
                'semestre': 8,
                'estado_inscripcion': 'Inscrito'
            }
        ]
        
        termino = termino.lower()
        return [
            e for e in estudiantes 
            if (termino in e['codigo_estudiante'].lower() or 
                termino in e['nombre'].lower() or
                termino in e['apPat'].lower() or
                (e.get('apMat') and termino in e['apMat'].lower()))
        ]
    
    def cerrar(self):
        """Cierra esta pantalla"""
        self.frame.pack_forget()