"""
Patrón Observer para MindCare-AI
Permite notificar a múltiples observadores cuando ocurren eventos en el sistema.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
import logging

# Configurar logging
logger = logging.getLogger(__name__)


# ==========================================
#  INTERFACES BASE DEL PATRÓN OBSERVER
# ==========================================

class Observer(ABC):
    """
    Interfaz base para todos los observadores.
    Los observadores concretos deben implementar el método update().
    """
    
    @abstractmethod
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Método llamado cuando el Subject notifica un cambio.
        
        Args:
            event_type: Tipo de evento que ocurrió
            data: Datos asociados al evento
        """
        pass


class Subject:
    """
    Clase base para objetos observables (Subject).
    Mantiene una lista de observadores y los notifica cuando ocurren cambios.
    """
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """Agrega un observador a la lista."""
        if observer not in self._observers:
            self._observers.append(observer)
            logger.info(f"Observador {observer.__class__.__name__} agregado")
    
    def detach(self, observer: Observer) -> None:
        """Remueve un observador de la lista."""
        if observer in self._observers:
            self._observers.remove(observer)
            logger.info(f"Observador {observer.__class__.__name__} removido")
    
    def notify(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Notifica a todos los observadores sobre un evento.
        
        Args:
            event_type: Tipo de evento (ej: 'usuario_registrado', 'analisis_completado')
            data: Datos del evento
        """
        logger.info(f"Notificando evento '{event_type}' a {len(self._observers)} observadores")
        
        for observer in self._observers:
            try:
                observer.update(event_type, data)
            except Exception as e:
                logger.error(f"Error en observador {observer.__class__.__name__}: {str(e)}")


# ==========================================
#  OBSERVADORES CONCRETOS
# ==========================================

class EmailNotificationObserver(Observer):
    """
    Observador que envía notificaciones por email cuando ocurren eventos importantes.
    """
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Envía notificación por email según el tipo de evento."""
        
        if event_type == "usuario_registrado":
            self._enviar_email_bienvenida(data)
        
        elif event_type == "analisis_estres_alto":
            self._enviar_alerta_estres(data)
        
        elif event_type == "evaluacion_completada":
            self._enviar_resumen_evaluacion(data)
    
    def _enviar_email_bienvenida(self, data: Dict[str, Any]) -> None:
        """Simula envío de email de bienvenida."""
        usuario = data.get('usuario')
        logger.info(f"📧 EMAIL: Enviando bienvenida a {usuario.get('correo', 'N/A')}")
        # Aquí integrarías un servicio real de email (SendGrid, AWS SES, etc.)
    
    def _enviar_alerta_estres(self, data: Dict[str, Any]) -> None:
        """Simula envío de alerta por estrés alto."""
        usuario = data.get('usuario')
        nivel_estres = data.get('nivel_estres')
        logger.warning(f"⚠️ EMAIL: Alerta de estrés alto ({nivel_estres}/10) para {usuario.get('correo', 'N/A')}")
    
    def _enviar_resumen_evaluacion(self, data: Dict[str, Any]) -> None:
        """Simula envío de resumen de evaluación."""
        usuario = data.get('usuario')
        emocion = data.get('emocion')
        logger.info(f"📊 EMAIL: Resumen de evaluación ({emocion}) para {usuario.get('correo', 'N/A')}")


class LoggingObserver(Observer):
    """
    Observador que registra todos los eventos en logs para auditoría.
    """
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Registra el evento en los logs."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = {
            "timestamp": timestamp,
            "event": event_type,
            "data": data
        }
        
        logger.info(f"📝 LOG: {log_entry}")
        
        # Aquí podrías guardar en una base de datos o archivo
        # Por ejemplo: guardar en tabla de auditoría


class StatisticsObserver(Observer):
    """
    Observador que recopila estadísticas sobre los eventos del sistema.
    """
    
    def __init__(self):
        self.stats = {
            "total_usuarios": 0,
            "total_analisis": 0,
            "emociones_detectadas": {},
            "nivel_estres_promedio": 0,
            "alertas_estres_alto": 0
        }
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Actualiza estadísticas según el evento."""
        
        if event_type == "usuario_registrado":
            self.stats["total_usuarios"] += 1
        
        elif event_type == "evaluacion_completada":
            self.stats["total_analisis"] += 1
            
            emocion = data.get("emocion", "neutral")
            if emocion not in self.stats["emociones_detectadas"]:
                self.stats["emociones_detectadas"][emocion] = 0
            self.stats["emociones_detectadas"][emocion] += 1
            
            # Calcular promedio de estrés
            nivel_estres = data.get("nivel_estres", 0)
            total_prev = self.stats["nivel_estres_promedio"] * (self.stats["total_analisis"] - 1)
            self.stats["nivel_estres_promedio"] = (total_prev + nivel_estres) / self.stats["total_analisis"]
        
        elif event_type == "analisis_estres_alto":
            self.stats["alertas_estres_alto"] += 1
        
        logger.info(f"📊 STATS: {self.stats}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna las estadísticas actuales."""
        return self.stats.copy()


class DatabaseObserver(Observer):
    """
    Observador que persiste eventos importantes en la base de datos.
    """
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Guarda el evento en la base de datos."""
        
        try:
            # Importación local para evitar dependencias circulares
            from .models import EvaluacionEmocional
            
            if event_type == "evaluacion_completada":
                # Ya se guarda en la vista, pero aquí podrías agregar metadata adicional
                logger.info(f"💾 DB: Evaluación guardada correctamente")
            
            # Aquí podrías crear un modelo EventLog para guardar todos los eventos
            # EventLog.objects.create(event_type=event_type, data=data, timestamp=datetime.now())
            
        except Exception as e:
            logger.error(f"Error guardando en base de datos: {str(e)}")


class RecommendationObserver(Observer):
    """
    Observador que genera recomendaciones personalizadas basadas en patrones de uso.
    """
    
    def __init__(self):
        self.user_history = {}  # {usuario_id: [evaluaciones]}
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Analiza patrones y genera recomendaciones."""
        
        if event_type == "evaluacion_completada":
            usuario_id = data.get("usuario_id")
            
            if usuario_id not in self.user_history:
                self.user_history[usuario_id] = []
            
            self.user_history[usuario_id].append({
                "emocion": data.get("emocion"),
                "nivel_estres": data.get("nivel_estres"),
                "fecha": datetime.now()
            })
            
            # Detectar patrones
            self._detectar_patrones(usuario_id)
    
    def _detectar_patrones(self, usuario_id: int) -> None:
        """Detecta patrones en el historial del usuario."""
        historial = self.user_history.get(usuario_id, [])
        
        if len(historial) >= 3:
            # Analizar últimas 3 evaluaciones
            ultimas_3 = historial[-3:]
            niveles_estres = [e["nivel_estres"] for e in ultimas_3]
            
            if all(n > 7 for n in niveles_estres):
                logger.warning(f"🔔 PATRÓN DETECTADO: Usuario {usuario_id} tiene estrés alto consistente")
                # Aquí podrías generar una recomendación especial o alertar a un profesional


class AlertObserver(Observer):
    """
    Observador que genera alertas cuando se detectan situaciones críticas.
    """
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Genera alertas para situaciones críticas."""
        
        if event_type == "analisis_estres_alto":
            nivel_estres = data.get("nivel_estres")
            usuario = data.get("usuario", {})
            
            if nivel_estres >= 9:
                self._alerta_critica(usuario, nivel_estres)
            elif nivel_estres >= 7:
                self._alerta_moderada(usuario, nivel_estres)
    
    def _alerta_critica(self, usuario: Dict, nivel_estres: int) -> None:
        """Genera alerta crítica."""
        logger.critical(f"🚨 ALERTA CRÍTICA: Usuario {usuario.get('nombre')} - Estrés: {nivel_estres}/10")
        # Aquí podrías:
        # - Enviar notificación push
        # - Notificar a un profesional de salud mental
        # - Ofrecer recursos de ayuda inmediata
    
    def _alerta_moderada(self, usuario: Dict, nivel_estres: int) -> None:
        """Genera alerta moderada."""
        logger.warning(f"⚠️ ALERTA MODERADA: Usuario {usuario.get('nombre')} - Estrés: {nivel_estres}/10")
        # Enviar sugerencias de técnicas de relajación


# ==========================================
#  SINGLETON DEL EVENTO MANAGER
# ==========================================

class EventManager(Subject):
    """
    Gestor central de eventos (Singleton).
    Coordina la notificación de eventos a todos los observadores registrados.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        super().__init__()
        self._initialized = True
        
        # Registrar observadores por defecto
        self._register_default_observers()
    
    def _register_default_observers(self):
        """Registra los observadores predeterminados del sistema."""
        self.attach(LoggingObserver())
        self.attach(StatisticsObserver())
        self.attach(EmailNotificationObserver())
        self.attach(DatabaseObserver())
        self.attach(RecommendationObserver())
        self.attach(AlertObserver())
        
        logger.info("✅ Observadores predeterminados registrados")
    
    # Métodos de conveniencia para eventos específicos
    
    def usuario_registrado(self, usuario_data: Dict[str, Any]) -> None:
        """Notifica que un usuario se registró."""
        self.notify("usuario_registrado", {"usuario": usuario_data})
    
    def evaluacion_completada(self, usuario_id: int, usuario_data: Dict, 
                             emocion: str, nivel_estres: int, 
                             recomendacion: str) -> None:
        """Notifica que se completó una evaluación emocional."""
        data = {
            "usuario_id": usuario_id,
            "usuario": usuario_data,
            "emocion": emocion,
            "nivel_estres": nivel_estres,
            "recomendacion": recomendacion,
            "timestamp": datetime.now().isoformat()
        }
        
        self.notify("evaluacion_completada", data)
        
        # Si el estrés es alto, generar evento adicional
        if nivel_estres >= 7:
            self.notify("analisis_estres_alto", data)
    
    def usuario_login(self, usuario_data: Dict[str, Any]) -> None:
        """Notifica que un usuario inició sesión."""
        self.notify("usuario_login", {"usuario": usuario_data})
    
    def error_ocurrido(self, error_type: str, error_message: str, 
                       context: Dict[str, Any]) -> None:
        """Notifica que ocurrió un error en el sistema."""
        self.notify("error_sistema", {
            "error_type": error_type,
            "message": error_message,
            "context": context,
            "timestamp": datetime.now().isoformat()
        })


# ==========================================
#  FUNCIÓN HELPER PARA OBTENER EL MANAGER
# ==========================================

def get_event_manager() -> EventManager:
    """
    Retorna la instancia única del EventManager.
    
    Returns:
        EventManager: Instancia singleton del gestor de eventos
    """
    return EventManager()
