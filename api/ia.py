import re

def analizar_texto(texto):
    texto = texto.lower()

    #detectar palabras claves emocionales simples
    emociones = {
        "estres":["estres","agobiado","cansado","presionado","cansada","presionada","estresado","estresada"],
        "ansiedad":["ansiedad","ansioso","ansiosa","nervioso","preocupado","miedo"],
        "tristeza":["tristeza","deprimido","deprimida","triste"],
        "alegria":["feliz","contento","contenta","bien"]
    }

    emocion_detectada = "neutral"
    nivel_estres = 3

    for emocion, palabras in emociones.items():
        if any(p in texto for p in palabras):
            emocion_detectada = emocion
            break
    
    #calcular el nivel de estrés según palabras fuertes.
    if emocion_detectada in ["estres","ansiedad"]:
        nivel_estres = 8
    elif emocion_detectada == "tristeza":
        nivel_estres = 6
    elif emocion_detectada == "alegria":
        nivel_estres = 2

    # recomendación simple
    recomendaciones = {
        "estres": "Haz una pausa y realiza respiraciones profundas durante 2 minutos.",
        "ansiedad": "Prueba meditación corta de 5 minutos.",
        "tristeza": "Habla con alguien de confianza o con un profesional de la salud mental.",
        "alegria": "Sigue con esa energía positiva.",
        "neutral": "Realiza una pausa de estiramiento."
    }

    recomendacion = recomendaciones.get(emocion_detectada,"Realiza una pausa breve.")
    return emocion_detectada, nivel_estres, recomendacion
