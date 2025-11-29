"""
Tests para la librería de emociones.
Verifica que la detección de emociones funciona correctamente.
"""

from api.emotion_library import EmotionLibrary

# Test casos
test_cases = [
    {
        "texto": "Estoy muy triste y deprimido hoy",
        "emocion_esperada": "tristeza"
    },
    {
        "texto": "¡Estoy tan feliz! No puedo creer lo bien que me siento",
        "emocion_esperada": "alegría"
    },
    {
        "texto": "Estoy muy ansioso y nervioso por la presentación",
        "emocion_esperada": "ansiedad"
    },
    {
        "texto": "Me da mucha rabia lo que pasó, estoy furioso",
        "emocion_esperada": "enojo"
    },
    {
        "texto": "Me siento solo y abandonado",
        "emocion_esperada": "soledad"
    },
    {
        "texto": "Creo que puedo lograrlo, tengo esperanza",
        "emocion_esperada": "esperanza"
    },
]

if __name__ == "__main__":
    print("=" * 60)
    print("TESTS DE DETECCIÓN DE EMOCIONES")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        resultado = EmotionLibrary.detectar_emociones(test["texto"])
        emocion = resultado["emocion_principal"]
        correcto = "✓" if emocion == test["emocion_esperada"] else "✗"
        
        print(f"\n{correcto} Test {i}:")
        print(f"  Texto: {test['texto']}")
        print(f"  Emoción esperada: {test['emocion_esperada']}")
        print(f"  Emoción detectada: {emocion}")
        print(f"  Confianza: {resultado['confianza']:.1f}%")
        print(f"  Nivel de estrés: {resultado['nivel_estres']:.1f}/10")
        print(f"  Recomendación: {resultado['recomendacion']}")
        print(f"  Emojis: {resultado['emojis']}")
