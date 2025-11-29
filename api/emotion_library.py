"""
Librería de detección de emociones basada en palabras clave y análisis de texto.
Orientada a detectar estado emocional del usuario mediante patrones de lenguaje.
"""

import re
from collections import Counter

class EmotionLibrary:
    """
    Librería para detectar emociones a partir de texto.
    Utiliza palabras clave asociadas a diferentes emociones.
    """
    
    # Diccionario de emociones con palabras clave en español
    EMOTIONS_DICT = {
        "alegría": {
            "palabras": [
                "feliz", "alegre", "contento", "joyoso", "divertido", "risa",
                "reír", "sonrisa", "genial", "increíble", "excelente", "maravilloso",
                "asombroso", "fantástico", "hermoso", "bonito", "amor", "adoro",
                "me encanta", "amo", "afortunado", "bendito", "celebro", "éxito",
                "bien", "buen", "bueno", "positivo", "optimista", "radiante", "euforia",
                "jubilo", "regocijo", "gozo", "satisfacción", "diversión"
            ],
            "color": "🟢",
            "nivel_base": 2
        },
        "tristeza": {
            "palabras": [
                "triste", "tristeza", "deprimido", "deprimida", "solo", "soledad", "lloro",
                "llorar", "lágrimas", "dolor", "sufrimiento", "pena", "desdicha",
                "infeliz", "desgraciado", "melancólico", "afligido", "abatido",
                "desconsuelo", "angustia", "me duele", "duelo", "pérdida", "mal", "malo",
                "desaliento", "desmoralizado", "depresión", "hundido", "derrotado",
                "lágrimas", "lamento", "arrepentimiento", "nostalgia"
            ],
            "color": "🔵",
            "nivel_base": -3
        },
        "ansiedad": {
            "palabras": [
                "ansiedad", "ansioso", "ansiosa", "nervioso", "nerviosa", "preocupado", "preocupada", "preocupación",
                "estrés", "estresado", "estresada", "tensión", "tenso", "tensa", "miedo", "pánico",
                "asustado", "asustada", "inquieto", "inquieta", "intranquilo", "agitado", "agitada", "acelerado",
                "palpitaciones", "temor", "terror", "fobia", "angustiado", "angustiada", "presionado", "presionada",
                "cansado", "cansada", "agobiado", "agobiada", "desasosiego", "desazón", "zozobra", "inquietud"
            ],
            "color": "🟡",
            "nivel_base": 2
        },
        "enojo": {
            "palabras": [
                "enojo", "enojado", "furioso", "rabia", "rabioso", "ira",
                "irritado", "molesto", "enfadado", "bravo", "indignado",
                "ofendido", "furor", "cólera", "colérico", "agresivo", "violento",
                "me revienta", "me irrita", "fuera de sí", "harto", "fastidiado",
                "exasperado", "resentido", "amargado", "hostil", "desprecio", "rencor",
                "enfurecido", "provocado", "ultrajado", "indignación"
            ],
            "color": "🔴",
            "nivel_base": 2
        },
        "calma": {
            "palabras": [
                "calma", "calmado", "tranquilo", "paz", "sereno", "relajado",
                "descansado", "sosegado", "apacible", "quieto", "plácido",
                "armonía", "equilibrio", "estabilidad", "meditación", "yoga",
                "respiro", "respiro profundo", "tranquilidad", "serenidad", "sosiego",
                "serena", "paciencia", "placidez", "reposo", "descanso"
            ],
            "color": "🟣",
            "nivel_base": -2
        },
        "esperanza": {
            "palabras": [
                "esperanza", "esperanzado", "optimista", "optimismo", "confianza",
                "seguro", "confío", "confidente", "futuro", "posibilidad",
                "oportunidad", "progreso", "mejora", "cambio positivo", "creo",
                "fe", "espero", "quiero", "voy a lograr", "puedo", "seré",
                "fe", "creencia", "aspiración", "ilusión", "motivación", "determinación"
            ],
            "color": "✨",
            "nivel_base": 1
        },
        "soledad": {
            "palabras": [
                "solo", "soledad", "abandonado", "aislado", "rechazado", "excluido",
                "incomprendido", "marginal", "desconectado", "apartado", "segregado",
                "nadie entiende", "me siento solo", "todos contra mí", "sin apoyo",
                "desamparado", "desprotegido", "olvidado", "ignorado", "invisible",
                "aislamiento", "desamparo", "alejamiento", "desvinculado"
            ],
            "color": "⚫",
            "nivel_base": -3
        },
        "culpa": {
            "palabras": [
                "culpa", "culpable", "arrepentido", "remordimiento", "vergüenza",
                "avergonzado", "humillado", "culpabilidad", "responsable", "mi culpa",
                "debería haber", "no debería", "cometí", "errores", "mal", "fracaso",
                "decepción", "fallé", "me siento mal", "no meresco", "reprobación",
                "autocrítica", "autocondena", "contricción", "penitencia"
            ],
            "color": "🟤",
            "nivel_base": -2
        },
        "confusión": {
            "palabras": [
                "confundido", "confusión", "desorientado", "perdido", "sin dirección",
                "incierto", "incertidumbre", "dudoso", "duda", "no sé", "no entiendo",
                "complicado", "complejo", "lío", "desorden", "caos", "caótico",
                "desconcierto", "aturdido", "atolondrado", "turbación", "perplejidad",
                "desvarío", "desvario", "incertidumbre", "ambigüedad", "vaguedad"
            ],
            "color": "🟠",
            "nivel_base": 0
        },
        "amor": {
            "palabras": [
                "amor", "amar", "amado", "amada", "cariño", "cariñoso", "afecto",
                "afectuoso", "querido", "querida", "apasionado", "apasionada",
                "enamorado", "enamorada", "pasión", "adoración", "devoción",
                "ternura", "dulzura", "romanticismo", "conexión", "vínculo", "devoción"
            ],
            "color": "💕",
            "nivel_base": 1
        },
        "orgullo": {
            "palabras": [
                "orgullo", "orgulloso", "orgullosa", "satisfecho", "satisfecha",
                "logro", "éxito", "victoria", "triunfo", "campeón", "ganador",
                "superioridad", "dignidad", "honra", "honor", "gloria",
                "grandiosidad", "magnificencia", "prepotencia", "vanidad", "altivez"
            ],
            "color": "🏆",
            "nivel_base": 1
        },
        "vergüenza": {
            "palabras": [
                "vergüenza", "avergonzado", "avergonzada", "humillación", "humillante",
                "deshonra", "deshonroso", "ignominia", "oprobio", "bochorno",
                "rubor", "sonrojarse", "apocado", "acobardado", "tímido", "timidez",
                "bajeza", "indignidad", "descrédito", "infamia"
            ],
            "color": "😳",
            "nivel_base": -2
        },
        "admiración": {
            "palabras": [
                "admiración", "admirar", "admirado", "admirada", "asombro", "asombrado",
                "maravillado", "maravillada", "fascinación", "fascinante", "cautivador",
                "sorprendente", "sorprendente", "impresionante", "impresionado",
                "reverencia", "veneración", "respeto", "estupefacto", "pasmado"
            ],
            "color": "😲",
            "nivel_base": 1
        },
        "disgusto": {
            "palabras": [
                "asco", "asqueado", "asqueada", "repugnancia", "repugnante", "repulsivo",
                "nauseabundo", "detestable", "odio", "odio", "aborrecimiento", "aversión",
                "desagrado", "desagradable", "repulsivo", "grotesco", "inmundo",
                "inmundicia", "impureza", "vileza", "ordinariez", "tosquedad"
            ],
            "color": "🤢",
            "nivel_base": -2
        },
        "sorpresa": {
            "palabras": [
                "sorpresa", "sorprendente", "sorprendido", "sorprendida", "asombroso",
                "imprevisto", "inesperado", "casual", "fortuitamente", "de repente",
                "de pronto", "improviso", "sorpresiva", "sorpresiva", "alerta",
                "atento", "cauteloso", "expectativa", "suspense", "intriga"
            ],
            "color": "🎉",
            "nivel_base": 0
        },
        "miedo": {
            "palabras": [
                "miedo", "asustado", "asustada", "aterrado", "aterrada", "espanto",
                "espantado", "espantada", "pánico", "pánico", "pánicamente", "fobias",
                "terror", "terrorífico", "aterrador", "pavor", "pánico", "pávor",
                "escalofría", "temblor", "tiritón", "cobardía", "medroso", "temeroso"
            ],
            "color": "😨",
            "nivel_base": 2
        },
        "gratitud": {
            "palabras": [
                "gratitud", "agradecido", "agradecida", "gracias", "apreciación",
                "apreciativo", "apreciativa", "reconocimiento", "reconocido", "reconocida",
                "deuda", "favor", "bendición", "fortuna", "suerte", "privilegio",
                "beneficio", "bien", "gentileza", "amabilidad", "benevolencia"
            ],
            "color": "🙏",
            "nivel_base": 1
        },
        "frustración": {
            "palabras": [
                "frustración", "frustrado", "frustrada", "decepción", "decepcionado",
                "decepcionada", "fracaso", "fracasado", "fracasada", "impedimento",
                "obstáculo", "barrera", "bloqueo", "impotencia", "impotente", "incapaz",
                "derrota", "revés", "contratiempo", "tropiezo", "desventura"
            ],
            "color": "😤",
            "nivel_base": -1
        },
        "nostalgia": {
            "palabras": [
                "nostalgia", "nostálgico", "nostálgica", "añoranza", "añorar",
                "recuerdo", "pasado", "antaño", "tiempos lejanos", "buenos tiempos",
                "melancolía", "melancolía", "melancolía", "evocación", "remembranza",
                "reminiscencia", "ausencia", "vacío", "anhelo", "deseo", "suspiro"
            ],
            "color": "💭",
            "nivel_base": -1
        },
        "alegría_moderada": {
            "palabras": [
                "sonrisa", "sonreír", "sonriente", "humor", "cómico", "bromista",
                "jocoso", "jocosidad", "hilaridad", "diversión", "entretenimiento",
                "placer", "deleite", "regocijo", "júbilo", "dicha", "felicidad"
            ],
            "color": "😊",
            "nivel_base": 1
        },
        "compasión": {
            "palabras": [
                "compasión", "compasivo", "compasiva", "empatía", "empático", "empática",
                "solidaridad", "solidario", "solidaria", "lástima", "pena", "duelo",
                "piedad", "misericordia", "clemencia", "altruismo", "filantropía",
                "benignidad", "bondad", "humanidad", "ternura", "dulzura"
            ],
            "color": "💚",
            "nivel_base": -1
        },
        "ansiedad_anticipatoria": {
            "palabras": [
                "anticipación", "anticipado", "anticipada", "expectativa", "expectante",
                "ansia", "ansias", "aprehensión", "inquietud", "desasosiego",
                "desazón", "zozobra", "presentimiento", "premonición", "mal presagio",
                "premonitorio", "próximo", "venidero", "futuro", "inminente"
            ],
            "color": "⏰",
            "nivel_base": 1
        },
        "empoderamiento": {
            "palabras": [
                "empoderamiento", "empoderado", "empoderada", "fortaleza", "fuerza",
                "poder", "capacidad", "habilidad", "dominio", "control", "autoridad",
                "liderazgo", "lider", "decidido", "decidida", "resuelto", "resuelto",
                "determinación", "voluntad", "autodeterminación", "autonomía"
            ],
            "color": "💪",
            "nivel_base": 1
        },
        "vacío": {
            "palabras": [
                "vacío", "vacía", "nada", "nada importa", "nihilismo", "nihilista",
                "falta de sentido", "sinsentido", "propósito", "significado",
                "insignificancia", "insignificante", "futilidad", "insubstancial",
                "vano", "intangible", "inaprehensible", "inexistencia", "inexistente"
            ],
            "color": "🕳️",
            "nivel_base": -2
        },
        "alivio": {
            "palabras": [
                "alivio", "aliviado", "aliviada", "desahogo", "desahogo", "respiro",
                "aligerar", "aligerado", "aligerada", "liberación", "liberado", "liberada",
                "descarga", "descargado", "descargada", "libertad", "emancipación",
                "redención", "salvación", "consuelo", "consolación", "sosiego"
            ],
            "color": "😌",
            "nivel_base": -1
        },
        "resentimiento": {
            "palabras": [
                "resentimiento", "resentido", "resentida", "rencor", "rencoroso",
                "amargura", "amargado", "amargada", "mala voluntad", "rencilla",
                "animosidad", "hostilidad", "enemistad", "antagonismo", "oposición",
                "acritud", "severidad", "dureza", "despecho", "ofensa"
            ],
            "color": "😠",
            "nivel_base": -2
        }
    }

    # Palabras intensificadoras (aumentan la intensidad de la emoción)
    INTENSIFIERS = {
        "muy": 1.5,
        "demasiado": 1.5,
        "extremadamente": 2.0,
        "increíblemente": 2.0,
        "terriblemente": 2.0,
        "super": 1.5,
        "mega": 1.5,
        "hiper": 1.5,
        "bastante": 1.3,
        "mucho": 1.3,
        "un montón": 1.5,
        "tal": 1.2,
        "realmente": 1.2
    }

    # Palabras negadoras (invierten la emoción)
    NEGATORS = ["no", "ni", "nunca", "jamás", "tampoco", "nada"]

    @staticmethod
    def detectar_emociones(texto):
        """
        Detecta emociones en un texto y retorna análisis detallado.
        
        Args:
            texto (str): Texto a analizar
            
        Returns:
            dict: Análisis con emoción principal, intensidad y detalles
        """
        if not texto or len(texto.strip()) == 0:
            return {
                "emocion_principal": "neutral",
                "confianza": 0,
                "emociones": {},
                "nivel_estres": 5,
                "recomendacion": "Por favor escribe algo para que analicemos tu estado emocional.",
                "intensidad": 0
            }

        texto_limpio = texto.lower().strip()
        palabras = re.findall(r'\b\w+\b', texto_limpio)
        
        # Contador de emociones
        emociones_encontradas = {}
        
        for emocion, datos in EmotionLibrary.EMOTIONS_DICT.items():
            puntuacion = 0
            contador_palabras = 0
            
            for i, palabra in enumerate(palabras):
                if palabra in datos["palabras"]:
                    # Buscar intensificadores cerca
                    intensidad = 1.0
                    
                    # Revisar palabras antes
                    if i > 0 and palabras[i-1] in EmotionLibrary.INTENSIFIERS:
                        intensidad *= EmotionLibrary.INTENSIFIERS[palabras[i-1]]
                    
                    # Revisar negadores
                    if i > 0 and palabras[i-1] in EmotionLibrary.NEGATORS:
                        intensidad *= -0.5
                    
                    puntuacion += intensidad * abs(datos["nivel_base"])
                    contador_palabras += 1
            
            if contador_palabras > 0:
                emociones_encontradas[emocion] = {
                    "puntuacion": puntuacion,
                    "palabras_detectadas": contador_palabras,
                    "intensidad": min((puntuacion / contador_palabras) * 1.2, 10)
                }
        
        # Determinar emoción principal
        if emociones_encontradas:
            emocion_principal = max(emociones_encontradas, 
                                   key=lambda x: abs(emociones_encontradas[x]["puntuacion"]))
            puntuacion_max = abs(emociones_encontradas[emocion_principal]["puntuacion"])
        else:
            emocion_principal = "neutral"
            puntuacion_max = 0
        
        # Calcular nivel de estrés (0-10)
        nivel_estres = EmotionLibrary._calcular_nivel_estres(emociones_encontradas)
        
        # Calcular confianza (0-100)
        confianza = EmotionLibrary._calcular_confianza(emociones_encontradas, len(palabras))
        
        # Generar recomendación
        recomendacion = EmotionLibrary._generar_recomendacion(emocion_principal, nivel_estres)
        
        return {
            "emocion_principal": emocion_principal,
            "confianza": min(confianza, 100),
            "emociones": emociones_encontradas,
            "nivel_estres": nivel_estres,
            "recomendacion": recomendacion,
            "intensidad": min(puntuacion_max / 10, 10),
            "emojis": EmotionLibrary.EMOTIONS_DICT[emocion_principal]["color"] if emocion_principal != "neutral" else "⚪"
        }

    @staticmethod
    def _calcular_nivel_estres(emociones):
        """Calcula el nivel de estrés general (0-10) con mejor sensibilidad a emociones negativas."""
        emociones_estresantes = ["ansiedad", "enojo", "tristeza", "miedo", "culpa", "resentimiento", "ansiedad_anticipatoria"]
        
        if not emociones:
            return 0
        
        estrés_total = 0
        emociones_encontradas = 0
        
        for emocion, datos in emociones.items():
            if emocion in emociones_estresantes:
                # Usar intensidad como base
                estrés_total += datos["intensidad"]
                emociones_encontradas += 1
        
        # Calcular promedio de las emociones estresantes encontradas
        if emociones_encontradas > 0:
            promedio_estres = estrés_total / emociones_encontradas
        else:
            # Si no hay emociones estresantes, pero hay otras, calcular bajo
            promedio_estres = 0
        
        # Multiplicar por factor de amplificación para mejor sensibilidad
        nivel_estres = min(promedio_estres * 1.5, 10)
        
        return nivel_estres

    @staticmethod
    def _calcular_confianza(emociones, total_palabras):
        """Calcula la confianza del análisis (0-100)."""
        if not emociones:
            return 30
        
        total_palabras_detectadas = sum(e["palabras_detectadas"] for e in emociones.values())
        confianza_base = (total_palabras_detectadas / max(total_palabras, 1)) * 100
        
        return min(confianza_base, 100)

    @staticmethod
    def _generar_recomendacion(emocion, nivel_estres):
        """Genera una recomendación personalizada basada en la emoción detectada y el nivel de estrés."""
        recomendaciones = {
            "alegría": {
                "bajo": "¡Qué alegría! Disfruta este momento de felicidad. Considera hacer algo especial que amplíe tu sonrisa. 😊",
                "medio": "¡Excelente! Tu energía positiva es contagiosa. Comparte tu felicidad con quienes te rodean. 🌟",
                "alto": "¡Estás radiante! Aprovecha esta euforia para alcanzar tus metas. ¡El mundo está a tu alcance! 🚀"
            },
            "tristeza": {
                "bajo": "Parece que hay algo que pesa en tu corazón. Habla con alguien de confianza sobre lo que sientes. 💙",
                "medio": "Atraviesas un momento difícil. Recuerda que es temporal. Busca actividades que te traigan paz y conexión. 🌸",
                "alto": "Tu dolor es válido. Considera buscar apoyo profesional si lo necesitas. Mereces estar bien. 🤝"
            },
            "ansiedad": {
                "bajo": "Algo te preocupa un poco. Respira profundamente. Inhala 4 segundos, sostén 4, exhala 4. 🧘",
                "medio": f"Detectamos ansiedad moderada (Estrés: {nivel_estres:.1f}/10). Practica técnicas de mindfulness o camina en la naturaleza. 🌿",
                "alto": f"Tu nivel de ansiedad es alto (Estrés: {nivel_estres:.1f}/10). Tómate tiempo para relajarte. Considera meditación o busca apoyo profesional. 🕯️"
            },
            "enojo": {
                "bajo": "Hay algo que te molesta. Es normal. Respira y piensa en qué puedes cambiar de la situación. 💭",
                "medio": "Siento tu frustración. Canaliza esa energía en algo productivo: ejercicio, arte o una conversación honesta. 💪",
                "alto": "Tu rabia es comprensible. Tómate tiempo para enfriarte. Luego, verás la situación con más claridad. 🔥➡️❄️"
            },
            "calma": {
                "bajo": "Mantén esta paz. Es un tesoro. Sigue con las actividades que te generan serenidad. ✨",
                "medio": "¡Qué equilibrio! Tu bienestar es excelente. Continúa cuidándote así. 🧘‍♀️",
                "alto": "Tu paz interior es hermosa. Comparte esta tranquilidad con otros. Eres un ejemplo de serenidad. 🕊️"
            },
            "esperanza": {
                "bajo": "Pequeñas luces de esperanza siempre iluminan el camino. Alimenta esa confianza. 💡",
                "medio": "¡Qué actitud positiva! Tu confianza es tu fortaleza. Continúa adelante con determinación. 🎯",
                "alto": "¡Tu optimismo es inspirador! Cree en ti mismo. Los sueños se hacen realidad con fe y acción. ⭐"
            },
            "soledad": {
                "bajo": "A veces necesitamos soledad para reflexionar. Eso está bien. Pero recuerda que puedes conectar cuando lo necesites. 📞",
                "medio": "Te sientes un poco aislado. Llama a un amigo, únete a un grupo o actividad que disfrutes. 🤝",
                "alto": "Tu soledad pesa. Busca conexión genuina. Comunidades en línea, grupos de interés, o profesionales pueden ayudarte. 💙"
            },
            "culpa": {
                "bajo": "Una lección valiosa viene con la culpa. Aprende de ella y perdónate. 🌱",
                "medio": "La culpa nos enseña. Reflexiona sobre qué pasó y cómo puedes mejorar. El perdón propio es clave. 🕯️",
                "alto": "Tu culpa es profunda. Considera hablar con alguien de confianza o buscar asesoría. Mereces paz. 💙"
            },
            "confusión": {
                "bajo": "Hay algo poco claro. Tómate tiempo para pensar. A menudo la claridad llega con la reflexión. 💭",
                "medio": "Parece que hay incertidumbre. Divide tus preocupaciones en pasos pequeños. Habla con alguien sabio. 📝",
                "alto": "Te sientes perdido. Es normal. Busca consejo, estructura tu pensamiento, y un paso a la vez. 🧭"
            },
            "amor": {
                "bajo": "Hay amor en tu corazón. Cultívalo en ti y en tus relaciones. 💕",
                "medio": "¡Qué hermoso! Estás en un estado de afecto y conexión. Valora esos vínculos especiales. 💑",
                "alto": "¡Tu corazón está lleno de amor! Es el combustible más hermoso. Expresa ese sentimiento. 💖"
            },
            "orgullo": {
                "bajo": "Reconoce tus logros. Mereces celebrar lo que has alcanzado. 🏅",
                "medio": "¡Estás orgulloso de ti! Ese sentimiento es saludable. Mantén humildad también. 🏆",
                "alto": "Tu autoestima es fuerte. Recuerda que nadie es perfecto. La humildad suma junto al orgullo. 👑"
            },
            "vergüenza": {
                "bajo": "Algo te avergüenza. Recuerda que los errores nos hacen humanos. Puedes aprender de esto. 🌱",
                "medio": "Sientes vergüenza. Es una emoción válida pero no te define. Perdónate y sigue adelante. 🤗",
                "alto": "Tu vergüenza es intensa. Habla con alguien. No estás solo. Mereces compasión, incluso de ti mismo. 💙"
            },
            "admiración": {
                "bajo": "Encuentras inspiración en otros. Eso es hermoso. Aprende y crece. 📚",
                "medio": "Admiras profundamente. Deja que inspire tu propio crecimiento. 🌟",
                "alto": "Tu admiración es encendida. Busca ser tú también una inspiración para otros. 🦸"
            },
            "disgusto": {
                "bajo": "Algo no te agrada. Está bien alejarte de ello. Enfócate en lo que sí te importa. 🚶",
                "medio": "Tienes una aversión clara. Honra ese instinto. Tu intuición te protege. ⚠️",
                "alto": "Algo te repugna profundamente. Tómate distancia si es posible. Tu bienestar primero. 🛡️"
            },
            "sorpresa": {
                "bajo": "Algo inesperado pasó. Tómate un momento para procesar. 🤔",
                "medio": "¡Qué sorpresa! A menudo traen oportunidades. Mantén la mente abierta. 🎁",
                "alto": "¡Impresionado! Los giros inesperados pueden llevar a cosas extraordinarias. Adapta y fluye. 🌀"
            },
            "miedo": {
                "bajo": "Algo te asusta un poco. Es natural tener miedo. Respira y pregúntate: ¿qué es lo peor que podría pasar? 🧘",
                "medio": "El miedo está presente. Enfrentarlo poco a poco reduce su poder. Avanza con cautela. 🪜",
                "alto": f"Tu miedo es intenso (Estrés: {nivel_estres:.1f}/10). Busca apoyo. Habla con alguien. No tienes que enfrentar esto solo. 🤝"
            },
            "gratitud": {
                "bajo": "Pequeñas cosas por las que agradecer enriquecen la vida. Reconócelas. 🙏",
                "medio": "Tu gratitud es hermosa. Cultívala. Transforma perspectivas hacia lo positivo. ✨",
                "alto": "¡Tu gratitud es radiante! Comparte ese agradecimiento. Inspira a otros a valorar lo que tienen. 💛"
            },
            "frustración": {
                "bajo": "Algo no sale como planeado. Respira. A menudo es temporal. 🌬️",
                "medio": "La frustración es una señal. ¿Qué necesitas cambiar? Actúa o acepta lo que no puedes cambiar. 🎯",
                "alto": "Tu frustración es profunda. Tómate un descanso. Luego busca una estrategia diferente. 🔄"
            },
            "nostalgia": {
                "bajo": "Recuerdas buenos momentos. Está bien. Aprecia la memoria. 🌅",
                "medio": "Te atrae el pasado. Valora esos recuerdos pero vive el presente también. ⏳",
                "alto": "Estás muy apegado al pasado. Intenta crear nuevos buenos momentos ahora. El presente también merece tu atención. 📷"
            },
            "alivio": {
                "bajo": "Algo mejoró un poco. Continúa adelante con esa paz. 😌",
                "medio": "¡Qué alivio! Disfruta este descanso. Lo merecías. 🙌",
                "alto": "¡Tu alivio es palpable! Parece que una carga se quitó. Tómate un momento para recuperarte. 🍃"
            },
            "resentimiento": {
                "bajo": "Hay un poco de amargura. Considera perdonar para liberarte. 🕊️",
                "medio": "El resentimiento te pesa. Recuerda: perdonar no es olvidar, es liberarse. 💫",
                "alto": "Tu resentimiento es profundo. Busca ayuda profesional para sanarlo. Mereces paz. 🩹"
            },
            "vacío": {
                "bajo": "Sientes un vacío pequeño. A menudo significa que falta algo significativo. Reflexiona qué. 🔍",
                "medio": "Hay vacío en ti. Busca propósito, conexión, significado. Llena tu vida de lo que importa. 🎨",
                "alto": "Tu vacío es profundo. Habla con un profesional. Mereces encontrar significado y luz. 🌟"
            },
            "compasión": {
                "bajo": "Tu compasión es hermosa. Cultívala hacia otros y hacia ti. 🌷",
                "medio": "¡Qué corazón compasivo tienes! Ayuda a otros sin olvidarte de ti mismo. ⚖️",
                "alto": "Tu compasión es radiante. Recuerda: también mereces compasión de ti mismo. Autobien es cuidado. 💚"
            },
            "ansiedad_anticipatoria": {
                "bajo": "Algo te preocupa del futuro. Recuerda que mañana aún no llega. Vive hoy. 🌞",
                "medio": "Anticipas eventos futuros con ansiedad. Prepárate pero no obsesiones. Confía en tu capacidad. 🎒",
                "alto": "Tu ansiedad por el futuro es alta. Vuelve al presente. Práctica grounding: 5 cosas que ves, 4 que tocas... 🧊"
            },
            "empoderamiento": {
                "bajo": "Empiezas a creer en ti. Cultiva ese poder interno. 💪",
                "medio": "¡Te sientes fuerte! Esa confianza es tu mayor activo. Úsala sabiamente. ⚡",
                "alto": "¡Tu empoderamiento es inspirador! Guía a otros también. Eres más fuerte de lo que sabes. 🔥"
            },
            "alegría_moderada": {
                "bajo": "Hay alegría discreta. A veces eso es más profundo. Valóralo. 😊",
                "medio": "¡Sonríes genuinamente! Eso es verdadera felicidad sostenida. Mantén eso. 😄",
                "alto": "Tu risa es contagiosa. Crea momentos para mantener esa ligereza. ¡Necesitamos más de esto! 🎉"
            },
            "neutral": {
                "bajo": "Estás en un lugar neutral. Cuéntame más para ayudarte mejor. 👂",
                "medio": "Parece que hay equilibrio. ¿Hay algo específico que quieras compartir? Estoy aquí. 🎧",
                "alto": "Busco comprenderte mejor. ¿Cómo te sientes realmente? Dime más. 💬"
            }
        }
        
        # Determinar si el nivel de estrés es bajo, medio o alto
        if nivel_estres <= 3:
            nivel = "bajo"
        elif nivel_estres <= 6:
            nivel = "medio"
        else:
            nivel = "alto"
        
        # Obtener recomendación personalizada
        if emocion in recomendaciones:
            return recomendaciones[emocion].get(nivel, "Estamos aquí para apoyarte en tu bienestar emocional. 💙")
        else:
            return "Estamos aquí para apoyarte en tu bienestar emocional. 💙"

    @staticmethod
    def analizar_multiples(textos):
        """
        Analiza múltiples textos y retorna un resumen general.
        
        Args:
            textos (list): Lista de textos a analizar
            
        Returns:
            dict: Análisis agregado
        """
        resultados = [EmotionLibrary.detectar_emociones(t) for t in textos]
        
        # Promediar emociones
        emociones_promedio = {}
        for resultado in resultados:
            for emocion, datos in resultado["emociones"].items():
                if emocion not in emociones_promedio:
                    emociones_promedio[emocion] = []
                emociones_promedio[emocion].append(datos["intensidad"])
        
        for emocion in emociones_promedio:
            emociones_promedio[emocion] = sum(emociones_promedio[emocion]) / len(emociones_promedio[emocion])
        
        nivel_estres_promedio = sum(r["nivel_estres"] for r in resultados) / len(resultados)
        
        return {
            "analisis_total": len(resultados),
            "emociones_promedio": emociones_promedio,
            "nivel_estres_promedio": nivel_estres_promedio,
            "tendencia": "positiva" if nivel_estres_promedio < 4 else "negativa" if nivel_estres_promedio > 6 else "neutral"
        }
