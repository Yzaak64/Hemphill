# Hemphill_App.py (Lanzador con Popup Aislado)

# ===================================================================================
# Hemphill.py (LANZADOR PRINCIPAL - VERSIÓN DE PRODUCCIÓN)
# Este es el archivo que se debe ejecutar.
# Muestra el pop-up de apoyo y luego lanza la aplicación principal.
# ===================================================================================

import sys
import os
import traceback

# Añadir la carpeta actual al path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

try:
    # Importar las funciones y clases necesarias
    from popapp import show_coffee_popup
    from app_logic import HemphillApp
except ImportError as e:
    print(f"ERROR: No se pudo importar un módulo necesario: {e}")
    input("Presiona Enter para salir...")
    sys.exit(1)


if __name__ == "__main__":
    try:
        # --- NUEVA LÓGICA DE INICIO SIMPLIFICADA ---

        # 1. Mostrar el pop-up de apoyo PRIMERO.
        #    Esta función ahora maneja su propio bucle de Tkinter y bloquea la ejecución.
        print("Mostrando pop-up de apoyo...")
        show_coffee_popup()
        print("Pop-up cerrado. Iniciando aplicación principal...")

        # 2. SOLO DESPUÉS de que el popup se cierre, crear e iniciar la aplicación principal.
        app = HemphillApp()
        app.mainloop()
        
    except Exception as e:
        print(f"ERROR FATAL en la aplicación principal: {e}")
        traceback.print_exc()
        input("Presiona Enter para salir...")