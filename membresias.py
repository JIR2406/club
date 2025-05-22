import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class MembershipManagementWindow:
    def __init__(self, root, app_manager):
        self.root = root
        self.app = app_manager
        self.current_membership = None
        self.user = None
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Construir interfaz
        self._create_ui()
        
        # Cargar datos iniciales
        self.update_memberships_list()

    def _create_ui(self):
        """Construye la interfaz gráfica"""
        # Configuración del grid principal
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Frame de búsqueda con botón de regreso
        search_frame = ctk.CTkFrame(self.main_frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Botón para regresar al menú
        ctk.CTkButton(
            search_frame,
            text="← Menú",
            width=80,
            command=self.return_to_menu,
            fg_color="#6c757d",
            hover_color="#5a6268"
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(search_frame, text="Buscar Membresía:").pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Estudiante, club o estado..."
        )
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_memberships())
        
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search_memberships,
            width=100
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            search_frame,
            text="Limpiar",
            command=self.clear_search,
            width=100
        ).pack(side="left")
        
        # Lista de membresías
        self._create_memberships_list()
        
        # Formulario de edición
        self._create_form()
        
        # Barra de estado
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Listo",
            anchor="w"
        )
        self.status_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
    
    def _create_memberships_list(self):
        """Crea el panel de lista de membresías"""
        self.list_frame = ctk.CTkFrame(self.main_frame, width=400)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.list_frame.grid_propagate(False)
        
        # Cabecera
        header_frame = ctk.CTkFrame(self.list_frame)
        header_frame.pack(fill="x")
        
        self.membership_count_label = ctk.CTkLabel(
            header_frame,
            text="Membresías (0)",
            font=ctk.CTkFont(weight="bold")
        )
        self.membership_count_label.pack(side="left", padx=5)
        
        ctk.CTkButton(
            header_frame,
            text="+ Nueva",
            width=80,
            command=self.new_membership
        ).pack(side="right")
        
        # Lista con scroll
        self.list_scroll = ctk.CTkScrollableFrame(
            self.list_frame,
            height=550
        )
        self.list_scroll.pack(fill="both", expand=True)
    
    def _create_form(self):
        """Crea el formulario de edición"""
        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.form_frame.grid(row=1, column=1, sticky="nsew")
        
        # Título del formulario
        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text="Nueva Membresía",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.form_title.pack(pady=(0, 20))
        
        # Campos del formulario
        fields = [
            {"label": "Estudiante*", "var_name": "estudiante_var", "required": True},
            {"label": "Club*", "var_name": "club_var", "required": True},
            {"label": "Fecha Inscripción*", "var_name": "fecha_insc_var", "required": True},
            {"label": "Fecha Expiración", "var_name": "fecha_exp_var"},
            {"label": "Estado*", "var_name": "estado_var", "required": True},
            {"label": "Rol*", "var_name": "rol_var", "required": True}
        ]
        
        self.form_vars = {}
        
        for field in fields:
            frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            
            label_text = field["label"].replace("*", "") + (" *" if field.get("required") else "")
            ctk.CTkLabel(frame, text=label_text, width=120).pack(side="left")
            
            var = ctk.StringVar()
            
            if field["var_name"] == "estado_var":
                ctk.CTkComboBox(
                    frame,
                    variable=var,
                    values=["Activa", "Inactiva", "Suspendida", "En proceso"],
                    state="readonly"
                ).pack(side="right", fill="x", expand=True)
            elif field["var_name"] == "rol_var":
                ctk.CTkComboBox(
                    frame,
                    variable=var,
                    values=["Miembro", "Coordinador", "Secretario", "Tesorero", "Asesor"],
                    state="readonly"
                ).pack(side="right", fill="x", expand=True)
            elif field["var_name"] in ["fecha_insc_var", "fecha_exp_var"]:
                ctk.CTkEntry(
                    frame,
                    textvariable=var,
                    placeholder_text="YYYY-MM-DD"
                ).pack(side="right", fill="x", expand=True)
            else:
                ctk.CTkEntry(
                    frame,
                    textvariable=var
                ).pack(side="right", fill="x", expand=True)
            
            self.form_vars[field["var_name"]] = var
        
        # Botones de acción
        button_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(
            button_frame,
            text="Guardar",
            command=self.save_membership,
            fg_color="#28a745"
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=self.cancel_edit
        ).pack(side="left", padx=(0, 10))
        
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="Eliminar",
            command=self.delete_membership,
            fg_color="#dc3545",
            state="disabled"
        )
        self.delete_btn.pack(side="right")
    
    def return_to_menu(self):
        """Regresa al menú principal"""
        self.app.show_menu(self.app.current_user)
    
    def update_memberships_list(self):
        """Actualiza la lista de membresías"""
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        memberships = self.get_memberships_from_db()
        self.membership_count_label.configure(text=f"Membresías ({len(memberships)})")
        
        if not memberships:
            ctk.CTkLabel(
                self.list_scroll,
                text="No se encontraron membresías",
                text_color="gray"
            ).pack(pady=20)
            return
        
        for membership in memberships:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            # Formatear información para mostrar
            text = (f"{membership['nombre_estudiante']} en {membership['nombre_club']} - "
                   f"{membership['estado_membresia']} ({membership['rol']})")
            
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda m=membership: self.load_membership_data(m)
            ).pack(side="right", padx=2)