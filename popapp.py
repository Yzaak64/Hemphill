# popapp.py (Versión Corregida con una Sola Raíz)

import tkinter as tk
from tkinter import ttk
import webbrowser
import sys
import os
from PIL import Image, ImageTk
import traceback

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def show_coffee_popup(parent):
    """
    Muestra una ventana emergente como un Toplevel de la ventana principal (parent).
    Esta función bloqueará la ejecución hasta que la ventana emergente se cierre.
    """
    try:
        # Ya no creamos un nuevo tk.Tk(). Usamos el 'parent' que nos pasan.
        popup = tk.Toplevel(parent)
        popup.title("Apoya este Proyecto")
        
        # --- El resto del diseño de la ventana es casi idéntico ---
        canvas = tk.Canvas(popup)
        v_scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        popup_frame = ttk.Frame(canvas, padding="20")
        
        popup_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=popup_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set)
        
        v_scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # La función de cierre ahora es más simple: solo destruye esta ventana.
        def on_close_popup():
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close_popup)
        
        ttk.Label(popup_frame, text="¡Hola!", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))
        
        support_text = "Si esta herramienta te resulta útil, considera apoyar su desarrollo futuro con un café."
        ttk.Label(popup_frame, text=support_text, wraplength=350, justify=tk.CENTER).pack(pady=(0, 20))
        
        support_url = "https://www.buymeacacoffee.com/Yzaak64"
        image_path = resource_path("Buy_Coffe.png")
        
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img.thumbnail((300, 100))
                popup.coffee_photo = ImageTk.PhotoImage(img) 
                
                coffee_button = tk.Button(popup_frame, image=popup.coffee_photo, 
                                          command=lambda: [webbrowser.open_new(support_url), on_close_popup()], 
                                          borderwidth=0, cursor="hand2")
                coffee_button.pack(pady=10)
            else:
                raise FileNotFoundError("Imagen no encontrada.")
        except Exception:
            traceback.print_exc()
            fallback_button = ttk.Button(popup_frame, text="☕ Invítame un café", 
                                         command=lambda: [webbrowser.open_new(support_url), on_close_popup()])
            fallback_button.pack(pady=10)
        
        continue_button = ttk.Button(popup_frame, text="Continuar al programa", command=on_close_popup)
        continue_button.pack(pady=(20, 0))

        # --- Lógica de centrado y modalidad ---
        popup.update_idletasks()
        p_width = max(popup_frame.winfo_reqwidth() + 40, 400); p_height = popup_frame.winfo_reqheight() + 40
        s_width = popup.winfo_screenwidth(); s_height = popup.winfo_screenheight()
        x = (s_width // 2) - (p_width // 2); y = (s_height // 2) - (p_height // 2)
        popup.geometry(f"{p_width}x{p_height}+{x}+{y}"); popup.minsize(350, 300)
        
        # Hacemos la ventana modal: bloquea la ventana principal hasta que esta se cierre
        popup.transient(parent)
        popup.grab_set()
        
        # Ya no se necesita un mainloop aquí. En su lugar, esperamos a que esta ventana se cierre.
        parent.wait_window(popup)

    except Exception as e:
        print(f"ERROR FATAL en show_coffee_popup: {e}")
        traceback.print_exc()