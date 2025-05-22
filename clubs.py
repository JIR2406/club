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
    
    
        

