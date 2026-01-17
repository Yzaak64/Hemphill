# Hemphill_App.py (Lanzador Principal - Versión Corregida)

import sys
import os
import traceback

# Añadir la carpeta actual al path para asegurar que los módulos locales se encuentren.
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

try:
    from popapp import show_coffee_popup
    from app_logic import HemphillApp
except ImportError as e:
    print(f"ERROR: No se pudo importar un módulo necesario: {e}")
    input("Presiona Enter para salir...")
    sys.exit(1)


if __name__ == "__main__":
    try:
        # 1. Crear la aplicación principal (la raíz única de Tkinter)
        app = HemphillApp()
        # 2. Ocultarla temporalmente para que solo se vea el popup
        app.withdraw()

        # 3. Mostrar el popup. La ejecución del código se pausará aquí
        #    hasta que el popup sea cerrado por el usuario.
        #    Le pasamos 'app' como su ventana "madre".
        print("Mostrando pop-up de apoyo...")
        show_coffee_popup(app)
        print("Pop-up cerrado. Iniciando aplicación principal...")

        # 4. Una vez que el popup se cierra, mostramos la ventana principal
        app.deiconify()
        
        # 5. Iniciar el único y principal mainloop
        app.mainloop()
        
    except Exception as e:
        print(f"ERROR FATAL en la aplicación principal: {e}")
        traceback.print_exc()
        input("Presiona Enter para salir...")