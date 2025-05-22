import customtkinter as ctk
from tkinter import messagebox

class ConsultarEstudiantesScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.create_widgets()
        
    def create_widgets(self):
        """Crea todos los componentes de la interfaz"""
        # Título
        ctk.CTkLabel(
            self.frame,
            text="Consulta de Estudiantes",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        # Panel de filtros
        filter_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        # Campo de búsqueda
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            filter_frame,
            textvariable=self.search_var,
            placeholder_text="Buscar por código, nombre o apellido...",
            width=300
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        # Botones de filtro
        ctk.CTkButton(
            filter_frame,
            text="Buscar",
            width=100,
            command=self.filtrar_estudiantes
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            filter_frame,
            text="Mostrar Todos",
            width=100,
            command=self.mostrar_todos
        ).pack(side="left", padx=5)
        
        # Lista de estudiantes
        self.list_container = ctk.CTkScrollableFrame(self.frame, height=400)
        self.list_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botón de volver
        ctk.CTkButton(
            self.frame,
            text="Volver",
            command=self.cerrar
        ).pack(pady=20)
        
        # Cargar todos los estudiantes inicialmente
        self.mostrar_todos()
    
    def mostrar_todos(self):
        """Muestra todos los estudiantes sin filtros"""
        self.search_var.set("")
        self.filtrar_estudiantes()
    
    def filtrar_estudiantes(self):
        """Filtra los estudiantes según el texto ingresado"""
        termino = self.search_var.get().strip().lower()
        
        # Limpiar lista actual
        for widget in self.list_container.winfo_children():
            widget.destroy()
        
        # Obtener estudiantes de la base de datos
        estudiantes = self.obtener_estudiantes_db(termino)
        
        if not estudiantes:
            ctk.CTkLabel(
                self.list_container,
                text="No se encontraron estudiantes",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return
        
        # Crear encabezados de la tabla
        header_frame = ctk.CTkFrame(self.list_container)
        header_frame.pack(fill="x", pady=(0, 5))
        
        headers = ["Código", "Nombre", "Ap. Paterno", "Ap. Materno", "Carrera", "Estado", "Acciones"]
        for i, header in enumerate(headers):
            width = 100 if i < len(headers)-1 else 80
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=width
            ).grid(row=0, column=i, padx=2, sticky="w")
        
        # Mostrar cada estudiante
        for estudiante in estudiantes:
            self.crear_item_estudiante(estudiante)
    
    def crear_item_estudiante(self, estudiante):
        """Crea un item de estudiante en la lista"""
        item_frame = ctk.CTkFrame(self.list_container)
        item_frame.pack(fill="x", pady=2)
        
        # Configurar grid para el item
        item_frame.grid_columnconfigure(0, minsize=100)  # Código
        item_frame.grid_columnconfigure(1, minsize=100)  # Nombre
        item_frame.grid_columnconfigure(2, minsize=100)  # Ap. Paterno
        item_frame.grid_columnconfigure(3, minsize=100)  # Ap. Materno
        item_frame.grid_columnconfigure(4, minsize=100)  # Carrera
        item_frame.grid_columnconfigure(5, minsize=100)  # Estado
        
        # Código
        ctk.CTkLabel(
            item_frame,
            text=estudiante['codigo_estudiante'],
            width=100
        ).grid(row=0, column=0, padx=2, sticky="w")
        
        # Nombre
        ctk.CTkLabel(
            item_frame,
            text=estudiante['nombre'],
            width=100
        ).grid(row=0, column=1, padx=2, sticky="w")
        
        # Apellido Paterno
        ctk.CTkLabel(
            item_frame,
            text=estudiante.get('apPat', ''),
            width=100
        ).grid(row=0, column=2, padx=2, sticky="w")
        
        # Apellido Materno
        ctk.CTkLabel(
            item_frame,
            text=estudiante.get('apMat', ''),
            width=100
        ).grid(row=0, column=3, padx=2, sticky="w")
        
        # Carrera
        ctk.CTkLabel(
            item_frame,
            text=estudiante.get('carrera', 'N/A'),
            width=100
        ).grid(row=0, column=4, padx=2, sticky="w")
        
        # Estado
        ctk.CTkLabel(
            item_frame,
            text=estudiante.get('estado_inscripcion', 'N/A'),
            width=100
        ).grid(row=0, column=5, padx=2, sticky="w")
        
        # Botón de seleccionar
        ctk.CTkButton(
            item_frame,
            text="Ver",
            width=80,
            command=lambda e=estudiante: self.mostrar_detalles(e)
        ).grid(row=0, column=6, padx=2)
    
    def mostrar_detalles(self, estudiante):
        """Muestra los detalles completos del estudiante"""
        # Limpiar la lista
        for widget in self.list_container.winfo_children():
            widget.destroy()
        
        # Botón para volver a la lista
        ctk.CTkButton(
            self.list_container,
            text="Volver a la lista",
            command=self.filtrar_estudiantes
        ).pack(pady=(0, 20), anchor="w")
        
        # Marco para los detalles
        details_frame = ctk.CTkFrame(self.list_container)
        details_frame.pack(fill="x", pady=10, padx=10)
        
        # Mostrar todos los campos del estudiante
        campos = [
            ("Código de Estudiante", estudiante['codigo_estudiante']),
            ("Nombre", estudiante['nombre']),
            ("Apellido Paterno", estudiante.get('apPat', 'N/A')),
            ("Apellido Materno", estudiante.get('apMat', 'N/A')),
            ("Correo Electrónico", estudiante['correo']),
            ("Teléfono", estudiante.get('telefono', 'N/A')),
            ("Fecha de Nacimiento", estudiante.get('fecha_nacimiento', 'N/A')),
            ("Carrera", estudiante.get('carrera', 'N/A')),
            ("Semestre", str(estudiante.get('semestre', 'N/A'))),
            ("Estado de Inscripción", estudiante.get('estado_inscripcion', 'N/A'))
        ]
        
        for i, (campo, valor) in enumerate(campos):
            row_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                row_frame,
                text=f"{campo}:",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=180,
                anchor="e"
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                row_frame,
                text=valor,
                font=ctk.CTkFont(size=12),
                wraplength=400,
                justify="left"
            ).pack(side="left", padx=5)
    
    def obtener_estudiantes_db(self, filtro=None):
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
        
        if filtro:
            return [
                e for e in estudiantes 
                if (filtro in e['codigo_estudiante'].lower() or 
                    filtro in e['nombre'].lower() or
                    filtro in e['apPat'].lower() or
                    filtro in e['apMat'].lower())
            ]
        return estudiantes
    
    def cerrar(self):
        """Cierra esta pantalla"""
        self.frame.pack_forget()