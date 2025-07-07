# manual_generator.py (Versión Corregida para Hemphill)

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
import traceback

def create_manual_pdf(filename="manual_hemphill.pdf"):
    """Genera un manual de usuario en formato PDF para la herramienta Hemphill."""
    try:
        doc = SimpleDocTemplate(filename)
        styles = getSampleStyleSheet()

        # --- Estilos personalizados ---
        styles.add(ParagraphStyle(name='H1', parent=styles['h1'], alignment=TA_CENTER, spaceAfter=20, fontSize=18))
        styles.add(ParagraphStyle(name='H2', parent=styles['h2'], spaceBefore=12, spaceAfter=8, fontSize=14))
        styles.add(ParagraphStyle(name='H3', parent=styles['h3'], spaceBefore=10, spaceAfter=6, fontSize=11))
        styles.add(ParagraphStyle(name='Body', parent=styles['Normal'], alignment=TA_JUSTIFY, spaceAfter=12, leading=14))

        # --- CORRECCIÓN: Modificar el estilo 'Bullet' existente en lugar de añadirlo ---
        bullet_style = styles['Bullet']
        bullet_style.firstLineIndent = 0
        bullet_style.leftIndent = 18
        bullet_style.spaceAfter = 6
        # --------------------------------------------------------------------------
        
        story = []

        title = "Manual de Usuario: Analizador de Cuestionario Hemphill"
        story.append(Paragraph(title, styles['H1']))

        story.append(Paragraph("1. Introducción", styles['H2']))
        intro_text = """
        Bienvenido al Analizador de Cuestionario Hemphill. Esta herramienta está diseñada para digitalizar y simplificar 
        el proceso de calificación e interpretación del Cuestionario de Descripción de Grupos de Hemphill. Permite tanto 
        el ingreso manual de respuestas como el procesamiento masivo de datos a través de archivos CSV, generando 
        perfiles gráficos y tablas de resultados para un análisis profundo.
        """
        story.append(Paragraph(intro_text, styles['Body']))
        story.append(Spacer(1, 0.2*inch))

        story.append(Paragraph("2. Cómo Crear un Archivo de Importación (CSV)", styles['H2']))
        story.append(Paragraph(
            "Una de las formas más eficientes de recolectar datos es a través de un formulario en línea como Google Forms. A continuación, se detalla cómo configurar un formulario para que sea 100% compatible con este programa.",
            styles['Body']
        ))
        
        steps_text = [
            "<b>Paso 1: Crear el Formulario.</b> Vaya a Google Forms y cree un nuevo formulario en blanco. Asígnele un título, como 'Cuestionario de Descripción de Grupos'.",
            "<b>Paso 2: Añadir la Pregunta de Identificación.</b> La primera pregunta <b>debe ser</b> para identificar al participante. Use el tipo 'Respuesta Corta' y escriba 'Nombre del Participante o Grupo:'. Márquela como obligatoria.",
            "<b>Paso 3: Añadir las 150 Preguntas del Cuestionario.</b> Para cada una de las 150 afirmaciones, añada una nueva pregunta de tipo <b>'Escala lineal'</b> o <b>'Cuadrícula de varias opciones'</b>. Configure el rango de <b>1 a 5</b>. En las etiquetas, escriba 'Totalmente de acuerdo' para el 1 y 'Totalmente en desacuerdo' para el 5. Copie el texto de la afirmación en el título de la pregunta y márquela como obligatoria.",
            "<b>Paso 4: Recolectar y Exportar.</b> Una vez recibidas las respuestas, vaya a la pestaña 'Respuestas' y haga clic en el icono verde de 'Crear hoja de cálculo'. En la hoja de cálculo, vaya a <b>Archivo > Descargar > Valores separados por comas (.csv)</b>. Este archivo CSV es el que importará en el programa."
        ]
        # Usar el estilo 'bullet_style' modificado
        steps_list = [ListItem(Paragraph(s, bullet_style)) for s in steps_text]
        story.append(ListFlowable(steps_list, bulletType='bullet', start='bulletchar', bulletFontSize=10, leftIndent=18))

        story.append(PageBreak())
        
        story.append(Paragraph("3. Guía de Uso del Programa", styles['H2']))

        story.append(Paragraph("3.1 Pantalla de Inicio", styles['H3']))
        story.append(Paragraph("La pantalla principal le ofrece las siguientes opciones:", styles['Body']))
        options_text = [
            "<b>📖 Ver Manual de Instrucciones:</b> Abre o descarga este manual.",
            "<b>📝 Responder Cuestionario Manualmente:</b> Para ingresar las respuestas (1-5) de un solo participante directamente en la aplicación.",
            "<b>📂 Procesar Respuestas del Cuestionario:</b> Para cargar archivos CSV (ej. de Google Forms) que contienen las respuestas numéricas de los participantes.",
            "<b>📊 Procesar Puntuaciones Crudas:</b> Para usuarios avanzados que ya han calculado las puntuaciones crudas y solo desean convertirlas a estaninas y graficarlas.",
            "<b>💾 Descargar Plantillas:</b> Para obtener archivos CSV de ejemplo que puede llenar manualmente."
        ]
        options_list = [ListItem(Paragraph(o, bullet_style)) for o in options_text]
        story.append(ListFlowable(options_list, bulletType='bullet', start='bulletchar', bulletFontSize=10, leftIndent=18))

        story.append(Paragraph("3.2 Cuestionario Manual", styles['H3']))
        story.append(Paragraph("Este modo le guía paso a paso. Primero, se le pedirá un nombre o identificador. Luego, responderá cada una de las 150 preguntas (con valores de 1 a 5). Al finalizar, si todas las preguntas están completas, se le mostrará la pantalla de resultados con su perfil individual.", styles['Body']))

        story.append(Paragraph("3.3 Procesamiento de Archivos (CSV)", styles['H3']))
        story.append(Paragraph("Permite analizar múltiples participantes a la vez. El programa generará un perfil para cada participante encontrado en los archivos y calculará un promedio grupal si hay más de uno.", styles['Body']))

        story.append(Paragraph("3.4 Pantalla de Resultados", styles['H3']))
        story.append(Paragraph("Esta es la pantalla principal de análisis:", styles['Body']))
        results_features_text = [
            "<b>Menú Desplegable:</b> Permite seleccionar qué resultado ver. Si procesó varios participantes, aparecerá la opción 'Promedio Grupal'.",
            "<b>Tabla de Resultados:</b> Muestra los valores numéricos de las puntuaciones crudas y estaninas para cada dimensión.",
            "<b>Gráfico de Perfil:</b> Visualiza las puntuaciones estaninas en un gráfico de barras, con bandas de color para una interpretación rápida (Bajo, Promedio, Alto).",
            "<b>Exportar Vista Actual:</b> Guarda un CSV de lo que está viendo actualmente (perfil individual o promedio grupal).",
            "<b>Exportar Datos Consolidados:</b> Crea un único archivo CSV con todos los resultados de todos los participantes, ideal para análisis estadísticos externos."
        ]
        results_list = [ListItem(Paragraph(r, bullet_style)) for r in results_features_text]
        story.append(ListFlowable(results_list, bulletType='bullet', start='bulletchar', bulletFontSize=10, leftIndent=18))

        doc.build(story)
        return True, None # Devuelve éxito y ningún mensaje de error
    except Exception as e:
        error_details = traceback.format_exc()
        return False, error_details # Devuelve fallo y los detalles del error