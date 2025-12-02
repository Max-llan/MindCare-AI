# 🧠 MindCare AI - Plataforma de Análisis Emocional

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Status](https://img.shields.io/badge/Status-Active-success)

> **Sistema inteligente de análisis emocional que detecta estrés, ansiedad y proporciona recomendaciones personalizadas mediante IA**

---

## 📋 ¿Qué es MindCare AI?

MindCare AI es una plataforma web que ayuda a las personas a **entender y gestionar su estado emocional** mediante:

- ✅ **Análisis de texto** basado en Inteligencia Artificial
- ✅ **Chatbot emocional** que comprende tus sentimientos
- ✅ **Detección de 25+ emociones** (alegría, tristeza, ansiedad, etc.)
- ✅ **Medición de estrés** en escala 0-10
- ✅ **Recomendaciones personalizadas** según tu estado
- ✅ **Alertas automáticas** cuando detecta estrés crítico

---

## 🎯 Problema que Resuelve

Muchas personas no saben identificar o manejar sus emociones. MindCare AI:

1. **Escucha** lo que escribes o dices
2. **Analiza** tus palabras con algoritmos de IA
3. **Detecta** tu emoción principal y nivel de estrés
4. **Recomienda** técnicas específicas de bienestar
5. **Alerta** cuando detecta situaciones críticas

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────┐
│              FRONTEND (HTML/CSS/JS)                  │
│  • Página de inicio                                  │
│  • Registro/Login                                    │
│  • Chat emocional con IA                            │
└──────────────────┬──────────────────────────────────┘
                   │
                   ↓ HTTP/REST API
┌─────────────────────────────────────────────────────┐
│           BACKEND (Django + REST Framework)          │
│  • Autenticación JWT                                 │
│  • API de análisis emocional                        │
│  • Gestión de usuarios                              │
│  • Patrón Observer para eventos                     │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ↓                     ↓
┌──────────────┐    ┌──────────────────┐
│ PostgreSQL   │    │  Emotion Library │
│   Database   │    │  (IA de análisis)│
└──────────────┘    └──────────────────┘
```

---

## 🚀 Tecnologías Utilizadas

### Backend
- **Python 3.11** - Lenguaje principal
- **Django 5.2** - Framework web
- **Django REST Framework** - API RESTful
- **PostgreSQL** - Base de datos
- **JWT** - Autenticación segura

### Frontend
- **HTML5/CSS3** - Estructura y diseño
- **JavaScript (Vanilla)** - Interactividad
- **Bootstrap 5** - Diseño responsivo
- **Web Speech API** - Reconocimiento de voz

### IA y Análisis
- **Emotion Library** (Propia) - 25+ emociones detectables
- **Algoritmos de NLP** - Procesamiento de lenguaje natural
- **Análisis de patrones** - Detección de palabras clave

### Patrones de Diseño
- **Observer Pattern** - Sistema de eventos y notificaciones
- **Singleton Pattern** - Gestor de eventos centralizado

---

## 📂 Estructura del Proyecto

```
MindCare-AI/
│
├── api/                          # Aplicación principal
│   ├── models.py                 # Modelos (Usuario, Evaluación)
│   ├── views.py                  # Lógica de las vistas
│   ├── serializers.py            # Serializadores REST
│   ├── observers.py              # Patrón Observer (eventos)
│   ├── emotion_library.py        # IA de análisis emocional
│   ├── ia.py                     # Funciones de IA
│   ├── auth_decorators.py        # Seguridad JWT
│   └── tests.py                  # Tests unitarios
│
├── mindcare/                     # Configuración Django
│   ├── settings.py               # Configuración principal
│   ├── urls.py                   # Rutas del sistema
│   └── wsgi.py                   # Servidor WSGI
│
├── templates/                    # Plantillas HTML
│   ├── index.html                # Página principal
│   ├── registro.html             # Registro de usuarios
│   ├── login.html                # Inicio de sesión
│   └── analizar.html             # Chat emocional
│
├── manage.py                     # CLI de Django
├── requirements.txt              # Dependencias Python
└── README.md                     # Este archivo
```

---

## 💡 Funcionalidades Principales

### 1. **Sistema de Registro y Autenticación**
- Registro con validación de contraseñas seguras
- Login con JWT (JSON Web Tokens)
- Sesiones persistentes
- Protección de rutas

### 2. **Análisis Emocional Inteligente**
- Detecta **25+ emociones**:
  - Positivas: alegría, calma, esperanza, gratitud, amor
  - Negativas: tristeza, ansiedad, enojo, miedo, soledad
  - Complejas: nostalgia, frustración, vergüenza, orgullo
- Mide **nivel de estrés** (0-10)
- Calcula **confianza del análisis** (0-100%)

### 3. **Chatbot Emocional**
- Conversación natural en español
- Reconocimiento de voz (Web Speech API)
- Respuestas empáticas personalizadas
- Historial de análisis en tiempo real

### 4. **Recomendaciones Personalizadas**
- Técnicas de respiración
- Ejercicios de mindfulness
- Consejos según la emoción detectada
- Sesiones de apoyo por nivel de estrés:
  - **Bajo** (0-3): Bienestar sostenible
  - **Moderado** (4-6): Estrategias de autocuidado
  - **Alto** (7-10): Apoyo inmediato y recursos de crisis

### 5. **Sistema de Alertas (Patrón Observer)**
- **Email** de bienvenida al registrarse
- **Alertas** cuando el estrés es alto (≥7)
- **Estadísticas** en tiempo real
- **Logs** de auditoría
- **Detección de patrones** de comportamiento

---

## 🎨 Interfaz de Usuario

### Página Principal
- Diseño moderno con gradientes
- Información clara sobre el servicio
- Acceso rápido al análisis

### Chat Emocional
```
┌────────────────────────────────────────────┐
│  💬 Chatbot Emocional                      │
├────────────────────────────────────────────┤
│                                            │
│  Bot: ¿Cómo te sientes hoy?               │
│                                            │
│            Usuario: Me siento ansioso 😟   │
│                                            │
│  Bot: Detecté algo de preocupación...     │
│       📋 Recomendación: Respira profundo  │
│                                            │
├────────────────────────────────────────────┤
│  [Escribe tu mensaje...]  [🎤] [Enviar]   │
└────────────────────────────────────────────┘

┌────────────────────────┐
│  📊 Análisis           │
├────────────────────────┤
│  😰 ANSIEDAD           │
│  Estrés: 7/10 ⚠️       │
│  Confianza: 85%        │
│                        │
│  💡 Recomendación      │
│  Practica técnicas...  │
└────────────────────────┘
```

---

## 🔬 Cómo Funciona la IA

### Algoritmo de Detección de Emociones

```python
1. Recibe texto del usuario
   ↓
2. Limpia y tokeniza el texto
   ↓
3. Busca palabras clave en diccionario emocional
   ↓
4. Detecta intensificadores ("muy", "demasiado")
   ↓
5. Identifica negaciones ("no", "nunca")
   ↓
6. Calcula puntuación por emoción
   ↓
7. Determina emoción principal
   ↓
8. Calcula nivel de estrés (0-10)
   ↓
9. Genera recomendación personalizada
   ↓
10. Retorna análisis completo
```

### Ejemplo de Detección

**Input:** "Estoy muy estresado con el trabajo"

**Proceso:**
- Detecta: "estresado" → Emoción: ansiedad
- Detecta: "muy" → Intensificador (×1.5)
- Contexto: "trabajo" → Aumenta nivel de estrés
- Resultado: **Ansiedad, Estrés: 7/10**

---

## 🔐 Seguridad

- ✅ **Contraseñas hasheadas** con PBKDF2
- ✅ **Autenticación JWT** con expiración
- ✅ **Validación de entrada** en todos los formularios
- ✅ **CSRF Protection** activada
- ✅ **HTTPS** en producción
- ✅ **Variables de entorno** para datos sensibles

---

## 📊 Patrón Observer Implementado

El sistema usa el **patrón de diseño Observer** para manejar eventos:

```
Evento Ocurre → EventManager → Notifica a todos los Observadores
                                        ↓
              ┌─────────────────────────┼──────────────────────┐
              ↓                         ↓                      ↓
       EmailObserver             LogObserver           StatsObserver
       (Envía emails)           (Guarda logs)        (Métricas)
```

### Observadores Implementados:
1. **EmailNotificationObserver** - Notificaciones por correo
2. **LoggingObserver** - Registro de auditoría
3. **StatisticsObserver** - Métricas del sistema
4. **DatabaseObserver** - Persistencia de eventos
5. **RecommendationObserver** - Detección de patrones
6. **AlertObserver** - Alertas críticas

---

## 🚀 Instalación y Uso

### Requisitos Previos
- Python 3.11+
- PostgreSQL 12+
- pip (gestor de paquetes)

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/MindCare-AI.git
cd MindCare-AI

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Crear archivo .env con:
# db_name=tu_base_datos
# db_user=tu_usuario
# db_password=tu_contraseña
# db_host=localhost
# db_port=5432

# 5. Migrar base de datos
python manage.py migrate

# 6. Ejecutar servidor
python manage.py runserver
```

### Acceder a la aplicación
Abrir navegador en: `http://localhost:8000`


---

## 📱 Endpoints de la API

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/registro/` | Registrar nuevo usuario | No |
| POST | `/api/login/` | Iniciar sesión | No |
| POST | `/api/chatbot/` | Analizar mensaje emocional | Sí |
| GET | `/api/evaluaciones/` | Obtener historial | Sí |
| POST | `/api/evaluaciones/` | Crear evaluación | Sí |



---


## 🎓 Casos de Uso

### 1. Estudiante con Estrés Académico
```
Usuario: "Tengo muchos exámenes y me siento abrumado"
Sistema: Detecta ansiedad (8/10)
Acción: Recomienda técnicas de respiración + alerta moderada
```

### 2. Persona con Día Positivo
```
Usuario: "¡Estoy súper feliz! Conseguí el trabajo"
Sistema: Detecta alegría (2/10 estrés)
Acción: Refuerza la emoción positiva
```

### 3. Usuario con Patrón de Estrés Alto
```
Sistema detecta 3 análisis seguidos con estrés > 7
Acción: RecommendationObserver alerta patrón crítico
Resultado: Sugiere contactar profesional
```

---

## 🔮 Mejoras Futuras

- [ ] **Integración con WhatsApp** para acceso móvil
- [ ] **Gráficos de evolución** emocional
- [ ] **Modelo de ML** con TensorFlow/PyTorch
- [ ] **Soporte multi-idioma** (inglés, portugués)
- [ ] **App móvil** nativa (React Native)
- [ ] **Integración con wearables** (frecuencia cardíaca)
- [ ] **Recomendaciones de profesionales** cercanos
- [ ] **Comunidad de apoyo** entre usuarios

---


**¡MindCare AI - Cuidando tu bienestar emocional con tecnología! 🧠💙**

---

