# popapp.py (Versión de Aislamiento Total)
import tkinter as tk
from tkinter import ttk
import webbrowser
import os
from PIL import Image, ImageTk
import traceback

def show_coffee_popup(): # <-- No recibe 'parent'
    """
    Muestra una ventana emergente en su propia instancia de Tkinter,
    bloqueando la ejecución hasta que se cierre.
    """
    print("[LOG] Iniciando show_coffee_popup (Aislamiento Total).")
    
    # 1. Crear una instancia de Tkinter temporal y ocultarla.
    temp_root = tk.Tk()
    temp_root.withdraw()

    popup = None
    try:
        # 2. El Toplevel pertenece a la raíz temporal.
        popup = tk.Toplevel(temp_root)
        popup.title("Apoya este Proyecto")
        
        def on_close_popup():
            print("[LOG] Popup cerrado. Destruyendo la instancia temporal de Tkinter.")
            temp_root.quit() # Rompe el mainloop
            temp_root.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close_popup)
        
        # --- El resto del código es igual ---
        popup_frame = ttk.Frame(popup, padding="20")
        popup_frame.pack(expand=True, fill=tk.BOTH)
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
        except Exception as e:
            traceback.print_exc()
            fallback_button = ttk.Button(popup_frame, text="☕ Invítame un café", command=lambda: [webbrowser.open_new(support_url), on_close_popup()])
            fallback_button.pack(pady=10)
        
        continue_button = ttk.Button(popup_frame, text="Continuar al programa", command=on_close_popup)
        continue_button.pack(pady=(20, 0))

        # --- Centrar y hacer visible ---
        popup.update_idletasks()
        p_width = popup.winfo_width()
        p_height = popup.winfo_height()
        s_width = popup.winfo_screenwidth()
        s_height = popup.winfo_screenheight()
        x = (s_width // 2) - (p_width // 2)
        y = (s_height // 2) - (p_height // 2)
        popup.geometry(f"{p_width}x{p_height}+{x}+{y}")
        popup.attributes('-topmost', True)
        popup.deiconify() # Asegurarse de que el Toplevel es visible
        popup.focus_force()
        popup.grab_set()

        # 3. Iniciar el bucle de eventos para la instancia temporal.
        print("[LOG] Iniciando bucle de eventos del popup.")
        temp_root.mainloop()
        print("[LOG] Bucle de eventos del popup finalizado.")

    except Exception as e:
        print(f"ERROR FATAL en show_coffee_popup: {e}")
        traceback.print_exc()
        if temp_root:
            temp_root.destroy()