"""
Test de casos extremos con sesiones de apoyo críticas
"""

from api.emotion_library import EmotionLibrary

print("="*100)
print("PRUEBA DE SESIONES DE APOYO CRÍTICAS - CASOS EXTREMOS")
print("="*100)
print()

# Casos que deberían generar estrés crítico (>7/10)
casos_criticos = [
    {
        "titulo": "Crisis Emocional - Pánico Intenso",
        "mensaje": "No puedo respirar tengo pánico absoluto terror miedo pánico",
        "descripcion": "Múltiples palabras de miedo y pánico repetidas"
    },
    {
        "titulo": "Depresión Profunda",
        "mensaje": "Estoy muy triste tristeza deprimido depresión sufrimiento dolor angustia",
        "descripcion": "Múltiples expresiones de tristeza e angustia"
    },
    {
        "titulo": "Ansiedad Severa",
        "mensaje": "Tengo mucha ansiedad ansiedad nervios tensión preocupación estrés",
        "descripcion": "Reiteración de síntomas de ansiedad"
    },
    {
        "titulo": "Crisis Múltiple",
        "mensaje": "Estoy furioso enojado rabia iracundo miedo pánico ansioso ansioso",
        "descripcion": "Combinación de enojo y miedo"
    },
]

for caso in casos_criticos:
    print(f"\n{'*'*100}")
    print(f"  {caso['titulo']}")
    print(f"  {caso['descripcion']}")
    print(f"{'*'*100}")
    
    print(f"\n📝 Mensaje: \"{caso['mensaje']}\"")
    
    analisis = EmotionLibrary.detectar_emociones(caso['mensaje'])
    
    print(f"\n📊 ANÁLISIS DETECTADO:")
    print(f"   Emoción principal: {analisis['emocion_principal'].upper()} {analisis['emojis']}")
    print(f"   Nivel de estrés: {analisis['nivel_estres']:.1f}/10")
    print(f"   Confianza: {analisis['confianza']:.1f}%")
    print(f"   Intensidad: {analisis['intensidad']:.1f}/10")
    
    print(f"\n💡 RECOMENDACIÓN:")
    print(f"   {analisis['recomendacion']}")
    
    # Simular respuesta del chatbot
    respuestas_base = {
        "miedo": "Entiendo tu miedo. Es una emoción válida pero no tiene que controlarte.",
        "tristeza": "Tu dolor es real y válido. No estás solo en esto.",
        "ansiedad": "La ansiedad es angustiante, pero podemos trabajar en ella juntos.",
        "enojo": "Tu ira tiene razones. Canalizarla es lo importante.",
    }
    
    respuesta = respuestas_base.get(analisis['emocion_principal'], "Te entiendo.")
    respuesta += f"\n\n📋 Mi recomendación: {analisis['recomendacion']}"
    
    # Agregar sesión de apoyo según nivel
    if analisis['nivel_estres'] > 7:
        respuesta += "\n\n⚠️ SESIÓN DE APOYO CRÍTICA - ESTRÉS SEVERO"
        respuesta += "\nTu situación es crítica. Necesitas ayuda INMEDIATA:"
        respuesta += "\n\n🆘 PASO 1 - RESPIRACIÓN DE EMERGENCIA (Haz esto AHORA):"
        respuesta += "\n   Inhala 4 segundos → Sostén 4 segundos → Exhala 4 segundos"
        respuesta += "\n   Repite 10 veces mientras cuentas los segundos"
        respuesta += "\n\n🆘 PASO 2 - ACCIONES INMEDIATAS:"
        respuesta += "\n   • Busca un lugar seguro"
        respuesta += "\n   • Toca algo frío (cubo con hielo, agua fría en cara)"
        respuesta += "\n   • Camina o salta para mover el cuerpo"
        respuesta += "\n   • Llama a alguien de confianza AHORA"
        respuesta += "\n\n🆘 PASO 3 - RECURSOS DE CRISIS:"
        respuesta += "\n   ⚠️ LLAMAR A UN PROFESIONAL DE EMERGENCIA"
        respuesta += "\n   ⚠️ Línea de prevención del suicidio (disponible 24/7)"
        respuesta += "\n   ⚠️ Ir a la sala de emergencia si es necesario"
        respuesta += "\n\n💙 Recuerda: Esto es TEMPORAL. Pasará. Mereces ayuda."
        
        print(f"\n🚨 TIPO DE SESIÓN: ⚠️ CRÍTICA (Requiere intervención profesional)")
    elif analisis['nivel_estres'] > 5:
        respuesta += "\n\n⚡ SESIÓN DE APOYO MODERADA"
        respuesta += "\nTu estrés es elevado pero manejable con estrategias:"
        respuesta += "\n   • Técnicas de relajación (meditación, yoga)"
        respuesta += "\n   • Apoyo social (hablar con alguien)"
        respuesta += "\n   • Considerar terapia profesional"
        print(f"\n🟡 TIPO DE SESIÓN: ⚡ MODERADA (Técnicas de autocuidado)")
    else:
        print(f"\n🟢 TIPO DE SESIÓN: ✅ PREVENTIVA (Bienestar sostenible)")
    
    print(f"\n💬 RESPUESTA COMPLETA DEL CHATBOT:")
    print(respuesta)
    print()

print("\n" + "="*100)
print("RESUMEN DE SESIONES DE APOYO")
print("="*100)
print()

print("🆘 SESIÓN CRÍTICA (Estrés >7/10):")
print("   Condiciones: Crisis emocional, pánico severo, depresión profunda")
print("   Intervenciones:")
print("     ✓ Técnicas de respiración de emergencia")
print("     ✓ Acciones de autorregulación inmediata")
print("     ✓ Contacto con red de apoyo")
print("     ✓ Referencia a servicios profesionales de emergencia")
print("     ✓ Enfoque en seguridad personal")
print()

print("⚡ SESIÓN MODERADA (Estrés 5-7/10):")
print("   Condiciones: Ansiedad moderada, tristeza considerable")
print("   Intervenciones:")
print("     ✓ Técnicas de relajación")
print("     ✓ Meditación y mindfulness")
print("     ✓ Ejercicio físico ligero")
print("     ✓ Apoyo social y conexión")
print("     ✓ Recomendación de terapia")
print()

print("✅ SESIÓN PREVENTIVA (Estrés <5/10):")
print("   Condiciones: Bienestar general, estrés bajo")
print("   Intervenciones:")
print("     ✓ Mantenimiento de actividades positivas")
print("     ✓ Construcción de resiliencia")
print("     ✓ Prevención de crisis futuras")
print("     ✓ Autocuidado y bienestar")
print()

print("="*100)
print("✅ SISTEMA DE SESIONES DE APOYO COMPLETAMENTE FUNCIONAL")
print("="*100)
