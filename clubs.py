import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from conn import get_connection
import re


class ClubManagementWindow:
    def __init__(self, root, app_manager):
        self.root = root
        self.app = app_manager
        self.current_club = None
        self.clubs_data = []
        
        self._create_ui()
        self.update_clubs_list()
        self.search_entry.focus()
        
    def _create_ui(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configuración del grid
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Frame de búsqueda
        search_frame = ctk.CTkFrame(self.main_frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ctk.CTkButton(
            search_frame, text="← Menú", width=80,
            command=self.return_to_menu, fg_color="#6c757d"
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(search_frame, text="Buscar Club:").pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame, width=300,
            placeholder_text="Nombre, código o responsable..."
        )
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_clubs())
        
        ctk.CTkButton(search_frame, text="Buscar", command=self.search_clubs, width=100
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(search_frame, text="Limpiar", command=self.clear_search, width=100
        ).pack(side="left")
        
        # Lista de clubs
        self._create_clubs_list()
        
        # Formulario de edición
        self._create_form()
        
        # Barra de estado
        self.status_label = ctk.CTkLabel(self.main_frame, text="Listo", anchor="w")
        self.status_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
    
    def _create_clubs_list(self):
        self.list_frame = ctk.CTkFrame(self.main_frame, width=350)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.list_frame.grid_propagate(False)
        
        header_frame = ctk.CTkFrame(self.list_frame)
        header_frame.pack(fill="x")
        
        self.club_count_label = ctk.CTkLabel(
            header_frame, text="Clubs (0)", font=ctk.CTkFont(weight="bold")
        )
        self.club_count_label.pack(side="left", padx=5)
        
        ctk.CTkButton(
            header_frame, text="+ Nuevo", width=80, command=self.new_club
        ).pack(side="right")
        
        self.list_scroll = ctk.CTkScrollableFrame(self.list_frame, height=550)
        self.list_scroll.pack(fill="both", expand=True)
    
    def _create_form(self):
        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.form_frame.grid(row=1, column=1, sticky="nsew")

        self.form_title = ctk.CTkLabel(
            self.form_frame, text="Nuevo Club", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.form_title.pack(pady=(0, 20))

        fields = [
            {"label": "Código Club*", "name": "code"},
            {"label": "Nombre Club*", "name": "name"},
            {"label": "Responsable", "name": "responsable"},
            {"label": "Correo Contacto", "name": "email"},
            {"label": "Estado*", "name": "status", "type": "combobox", "values": ["Activo", "Inactivo", "En pausa"]},
            {"label": "Fecha Creación", "name": "creation_date"},
            {"label": "Máx. Miembros", "name": "max_members"},
            {"label": "Requisitos", "name": "requirements", "type": "textbox"},
            {"label": "Descripción", "name": "description", "type": "textbox"},
        ]

        self.form_widgets = {}

        for field in fields:
            frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            frame.pack(fill="x", pady=5)

            label = ctk.CTkLabel(frame, text=field["label"], width=120)
            label.pack(side="left")

            if field.get("type") == "combobox":
                widget = ctk.CTkComboBox(frame, values=field["values"], state="readonly")
                widget.pack(side="right", fill="x", expand=True)
                if field["name"] == "status":
                    widget.set("Activo")
            elif field.get("type") == "textbox":
                widget = ctk.CTkTextbox(frame, height=60)
                widget.pack(side="right", fill="x", expand=True)
            else:
                widget = ctk.CTkEntry(frame)
                widget.pack(side="right", fill="x", expand=True)
                if field["name"] == "creation_date":
                    widget.insert(0, datetime.now().strftime("%Y-%m-%d"))

            self.form_widgets[field["name"]] = widget

        # Botones
        button_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))

        ctk.CTkButton(
            button_frame, text="Guardar", command=self.save_club, fg_color="#28a745"
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            button_frame, text="Cancelar", command=self.cancel_edit
        ).pack(side="left", padx=(0, 10))

        self.delete_btn = ctk.CTkButton(
            button_frame, text="Eliminar", command=self.delete_club,
            fg_color="#dc3545", state="disabled"
        )
        self.delete_btn.pack(side="right")
    
        

