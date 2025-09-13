# app_logic.py (Versión Final Corregida con Scroll H/V y manejo de errores NaN)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import os
import webbrowser

# Importar datos y lógica
try:
    from config import preguntas_espanol, nombres_dimensiones
    from logic import calculate_scores_from_answers, calculate_stanine
    from manual_generator import create_manual_pdf
    from PIL import Image, ImageTk
except ImportError as e:
    messagebox.showerror("Error de Módulo Interno", f"Falta un archivo esencial para Hemphill:\n{e}")
    import sys
    sys.exit(1)

# --- CLASE REUTILIZABLE PARA UN FRAME CON SCROLL HORIZONTAL Y VERTICAL ---
class ScrollableFrame(ttk.Frame):
    """Un marco con barras de desplazamiento vertical y horizontal."""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        canvas = tk.Canvas(self)
        
        # Crear ambas barras de desplazamiento
        v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar: el orden es importante
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

class HemphillApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador de Cuestionario Hemphill")
        self.geometry("950x700")

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        # Variables de estado
        self.all_individual_results = {}
        self.all_answers = []
        self.current_question_index = 0
        self.current_participant_name = ""
        self.average_results = pd.DataFrame()
        self.consolidated_results = pd.DataFrame()

        self.main_container = ScrollableFrame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.main_frame = self.main_container.scrollable_frame
        
        self.show_start_screen()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        self.clear_main_frame()
        ttk.Label(self.main_frame, text="Analizador de Cuestionario Hemphill", font=("Helvetica", 16, "bold")).pack(pady=20)
        ttk.Button(self.main_frame, text="📖 Ver Manual de Instrucciones", command=self.open_manual).pack(fill=tk.X, pady=(0, 15))
        ttk.Button(self.main_frame, text="📝 Responder Cuestionario Manualmente", command=self.prompt_for_participant_name).pack(fill=tk.X, pady=5)
        ttk.Button(self.main_frame, text="📂 Procesar Respuestas del Cuestionario", command=lambda: self.process_files('questions')).pack(fill=tk.X, pady=5)
        ttk.Button(self.main_frame, text="📊 Procesar Puntuaciones Crudas", command=lambda: self.process_files('scores')).pack(fill=tk.X, pady=5)
        
        template_frame = ttk.Frame(self.main_frame)
        template_frame.pack(pady=(20,5))
        ttk.Label(template_frame, text="Descargar plantillas para llenado manual:").pack()
        ttk.Button(template_frame, text="💾 Plantilla de Respuestas", command=lambda: self.download_template('questions')).pack(side=tk.LEFT, padx=10)
        ttk.Button(template_frame, text="💾 Plantilla de Puntuaciones", command=lambda: self.download_template('scores')).pack(side=tk.LEFT, padx=10)

    def open_manual(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            pdf_path = os.path.join(base_dir, "manual_hemphill.pdf")
            
            if not os.path.exists(pdf_path):
                if messagebox.askyesno("Manual no encontrado", "El manual no existe. ¿Deseas generarlo ahora?"):
                    success, error_msg = create_manual_pdf(pdf_path)
                    if not success:
                        messagebox.showerror("Error al Generar Manual", f"No se pudo crear el manual PDF.\n\nDetalles:\n{error_msg}")
                        return
                else:
                    return
            
            webbrowser.open_new(f"file://{pdf_path}")
        except Exception as e:
            messagebox.showerror("Error al Abrir Manual", f"No se pudo abrir el manual.\n\nError: {e}")

    # REEMPLAZA ESTA FUNCIÓN COMPLETA

    def process_files(self, mode):
        filepaths = filedialog.askopenfilenames(title=f"Selecciona los archivos CSV", filetypes=[("CSV Files", "*.csv")])
        if not filepaths: return
        
        self.all_individual_results = {}
        processed_count = 0
        skipped_participants = []

        for path in filepaths:
            try:
                try: df_raw = pd.read_csv(path, encoding='utf-8')
                except UnicodeDecodeError: df_raw = pd.read_csv(path, encoding='latin1')
                
                if mode == 'questions':
                    # Lógica para procesar respuestas (sin cambios)
                    name_col = next((col for col in df_raw.columns if "Nombre" in col), None)
                    if not name_col:
                        messagebox.showwarning("Formato Incorrecto", f"El archivo {os.path.basename(path)} no contiene una columna de 'Nombre'."); continue
                    start_index = df_raw.columns.get_loc(name_col) + 1
                    for index, row in df_raw.iterrows():
                        base_name = row[name_col] if pd.notna(row[name_col]) and str(row[name_col]).strip() else "Sujeto"
                        nombre = f"{base_name}_{index+1}"
                        try:
                            respuestas_raw = row[start_index : start_index + 150]
                            if len(respuestas_raw) < 150: raise ValueError("Fila no contiene 150 respuestas.")
                            respuestas = [int(float(r)) for r in respuestas_raw]
                            self.all_individual_results[nombre] = calculate_scores_from_answers(respuestas)
                            processed_count += 1
                        except (ValueError, TypeError):
                            skipped_participants.append(nombre); continue

                elif mode == 'scores':
                    possible_name_cols = ['Nombre o Identificador del Sujeto/Grupo:', 'Sujeto', 'Nombre del Participante o Grupo:']
                    name_col = next((col for col in df_raw.columns if col in possible_name_cols), None)
                    if name_col is None:
                        messagebox.showwarning("Formato Incorrecto", f"El archivo {os.path.basename(path)} no contiene una columna de identificación válida (ej. 'Sujeto')."); continue
                    
                    for index, row in df_raw.iterrows():
                        base_name = row[name_col] if pd.notna(row[name_col]) and str(row[name_col]).strip() else "Sujeto"
                        nombre = f"{base_name}_{index+1}"
                        try:
                            # --- CAMBIO AQUÍ: Buscamos los nombres de dimensión simplificados ---
                            # En lugar de "Puntuación Cruda para: Autonomía", ahora solo busca "Autonomía".
                            puntuaciones_brutas = {key: row[val] for key, val in nombres_dimensiones.items()}
                            self.all_individual_results[nombre] = calculate_stanine(puntuaciones_brutas)
                            processed_count += 1
                        except (ValueError, TypeError, KeyError):
                            skipped_participants.append(f"{nombre} (columnas de puntuación no encontradas o inválidas)")
                            continue

            except Exception as e:
                messagebox.showerror("Error de Archivo", f"No se pudo procesar {os.path.basename(path)}.\nError: {e}"); continue
        
        if self.all_individual_results:
            messagebox.showinfo("Proceso Completo", f"Se han procesado {processed_count} participantes/grupos.")
            self.calculate_group_averages()
            self.show_results_screen()
        else:
            messagebox.showwarning("Sin Datos", "No se pudieron procesar datos válidos de los archivos seleccionados.")

        if skipped_participants:
            skipped_list = "\n".join(skipped_participants)
            messagebox.showwarning("Participantes Omitidos", f"Los siguientes participantes/filas fueron omitidos por tener datos faltantes o inválidos:\n\n{skipped_list}")
        
    def prompt_for_participant_name(self):
        self.clear_main_frame()
        ttk.Label(self.main_frame, text="Responder Cuestionario", font=("Helvetica", 14, "bold")).pack(pady=20)
        ttk.Label(self.main_frame, text="Por favor, introduce un nombre o identificador para este análisis.").pack(pady=5)
        entry_frame = ttk.Frame(self.main_frame); entry_frame.pack(pady=20)
        ttk.Label(entry_frame, text="Nombre:").pack(side=tk.LEFT, padx=5)
        self.name_var_manual = tk.StringVar()
        name_entry = ttk.Entry(entry_frame, textvariable=self.name_var_manual, width=40)
        name_entry.pack(side=tk.LEFT, padx=5)
        name_entry.focus_set()
        name_entry.bind("<Return>", lambda event: self._start_quiz_with_name())
        button_frame = ttk.Frame(self.main_frame); button_frame.pack(pady=10)
        ttk.Button(button_frame, text="⬅️ Volver al Inicio", command=self.show_start_screen).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Comenzar Cuestionario ➡️", command=self._start_quiz_with_name).pack(side=tk.LEFT, padx=10)

    def _start_quiz_with_name(self):
        name = self.name_var_manual.get().strip()
        if not name:
            if not messagebox.askyesno("Nombre Vacío", "No has ingresado un nombre. ¿Deseas continuar como 'Sujeto Anónimo'?"): return
            self.current_participant_name = "Sujeto Anónimo"
        else: self.current_participant_name = name
        self.all_answers = [0] * 150
        self.current_question_index = 0
        self.show_quiz_screen()

    def show_quiz_screen(self):
        self.clear_main_frame()
        vcmd = (self.register(self.validate_input), '%P')
        instructions_text = "Califica cada afirmación. Usa los botones o presiona Enter para avanzar.\n1: TOTALMENTE DE ACUERDO, 2: DE ACUERDO, 3: INDECISO, 4: EN DESACUERDO, 5: TOTALMENTE EN DESACUERDO"
        ttk.Label(self.main_frame, text=instructions_text, wraplength=780, justify=tk.CENTER).pack(pady=10)
        self.question_label = ttk.Label(self.main_frame, text="", font=("Helvetica", 12), wraplength=780, justify=tk.CENTER); self.question_label.pack(pady=20)
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(self.main_frame, textvariable=self.answer_var, justify=tk.CENTER, validate="key", validatecommand=vcmd); self.answer_entry.pack(pady=10)
        self.answer_entry.bind("<Return>", lambda event: self.navigate("next"))
        nav_frame = ttk.Frame(self.main_frame); nav_frame.pack(pady=10)
        self.prev_button = ttk.Button(nav_frame, text="⬅️ Anterior", command=lambda: self.navigate("prev")); self.prev_button.pack(side=tk.LEFT, padx=5)
        self.next_button = ttk.Button(nav_frame, text="Siguiente ➡️", command=lambda: self.navigate("next")); self.next_button.pack(side=tk.LEFT, padx=5)
        action_frame = ttk.Frame(self.main_frame); action_frame.pack(pady=20)
        ttk.Button(action_frame, text="❌ Salir y Volver al Inicio", command=self.show_start_screen).pack(side=tk.LEFT, padx=10)
        ttk.Button(action_frame, text="🏁 Finalizar Cuestionario", command=self.finish_quiz).pack(side=tk.LEFT, padx=10)
        self.update_quiz_view()

    def validate_input(self, new_value):
        if new_value == "": return True
        if len(new_value) > 1: return False
        return new_value.isdigit() and 1 <= int(new_value) <= 5

    def update_quiz_view(self):
        question_text = preguntas_espanol[self.current_question_index]
        self.question_label.config(text=f"Pregunta {self.current_question_index + 1}/150\n\n{question_text}")
        self.answer_var.set(str(self.all_answers[self.current_question_index]) if self.all_answers[self.current_question_index] != 0 else "")
        self.answer_entry.focus_set()
        self.prev_button.config(state=tk.NORMAL if self.current_question_index > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_question_index < 149 else tk.DISABLED)

    def navigate(self, direction):
        if not self.save_current_answer(): return
        if direction == "next":
            if self.current_question_index < 149: self.current_question_index += 1; self.update_quiz_view()
            else: self.finish_quiz()
        elif direction == "prev" and self.current_question_index > 0: self.current_question_index -= 1; self.update_quiz_view()
        
    def save_current_answer(self):
        answer_str = self.answer_var.get()
        if not answer_str: self.all_answers[self.current_question_index] = 0; return True
        try:
            answer_num = int(answer_str)
            if 1 <= answer_num <= 5: self.all_answers[self.current_question_index] = answer_num; return True
            else: messagebox.showerror("Error de Validación", "Por favor, ingresa un número entre 1 y 5."); return False
        except ValueError: messagebox.showerror("Error de Validación", "Entrada no válida. Por favor, ingresa solo un número."); return False

    def finish_quiz(self):
        if not self.save_current_answer(): return
        if 0 in self.all_answers:
            first_unanswered = self.all_answers.index(0)
            messagebox.showwarning("Incompleto", f"Falta responder la pregunta #{first_unanswered + 1}.\nTe llevaremos a ella.")
            self.current_question_index = first_unanswered; self.update_quiz_view()
            return
        results_df = calculate_scores_from_answers(self.all_answers)
        self.all_individual_results = {self.current_participant_name: results_df}
        self.calculate_group_averages()
        self.show_results_screen()
    def calculate_group_averages(self):
        if not self.all_individual_results: return
        all_dfs = [df.assign(Sujeto=name) for name, df in self.all_individual_results.items()]
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df['Puntuación Estanina'] = pd.to_numeric(combined_df['Puntuación Estanina'], errors='coerce')
        self.average_results = combined_df.groupby('Dimensión')['Puntuación Estanina'].mean().round(2).reset_index()
        self.average_results.rename(columns={'Puntuación Estanina': 'Promedio Estanina'}, inplace=True)
        self.consolidated_results = combined_df.pivot(index='Sujeto', columns='Dimensión', values='Puntuación Estanina')
        
    def show_results_screen(self):
        self.clear_main_frame()
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        ttk.Label(control_frame, text="Ver resultados de:").pack(side=tk.LEFT, padx=(0, 10))
        dropdown_options = ["Promedio Grupal"] + list(self.all_individual_results.keys()) if len(self.all_individual_results) > 1 else list(self.all_individual_results.keys())
        self.view_selector = ttk.Combobox(control_frame, values=dropdown_options, state="readonly", width=40)
        self.view_selector.pack(side=tk.LEFT)
        if dropdown_options: self.view_selector.current(0)
        self.view_selector.bind("<<ComboboxSelected>>", self.update_results_view)
        
        results_frame = ttk.Frame(self.main_frame); results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.table_frame = ttk.Frame(results_frame); self.table_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10))
        
        graph_container = ttk.Frame(results_frame); graph_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fig, self.ax = plt.subplots(figsize=(7, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_container)
        toolbar = NavigationToolbar2Tk(self.canvas, graph_container); toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        bottom_frame = ttk.Frame(self.main_frame); bottom_frame.pack(fill=tk.X, pady=10, side=tk.BOTTOM)
        ttk.Button(bottom_frame, text="Exportar Vista Actual", command=self.export_current_view).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Exportar Datos Consolidados", command=self.export_consolidated).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="🏠 Volver al Inicio", command=self.show_start_screen).pack(side=tk.RIGHT, padx=5)
        
        self.update_results_view()

    def update_results_view(self, event=None):
        selected = self.view_selector.get()
        if not selected: return
        
        for widget in self.table_frame.winfo_children(): widget.destroy()
        
        is_average_view = selected == "Promedio Grupal"
        df_to_show = self.average_results if is_average_view else self.all_individual_results[selected]
        
        tree = ttk.Treeview(self.table_frame, columns=list(df_to_show.columns), show="headings", height=15)
        for col in df_to_show.columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor='center')
        for _, row in df_to_show.iterrows(): tree.insert("", "end", values=list(row))
        tree.pack(fill=tk.BOTH, expand=True)
        
        self.ax.clear()
        value_col = 'Promedio Estanina' if is_average_view else 'Puntuación Estanina'
        title = 'Perfil Grupal Promediado' if is_average_view else f'Perfil: {selected}'
        color = 'rebeccapurple' if is_average_view else 'darkcyan'
        
        # Asegurar que el orden de las dimensiones sea siempre el mismo
        dimension_order = [nombres_dimensiones[d] for d in sorted(nombres_dimensiones.keys(), key=lambda x: nombres_dimensiones[x])]
        
        # Crear una copia para evitar SettingWithCopyWarning
        df_to_plot = df_to_show.copy()
        df_to_plot['Dimensión'] = pd.Categorical(df_to_plot['Dimensión'], categories=dimension_order, ordered=True)
        df_to_plot.sort_values('Dimensión', inplace=True)
        df_to_plot[value_col] = pd.to_numeric(df_to_plot[value_col], errors='coerce').fillna(0)
        
        bars = self.ax.barh(df_to_plot['Dimensión'], df_to_plot[value_col], color=color)
        self.ax.set_xlabel('Puntuación Estanina'); self.ax.set_title(title)
        self.ax.set_xticks(range(1, 10)); self.ax.set_xlim(0, 10)
        self.ax.invert_yaxis()
        
        for bar in bars:
            width = bar.get_width()
            if width > 0: self.ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.2f}', ha='left', va='center')
            
        self.ax.fill_betweenx(self.ax.get_ylim(), 0, 3.5, color='red', alpha=0.1, label='Bajo (1-3)')
        self.ax.fill_betweenx(self.ax.get_ylim(), 3.5, 6.5, color='grey', alpha=0.1, label='Promedio (4-6)')
        self.ax.fill_betweenx(self.ax.get_ylim(), 6.5, 10, color='green', alpha=0.1, label='Alto (7-9)')
        self.ax.legend(title='Interpretación', bbox_to_anchor=(1.05, 1), loc='upper left')
        self.fig.tight_layout(rect=[0, 0, 0.82, 1])
        self.canvas.draw()
    def export_current_view(self):
        selected = self.view_selector.get()
        if not selected: return
        df_to_export = self.average_results if selected == "Promedio Grupal" else self.all_individual_results[selected]
        # Limpiar el nombre del archivo para que sea válido
        safe_filename = "".join(c for c in selected if c.isalnum() or c in (' ', '_')).rstrip()
        filename = f"resultados_promedio_grupal.csv" if selected == "Promedio Grupal" else f"resultados_{safe_filename.replace(' ', '_')}.csv"
        self.save_df_to_csv(df_to_export, filename)

    def export_consolidated(self):
        if self.consolidated_results.empty:
            messagebox.showwarning("Sin Datos", "No hay datos consolidados para exportar.")
            return
        self.save_df_to_csv(self.consolidated_results, "resultados_consolidados.csv")

    def save_df_to_csv(self, df, default_name):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], initialfile=default_name)
        if not filepath: return
        try:
            # El argumento 'index=True' es importante para el dataframe consolidado
            df.to_csv(filepath, index=True, encoding='utf-8-sig')
            messagebox.showinfo("Éxito", f"Datos guardados en:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    def download_template(self, mode):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], initialfile=f"plantilla_{mode}.csv")
        if not filepath: return
        
        if mode == 'questions':
            headers = ["Nombre del Participante o Grupo:"] + [f"{p}" for p in preguntas_espanol]
            df = pd.DataFrame(columns=headers)
            df.loc[0] = ["Ejemplo Sujeto 1"] + ["1"] * 150
            df.loc[1] = ["# Escriba las respuestas (números del 1 al 5) en las columnas siguientes"] + [""] * 150
        
        else: # mode == 'scores'
            # --- CAMBIO AQUÍ: Simplificamos los encabezados ---
            # Ahora usamos 'Sujeto' y los nombres de las dimensiones directamente.
            headers = ["Sujeto"] + list(nombres_dimensiones.values())
            df = pd.DataFrame(columns=headers)
            df.loc[0] = ["Ejemplo Grupo Alfa"] + [20] * len(nombres_dimensiones)
            df.loc[1] = ["# Escriba las puntuaciones crudas (números) en las columnas siguientes"] + [""] * len(nombres_dimensiones)
            
        try:
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            messagebox.showinfo("Plantilla Guardada", f"Se ha guardado una plantilla en:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la plantilla:\n{e}")