import customtkinter as ctk
from tkinter import messagebox
from db import get_connection

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

