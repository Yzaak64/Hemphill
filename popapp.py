# popapp.py (Versión Final con Scroll H/V)

import tkinter as tk
from tkinter import ttk
import webbrowser
import os
from PIL import Image, ImageTk
import traceback

def show_coffee_popup():
    """
    Muestra una ventana emergente con scrolls H/V en su propia instancia de Tkinter,
    bloqueando la ejecución hasta que se cierre.
    """
    temp_root = tk.Tk()
    temp_root.withdraw()

    popup = None
    try:
        popup = tk.Toplevel(temp_root)
        popup.title("Apoya este Proyecto")
        
        # --- INICIO DE MODIFICACIONES PARA SCROLL H/V ---
        
        # El canvas que permite el desplazamiento
        canvas = tk.Canvas(popup)
        
        # Crear ambas barras de desplazamiento
        v_scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(popup, orient="horizontal", command=canvas.xview)
        
        # El frame interno que contendrá todos los widgets
        popup_frame = ttk.Frame(canvas, padding="20")

        # Binding para actualizar la región de scroll cuando el contenido cambia
        popup_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=popup_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar los widgets en la ventana principal
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        
        # --- FIN DE MODIFICACIONES ---

        def on_close_popup():
            temp_root.quit()
            temp_root.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close_popup)
        
        # --- El resto del código que añade widgets a 'popup_frame' es igual ---
        ttk.Label(popup_frame, text="¡Hola!", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))
        support_text = "Si esta herramienta te resulta útil, considera apoyar su desarrollo futuro con un café."
        ttk.Label(popup_frame, text=support_text, wraplength=350, justify=tk.CENTER).pack(pady=(0, 20))
        
        support_url = "https://www.buymeacoffee.com/Yzaak64"
        image_path = "Buy_Coffe.png"
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img.thumbnail((300, 100))
                popup.coffee_photo = ImageTk.PhotoImage(img) 
                coffee_button = tk.Button(popup_frame, image=popup.coffee_photo, command=lambda: [webbrowser.open_new(support_url), on_close_popup()], borderwidth=0, cursor="hand2")
                coffee_button.pack(pady=10)
            else:
                fallback_button = ttk.Button(popup_frame, text="☕ Invítame un café", command=lambda: [webbrowser.open_new(support_url), on_close_popup()])
                fallback_button.pack(pady=10)
        except Exception:
            traceback.print_exc()
            fallback_button = ttk.Button(popup_frame, text="☕ Invítame un café", command=lambda: [webbrowser.open_new(support_url), on_close_popup()])
            fallback_button.pack(pady=10)
        
        continue_button = ttk.Button(popup_frame, text="Continuar al programa", command=on_close_popup)
        continue_button.pack(pady=(20, 0))

        # Centrar y hacer visible la ventana
        popup.update_idletasks()
        # Ajustamos un tamaño mínimo para que el pop-up no sea demasiado pequeño
        p_width = max(popup_frame.winfo_reqwidth() + 40, 400) # +40 for padding
        p_height = popup_frame.winfo_reqheight() + 40
        s_width = popup.winfo_screenwidth()
        s_height = popup.winfo_screenheight()
        x = (s_width // 2) - (p_width // 2)
        y = (s_height // 2) - (p_height // 2)
        popup.geometry(f"{p_width}x{p_height}+{x}+{y}")
        popup.minsize(350, 300) # Evita que se haga demasiado pequeño
        
        popup.attributes('-topmost', True)
        popup.deiconify()
        popup.focus_force()
        popup.grab_set()

        temp_root.mainloop()

    except Exception as e:
        print(f"ERROR FATAL en show_coffee_popup: {e}")
        traceback.print_exc()
        if temp_root:
            temp_root.destroy()