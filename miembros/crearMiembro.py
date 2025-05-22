import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import re

class RegistroEstudianteForm:
    def __init__(self, root, on_submit=None):
        """
        Formulario para registrar un nuevo estudiante/miembro
        
        Args:
            root: Ventana padre o frame contenedor
            on_submit: Función callback que se ejecutará al enviar el formulario
        """
        self.root = root
        self.on_submit = on_submit
        
        # Configurar el grid principal
        self.root.grid_columnconfigure(1, weight=1)
        
        # Título del formulario
        self.title_label = ctk.CTkLabel(
            self.root, 
            text="Registro de Nuevo Estudiante",
            font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        
        # Campos del formulario
        self.create_widgets()
        
    def create_widgets(self):
        """Crea todos los widgets del formulario"""
        row = 1
        
        # Código de Estudiante
        self.codigo_label = ctk.CTkLabel(self.root, text="Código de Estudiante:")
        self.codigo_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.codigo_entry = ctk.CTkEntry(self.root, placeholder_text="Ej: EST-2023-001")
        self.codigo_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Nombre
        self.nombre_label = ctk.CTkLabel(self.root, text="Nombre(s):")
        self.nombre_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.nombre_entry = ctk.CTkEntry(self.root)
        self.nombre_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Apellido
        self.apellido_label = ctk.CTkLabel(self.root, text="Apellido(s):")
        self.apellido_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.apellido_entry = ctk.CTkEntry(self.root)
        self.apellido_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Correo Electrónico
        self.correo_label = ctk.CTkLabel(self.root, text="Correo Electrónico:")
        self.correo_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.correo_entry = ctk.CTkEntry(self.root, placeholder_text="ejemplo@dominio.com")
        self.correo_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Teléfono
        self.telefono_label = ctk.CTkLabel(self.root, text="Teléfono:")
        self.telefono_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.telefono_entry = ctk.CTkEntry(self.root, placeholder_text="+52 1234567890")
        self.telefono_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Fecha de Nacimiento
        self.fecha_nac_label = ctk.CTkLabel(self.root, text="Fecha de Nacimiento:")
        self.fecha_nac_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.fecha_nac_entry = ctk.CTkEntry(self.root, placeholder_text="AAAA-MM-DD")
        self.fecha_nac_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Carrera
        self.carrera_label = ctk.CTkLabel(self.root, text="Carrera:")
        self.carrera_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.carrera_entry = ctk.CTkEntry(self.root, placeholder_text="Ej: Ingeniería en Sistemas")
        self.carrera_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Semestre
        self.semestre_label = ctk.CTkLabel(self.root, text="Semestre:")
        self.semestre_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.semestre_entry = ctk.CTkEntry(self.root, placeholder_text="1 al 12")
        self.semestre_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Estado de Inscripción
        self.estado_label = ctk.CTkLabel(self.root, text="Estado de Inscripción:")
        self.estado_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.estado_var = ctk.StringVar(value="Inscrito")
        self.estado_combobox = ctk.CTkComboBox(
            self.root, 
            values=["Inscrito", "No inscrito", "Graduado", "Baja temporal"],
            variable=self.estado_var
        )
        self.estado_combobox.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Botones de acción
        self.button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.button_frame.grid(row=row, column=0, columnspan=2, pady=20, sticky="e")
        
        self.cancel_button = ctk.CTkButton(
            self.button_frame, 
            text="Cancelar", 
            fg_color="gray", 
            command=self.close_form
        )
        self.cancel_button.pack(side="right", padx=5)
        
        self.submit_button = ctk.CTkButton(
            self.button_frame, 
            text="Registrar Estudiante", 
            command=self.submit_form
        )
        self.submit_button.pack(side="right", padx=5)
    
    def validate_form(self):
        """Valida los datos del formulario"""
        errors = []
        
        # Validar campos obligatorios
        if not self.codigo_entry.get().strip():
            errors.append("El código de estudiante es obligatorio")
        if not self.nombre_entry.get().strip():
            errors.append("El nombre es obligatorio")
        if not self.apellido_entry.get().strip():
            errors.append("El apellido es obligatorio")
        if not self.correo_entry.get().strip():
            errors.append("El correo electrónico es obligatorio")
        
        # Validar formato de correo
        correo = self.correo_entry.get().strip()
        if correo and not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            errors.append("El correo electrónico no tiene un formato válido")
        
        # Validar fecha de nacimiento
        fecha_nac = self.fecha_nac_entry.get().strip()
        if fecha_nac:
            try:
                datetime.strptime(fecha_nac, "%Y-%m-%d")
            except ValueError:
                errors.append("La fecha de nacimiento debe estar en formato AAAA-MM-DD")
        
        # Validar semestre
        semestre = self.semestre_entry.get().strip()
        if semestre:
            try:
                semestre_num = int(semestre)
                if semestre_num < 1 or semestre_num > 12:
                    errors.append("El semestre debe estar entre 1 y 12")
            except ValueError:
                errors.append("El semestre debe ser un número entero")
        
        return errors
    
    def get_form_data(self):
        """Obtiene los datos del formulario en un diccionario"""
        return {
            "codigo_estudiante": self.codigo_entry.get().strip(),
            "nombre": self.nombre_entry.get().strip(),
            "apellido": self.apellido_entry.get().strip(),
            "correo": self.correo_entry.get().strip(),
            "telefono": self.telefono_entry.get().strip() or None,
            "fecha_nacimiento": self.fecha_nac_entry.get().strip() or None,
            "carrera": self.carrera_entry.get().strip() or None,
            "semestre": int(self.semestre_entry.get()) if self.semestre_entry.get().strip() else None,
            "estado_inscripcion": self.estado_var.get()
        }
    
    def submit_form(self):
        """Envía el formulario después de validar los datos"""
        errors = self.validate_form()
        
        if errors:
            messagebox.showerror("Errores en el formulario", "\n".join(errors))
            return
        
        form_data = self.get_form_data()
        
        if self.on_submit:
            self.on_submit(form_data)
    
    def close_form(self):
        """Cierra el formulario"""
        if hasattr(self.root, "destroy"):
            self.root.destroy()
        else:
            self.root.grid_forget()


# Ejemplo de uso
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Registro de Estudiante")
    root.geometry("800x700")
    
    def handle_submit(data):
        print("Datos del estudiante recibidos:")
        print(data)
        messagebox.showinfo("Éxito", "Estudiante registrado correctamente")
        root.destroy()
    
    # Crear un frame principal
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Mostrar el formulario
    form = RegistroEstudianteForm(main_frame, on_submit=handle_submit)
    
    root.mainloop()