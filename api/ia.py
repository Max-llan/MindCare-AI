from .emotion_library import EmotionLibrary

def analizar_texto(texto):
    """
    Analiza el texto y retorna emoción, nivel de estrés y recomendación.
    Utiliza la librería avanzada de emociones.
    """
    resultado = EmotionLibrary.detectar_emociones(texto)
    
    return (
        resultado["emocion_principal"],
        int(round(resultado["nivel_estres"])),
        resultado["recomendacion"]
    )

def obtener_analisis_completo(texto):
    """
    Retorna análisis completo con todos los detalles de emociones.
    """
    return EmotionLibrary.detectar_emociones(texto)
