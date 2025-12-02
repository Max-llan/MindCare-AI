# Patrón Observer - MindCare AI

## 📋 Descripción

Este proyecto implementa el **Patrón de Diseño Observer** para gestionar eventos y notificaciones en el sistema MindCare-AI. El patrón permite que múltiples componentes (observadores) reaccionen automáticamente cuando ocurren eventos importantes en la aplicación.

## 🎯 Objetivo

Desacoplar la lógica de notificación y registro de eventos de la lógica principal del negocio, permitiendo:

- ✅ Notificaciones automáticas por email
- ✅ Registro de auditoría centralizado
- ✅ Recopilación de estadísticas en tiempo real
- ✅ Detección de patrones de comportamiento
- ✅ Generación de alertas críticas
- ✅ Persistencia de eventos en base de datos

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    EventManager                          │
│                     (Singleton)                          │
│                                                          │
│  - attach(observer)                                      │
│  - detach(observer)                                      │
│  - notify(event_type, data)                             │
└─────────────────┬───────────────────────────────────────┘
                  │
                  │ notifica
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌──────────────┐    ┌──────────────┐
│   Observer   │    │   Observer   │
│   Concreto 1 │    │   Concreto 2 │
└──────────────┘    └──────────────┘
```

## 📦 Componentes

### 1. **Subject (Observable)**
Clase base que mantiene la lista de observadores y los notifica.

```python
class Subject:
    def attach(self, observer: Observer) -> None
    def detach(self, observer: Observer) -> None
    def notify(self, event_type: str, data: Dict[str, Any]) -> None
```

### 2. **Observer (Observador)**
Interfaz abstracta que todos los observadores deben implementar.

```python
class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, data: Dict[str, Any]) -> None
```

### 3. **EventManager (Singleton)**
Gestor central de eventos que coordina todas las notificaciones.

```python
event_manager = get_event_manager()
event_manager.usuario_registrado(usuario_data)
event_manager.evaluacion_completada(...)
event_manager.usuario_login(usuario_data)
event_manager.error_ocurrido(...)
```

### 4. **Observadores Concretos**

#### 📧 EmailNotificationObserver
Envía notificaciones por correo electrónico.
- Bienvenida a nuevos usuarios
- Alertas de estrés alto
- Resúmenes de evaluaciones

#### 📝 LoggingObserver
Registra todos los eventos para auditoría.

#### 📊 StatisticsObserver
Recopila métricas y estadísticas:
- Total de usuarios registrados
- Total de análisis realizados
- Emociones más frecuentes
- Nivel promedio de estrés
- Alertas generadas

#### 💾 DatabaseObserver
Persiste eventos importantes en la base de datos.

#### 🔔 RecommendationObserver
Detecta patrones en el comportamiento del usuario:
- Estrés alto consistente
- Emociones recurrentes
- Genera recomendaciones personalizadas

#### 🚨 AlertObserver
Genera alertas para situaciones críticas:
- **Alerta Crítica**: Estrés ≥ 9/10
- **Alerta Moderada**: Estrés ≥ 7/10

## 🚀 Uso

### Integración en las Vistas

```python
from .observers import get_event_manager

# En RegistroView
event_manager = get_event_manager()
event_manager.usuario_registrado({
    "id": usuario.id,
    "nombre": usuario.nombre,
    "correo": usuario.correo,
    "fecha_creacion": usuario.fecha_creacion.isoformat()
})

# En ChatbotView
event_manager.evaluacion_completada(
    usuario_id=request.usuario.id,
    usuario_data={
        "id": request.usuario.id,
        "nombre": request.usuario.nombre,
        "correo": request.usuario.correo
    },
    emocion=emocion,
    nivel_estres=nivel_estres,
    recomendacion=recomendacion
)
```

### Crear Observadores Personalizados

```python
from api.observers import Observer, get_event_manager

class CustomObserver(Observer):
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        if event_type == "usuario_registrado":
            # Tu lógica personalizada
            print(f"Nuevo usuario: {data['usuario']['nombre']}")

# Registrar el observador
event_manager = get_event_manager()
event_manager.attach(CustomObserver())
```

## 📋 Eventos Soportados

| Evento | Descripción | Datos |
|--------|-------------|-------|
| `usuario_registrado` | Usuario nuevo se registra | `{usuario: {...}}` |
| `usuario_login` | Usuario inicia sesión | `{usuario: {...}}` |
| `evaluacion_completada` | Análisis emocional finalizado | `{usuario_id, usuario, emocion, nivel_estres, recomendacion}` |
| `analisis_estres_alto` | Nivel de estrés >= 7 | `{usuario_id, usuario, nivel_estres, ...}` |
| `error_sistema` | Error en el sistema | `{error_type, message, context}` |

## 💡 Ejemplos de Salida

### Registro de Usuario
```
INFO - Notificando evento 'usuario_registrado' a 6 observadores
INFO - 📧 EMAIL: Enviando bienvenida a usuario@example.com
INFO - 📝 LOG: {'timestamp': '2025-12-02 15:30:45', 'event': 'usuario_registrado', ...}
INFO - 📊 STATS: {'total_usuarios': 1, ...}
```

### Análisis con Estrés Alto
```
INFO - Notificando evento 'evaluacion_completada' a 6 observadores
INFO - Notificando evento 'analisis_estres_alto' a 6 observadores
WARNING - ⚠️ EMAIL: Alerta de estrés alto (8/10) para usuario@example.com
WARNING - ⚠️ ALERTA MODERADA: Usuario Juan - Estrés: 8/10
```

### Patrón Detectado
```
WARNING - 🔔 PATRÓN DETECTADO: Usuario 5 tiene estrés alto consistente
```

## 🔧 Configuración

### Habilitar/Deshabilitar Observadores

```python
# En observers.py, método _register_default_observers()
def _register_default_observers(self):
    self.attach(LoggingObserver())
    self.attach(StatisticsObserver())
    # self.attach(EmailNotificationObserver())  # Comentar para deshabilitar
    self.attach(DatabaseObserver())
    # ...
```

### Agregar Nuevos Observadores Dinámicamente

```python
from api.observers import get_event_manager, Observer

class MetricsObserver(Observer):
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        # Enviar métricas a servicio externo (ej: Prometheus)
        pass

event_manager = get_event_manager()
event_manager.attach(MetricsObserver())
```

## 🎯 Beneficios

1. **Desacoplamiento**: La lógica de negocio no depende de las notificaciones
2. **Extensibilidad**: Fácil agregar nuevos observadores sin modificar código existente
3. **Mantenibilidad**: Cada observador tiene una responsabilidad única
4. **Escalabilidad**: Los observadores pueden ejecutarse de forma asíncrona
5. **Testabilidad**: Fácil hacer mock de observadores en tests

## 🧪 Testing

```python
from api.observers import get_event_manager, Observer

class TestObserver(Observer):
    def __init__(self):
        self.events_received = []
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        self.events_received.append((event_type, data))

# En tests
test_observer = TestObserver()
event_manager = get_event_manager()
event_manager.attach(test_observer)

# Ejecutar acción que genera evento
# ...

# Verificar
assert len(test_observer.events_received) == 1
assert test_observer.events_received[0][0] == "usuario_registrado"
```

## 🚀 Mejoras Futuras

- [ ] Procesamiento asíncrono de eventos (Celery/RabbitMQ)
- [ ] Persistencia de eventos en cola (Redis/Kafka)
- [ ] Dashboard de estadísticas en tiempo real
- [ ] Webhooks para integraciones externas
- [ ] Retry logic para observadores fallidos
- [ ] Rate limiting para prevenir spam de notificaciones

## 📚 Referencias

- [Observer Pattern - Refactoring Guru](https://refactoring.guru/design-patterns/observer)
- [Observer Pattern - Gang of Four](https://en.wikipedia.org/wiki/Observer_pattern)
- [Django Signals](https://docs.djangoproject.com/en/stable/topics/signals/) (alternativa nativa de Django)

## 👨‍💻 Autor

Implementado para MindCare-AI - Sistema de Análisis Emocional
