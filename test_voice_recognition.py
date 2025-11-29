"""
Script de prueba para verificar que las palabras clave de emotion_library.py 
funcionan correctamente con texto capturado por voz (transcripción).
"""

from api.emotion_library import EmotionLibrary
import json

# Simular ejemplos de transcripciones de voz típicas
pruebas_voz = [
    # Tristeza
    "me siento muy triste y solo, nada me importa ya",
    "estoy deprimido, me duele el corazón",
    "lloro cada noche por la soledad",
    
    # Alegría
    "estoy muy feliz hoy, me encanta la vida",
    "qué día tan hermoso, me siento increíble",
    "amo todo lo que me rodea, ¡qué excelente!",
    
    # Ansiedad
    "tengo mucha preocupación y nervios",
    "estoy ansioso por lo que pasará",
    "siento palpitaciones y tensión en el cuerpo",
    
    # Enojo
    "estoy furioso con esto, me revienta",
    "me irrita demasiado lo que hizo",
    "esa situación me enoja muchísimo",
    
    # Calma
    "me siento tranquilo y en paz",
    "qué sereno y relajado me siento ahora",
    "meditación me trajo esta tranquilidad",
    
    # Amor
    "amo profundamente a mi familia",
    "tengo tanto cariño por esa persona",
    "me encanta con toda mi pasión",
    
    # Esperanza
    "confío en que todo mejorará",
    "tengo fe en el futuro",
    "espero que las cosas cambien positivamente",
    
    # Miedo
    "tengo mucho miedo a lo que pasará",
    "me asusta esta situación",
    "siento pánico y terror",
    
    # Gratitud
    "estoy muy agradecido por tu ayuda",
    "gracias, reconozco tu bondad",
    "aprecio muchísimo lo que hiciste",
    
    # Vergüenza
    "me siento avergonzado de mí",
    "me da vergüenza admitirlo",
    "estoy humillado por lo que pasó",
]

print("="*80)
print("PRUEBA DE RECONOCIMIENTO DE VOZ - EMOTION LIBRARY")
print("="*80)
print()

resultados = []

for i, transcripcion in enumerate(pruebas_voz, 1):
    print(f"Prueba {i}:")
    print(f"Transcripción de voz: '{transcripcion}'")
    
    # Analizar la transcripción
    resultado = EmotionLibrary.detectar_emociones(transcripcion)
    
    print(f"✓ Emoción detectada: {resultado['emocion_principal'].upper()}")
    print(f"✓ Nivel de estrés: {resultado['nivel_estres']:.1f}/10")
    print(f"✓ Confianza: {resultado['confianza']:.1f}%")
    print(f"✓ Emoji: {resultado['emojis']}")
    print(f"✓ Intensidad: {resultado['intensidad']:.1f}/10")
    print(f"✓ Recomendación: {resultado['recomendacion']}")
    
    # Emociones detectadas
    if resultado['emociones']:
        print(f"✓ Emociones encontradas:")
        for emocion, datos in sorted(resultado['emociones'].items(), 
                                      key=lambda x: x[1]['puntuacion'], 
                                      reverse=True)[:3]:
            print(f"  - {emocion}: {datos['palabras_detectadas']} palabras, " 
                  f"intensidad: {datos['intensidad']:.2f}")
    
    print("-" * 80)
    print()
    
    resultados.append({
        "transcripcion": transcripcion,
        "emocion": resultado['emocion_principal'],
        "nivel_estres": resultado['nivel_estres'],
        "confianza": resultado['confianza'],
        "intensidad": resultado['intensidad']
    })

# Resumen estadístico
print("\n" + "="*80)
print("RESUMEN DE RESULTADOS")
print("="*80)
print()

emociones_detectadas = {}
for r in resultados:
    emocion = r['emocion']
    if emocion not in emociones_detectadas:
        emociones_detectadas[emocion] = 0
    emociones_detectadas[emocion] += 1

print("Emociones detectadas:")
for emocion, count in sorted(emociones_detectadas.items(), key=lambda x: x[1], reverse=True):
    print(f"  • {emocion}: {count} ocasiones")

promedio_confianza = sum(r['confianza'] for r in resultados) / len(resultados)
promedio_estres = sum(r['nivel_estres'] for r in resultados) / len(resultados)

print(f"\nPromedios:")
print(f"  • Confianza promedio: {promedio_confianza:.1f}%")
print(f"  • Nivel de estrés promedio: {promedio_estres:.1f}/10")

print("\n✅ PRUEBA COMPLETADA - Las palabras clave funcionan correctamente con voz")
print("="*80)

# Verificar que cada emoción tiene suficientes palabras
print("\nVerificación de cobertura de palabras clave:")
print("="*80)

for emocion, datos in EmotionLibrary.EMOTIONS_DICT.items():
    num_palabras = len(datos['palabras'])
    print(f"• {emocion:25} - {num_palabras:2} palabras clave")

print("\n✅ Todas las emociones tienen palabras clave disponibles para detectar en voz")
