"""
Tests unitarios para el patrón Observer
"""

import unittest
from datetime import datetime
from api.observers import (
    Observer,
    Subject,
    EventManager,
    EmailNotificationObserver,
    LoggingObserver,
    StatisticsObserver,
    AlertObserver,
    get_event_manager
)


class TestObserver(Observer):
    """Observador de prueba para testing"""
    
    def __init__(self):
        self.events_received = []
    
    def update(self, event_type: str, data: dict) -> None:
        self.events_received.append({
            'event_type': event_type,
            'data': data,
            'timestamp': datetime.now()
        })


class TestSubject(unittest.TestCase):
    """Tests para la clase Subject"""
    
    def setUp(self):
        self.subject = Subject()
        self.observer1 = TestObserver()
        self.observer2 = TestObserver()
    
    def test_attach_observer(self):
        """Probar que se puede agregar un observador"""
        self.subject.attach(self.observer1)
        self.assertIn(self.observer1, self.subject._observers)
    
    def test_attach_multiple_observers(self):
        """Probar que se pueden agregar múltiples observadores"""
        self.subject.attach(self.observer1)
        self.subject.attach(self.observer2)
        self.assertEqual(len(self.subject._observers), 2)
    
    def test_detach_observer(self):
        """Probar que se puede remover un observador"""
        self.subject.attach(self.observer1)
        self.subject.detach(self.observer1)
        self.assertNotIn(self.observer1, self.subject._observers)
    
    def test_notify_observers(self):
        """Probar que notify() llama a update() en todos los observadores"""
        self.subject.attach(self.observer1)
        self.subject.attach(self.observer2)
        
        test_data = {"message": "test event"}
        self.subject.notify("test_event", test_data)
        
        self.assertEqual(len(self.observer1.events_received), 1)
        self.assertEqual(len(self.observer2.events_received), 1)
        self.assertEqual(self.observer1.events_received[0]['event_type'], "test_event")
        self.assertEqual(self.observer1.events_received[0]['data'], test_data)


class TestEventManager(unittest.TestCase):
    """Tests para EventManager (Singleton)"""
    
    def test_singleton_pattern(self):
        """Verificar que EventManager es un Singleton"""
        manager1 = get_event_manager()
        manager2 = get_event_manager()
        self.assertIs(manager1, manager2)
    
    def test_default_observers_registered(self):
        """Verificar que los observadores por defecto están registrados"""
        manager = get_event_manager()
        self.assertGreater(len(manager._observers), 0)
    
    def test_usuario_registrado_event(self):
        """Probar evento usuario_registrado"""
        manager = get_event_manager()
        test_observer = TestObserver()
        manager.attach(test_observer)
        
        usuario_data = {
            "id": 1,
            "nombre": "Test User",
            "correo": "test@example.com"
        }
        
        manager.usuario_registrado(usuario_data)
        
        # Verificar que el evento fue recibido
        received_events = [e for e in test_observer.events_received 
                          if e['event_type'] == 'usuario_registrado']
        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0]['data']['usuario']['nombre'], "Test User")
    
    def test_evaluacion_completada_event(self):
        """Probar evento evaluacion_completada"""
        manager = get_event_manager()
        test_observer = TestObserver()
        manager.attach(test_observer)
        
        manager.evaluacion_completada(
            usuario_id=1,
            usuario_data={"id": 1, "nombre": "Test", "correo": "test@example.com"},
            emocion="alegría",
            nivel_estres=3,
            recomendacion="Mantén tu energía positiva"
        )
        
        received_events = [e for e in test_observer.events_received 
                          if e['event_type'] == 'evaluacion_completada']
        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0]['data']['emocion'], "alegría")
    
    def test_analisis_estres_alto_event(self):
        """Probar que se genera evento adicional cuando estrés es alto"""
        manager = get_event_manager()
        test_observer = TestObserver()
        manager.attach(test_observer)
        
        manager.evaluacion_completada(
            usuario_id=1,
            usuario_data={"id": 1, "nombre": "Test", "correo": "test@example.com"},
            emocion="ansiedad",
            nivel_estres=8,
            recomendacion="Practica técnicas de relajación"
        )
        
        # Debe generar 2 eventos: evaluacion_completada y analisis_estres_alto
        self.assertGreaterEqual(len(test_observer.events_received), 2)
        
        estres_alto_events = [e for e in test_observer.events_received 
                             if e['event_type'] == 'analisis_estres_alto']
        self.assertEqual(len(estres_alto_events), 1)


class TestStatisticsObserver(unittest.TestCase):
    """Tests para StatisticsObserver"""
    
    def setUp(self):
        self.stats_observer = StatisticsObserver()
    
    def test_count_usuarios(self):
        """Probar conteo de usuarios registrados"""
        self.stats_observer.update("usuario_registrado", {"usuario": {"nombre": "User1"}})
        self.stats_observer.update("usuario_registrado", {"usuario": {"nombre": "User2"}})
        
        self.assertEqual(self.stats_observer.stats["total_usuarios"], 2)
    
    def test_count_analisis(self):
        """Probar conteo de análisis"""
        self.stats_observer.update("evaluacion_completada", {
            "emocion": "alegría",
            "nivel_estres": 2
        })
        self.stats_observer.update("evaluacion_completada", {
            "emocion": "calma",
            "nivel_estres": 3
        })
        
        self.assertEqual(self.stats_observer.stats["total_analisis"], 2)
    
    def test_emotions_tracking(self):
        """Probar seguimiento de emociones"""
        self.stats_observer.update("evaluacion_completada", {
            "emocion": "alegría",
            "nivel_estres": 2
        })
        self.stats_observer.update("evaluacion_completada", {
            "emocion": "alegría",
            "nivel_estres": 3
        })
        self.stats_observer.update("evaluacion_completada", {
            "emocion": "tristeza",
            "nivel_estres": 6
        })
        
        self.assertEqual(self.stats_observer.stats["emociones_detectadas"]["alegría"], 2)
        self.assertEqual(self.stats_observer.stats["emociones_detectadas"]["tristeza"], 1)
    
    def test_stress_average(self):
        """Probar cálculo de promedio de estrés"""
        self.stats_observer.update("evaluacion_completada", {
            "emocion": "calma",
            "nivel_estres": 2
        })
        self.stats_observer.update("evaluacion_completada", {
            "emocion": "ansiedad",
            "nivel_estres": 8
        })
        
        # Promedio: (2 + 8) / 2 = 5
        self.assertEqual(self.stats_observer.stats["nivel_estres_promedio"], 5)
    
    def test_high_stress_alerts(self):
        """Probar conteo de alertas de estrés alto"""
        self.stats_observer.update("analisis_estres_alto", {
            "nivel_estres": 8
        })
        self.stats_observer.update("analisis_estres_alto", {
            "nivel_estres": 9
        })
        
        self.assertEqual(self.stats_observer.stats["alertas_estres_alto"], 2)


class TestAlertObserver(unittest.TestCase):
    """Tests para AlertObserver"""
    
    def setUp(self):
        self.alert_observer = AlertObserver()
    
    def test_no_alert_for_low_stress(self):
        """No debe generar alertas para estrés bajo"""
        # Capturar logs si es necesario
        self.alert_observer.update("analisis_estres_alto", {
            "nivel_estres": 5,
            "usuario": {"nombre": "Test"}
        })
        # No debería lanzar excepciones
    
    def test_moderate_alert(self):
        """Debe generar alerta moderada para estrés >= 7"""
        self.alert_observer.update("analisis_estres_alto", {
            "nivel_estres": 7,
            "usuario": {"nombre": "Test User"}
        })
        # Verificar que se llamó _alerta_moderada (revisar logs)
    
    def test_critical_alert(self):
        """Debe generar alerta crítica para estrés >= 9"""
        self.alert_observer.update("analisis_estres_alto", {
            "nivel_estres": 9,
            "usuario": {"nombre": "Critical User"}
        })
        # Verificar que se llamó _alerta_critica (revisar logs)


class TestIntegration(unittest.TestCase):
    """Tests de integración del sistema completo"""
    
    def test_full_user_registration_flow(self):
        """Probar flujo completo de registro de usuario"""
        manager = get_event_manager()
        test_observer = TestObserver()
        manager.attach(test_observer)
        
        # Simular registro de usuario
        usuario_data = {
            "id": 123,
            "nombre": "Juan Pérez",
            "correo": "juan@example.com",
            "fecha_creacion": datetime.now().isoformat()
        }
        
        manager.usuario_registrado(usuario_data)
        
        # Verificar que se recibió el evento
        events = test_observer.events_received
        self.assertGreater(len(events), 0)
        
        # Buscar evento de registro
        registro_event = next((e for e in events if e['event_type'] == 'usuario_registrado'), None)
        self.assertIsNotNone(registro_event)
        self.assertEqual(registro_event['data']['usuario']['nombre'], "Juan Pérez")
    
    def test_full_evaluation_flow_with_high_stress(self):
        """Probar flujo completo de evaluación con estrés alto"""
        manager = get_event_manager()
        test_observer = TestObserver()
        stats_observer = StatisticsObserver()
        
        manager.attach(test_observer)
        manager.attach(stats_observer)
        
        # Simular evaluación con estrés alto
        manager.evaluacion_completada(
            usuario_id=456,
            usuario_data={
                "id": 456,
                "nombre": "María González",
                "correo": "maria@example.com"
            },
            emocion="ansiedad",
            nivel_estres=8,
            recomendacion="Practica respiración profunda"
        )
        
        # Verificar eventos recibidos
        events = test_observer.events_received
        event_types = [e['event_type'] for e in events]
        
        self.assertIn('evaluacion_completada', event_types)
        self.assertIn('analisis_estres_alto', event_types)
        
        # Verificar estadísticas
        self.assertEqual(stats_observer.stats["total_analisis"], 1)
        self.assertEqual(stats_observer.stats["alertas_estres_alto"], 1)


if __name__ == '__main__':
    # Ejecutar tests
    unittest.main()
