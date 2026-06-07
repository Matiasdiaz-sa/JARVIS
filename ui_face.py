import sys
import os
import time
import math
import random

# Redireccionar logs
sys.stdout = open(os.path.join(os.path.dirname(__file__), "jarvis_face.log"), "w", encoding="utf-8", buffering=1)
sys.stderr = open(os.path.join(os.path.dirname(__file__), "jarvis_face_error.log"), "w", encoding="utf-8", buffering=1)

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QPointF, QRectF
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QRadialGradient, QLinearGradient, QPainterPath

import motor_audio

class AudioWorker(QThread):
    update_signal = pyqtSignal(str, float, float)

    def run(self):
        def callback(estado, energia, conf):
            self.update_signal.emit(estado, energia, conf)
            
        print("[UI_FACE] Iniciando Hilo de Audio...")
        try:
            motor_audio.escuchar_continuo(callback_ui=callback)
        except Exception as e:
            print(f"[UI_FACE] Error en motor de audio: {e}")

class JarvisFaceWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configuración para Pantalla Completa y "Kiosk Mode"
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.showFullScreen()
        
        # Ocultar el cursor del mouse
        self.setCursor(Qt.CursorShape.BlankCursor)
        
        # Variables de estado
        self.estado_actual = "esperando"
        self.energia_actual = 0.0
        
        # Colores (Celeste Phantom)
        self.color_base_ojos = QColor(0, 200, 255)    # Celeste brillante / Phantom
        self.color_resplandor_esperando = QColor(0, 0, 0)
        self.color_resplandor_hablando = QColor(0, 0, 0) 
        self.color_resplandor_escuchando = QColor(0, 0, 0)
        self.color_resplandor_pensando = QColor(0, 0, 0)
        
        self.current_glow_color = QColor(0, 0, 0)
        
        # Animación
        self.time_counter = 0.0
        self.eye_openness = 1.0 # 1.0 = Abierto, 0.0 = Cerrado
        self.target_eye_openness = 1.0
        self.eye_width_scale = 1.0
        self.target_eye_width_scale = 1.0
        
        # Parpadeo
        self.next_blink = time.time() + random.uniform(2.0, 5.0)
        self.is_blinking = False
        
        # Timers
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_animation)
        self.anim_timer.start(16) # ~60fps
        
        # Hilo de Audio
        self.worker = AudioWorker()
        self.worker.update_signal.connect(self.on_audio_update)
        self.worker.start()

    def on_audio_update(self, estado, energia, conf):
        self.estado_actual = estado
        self.energia_actual = energia

    def keyPressEvent(self, event):
        # Salir con ESC por seguridad mientras pruebas
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def update_animation(self):
        self.time_counter += 0.05
        
        target_color = self.color_resplandor_esperando
        self.target_eye_openness = 1.0
        self.target_eye_width_scale = 1.0
        
        # Lógica de Parpadeo Autónomo
        current_time = time.time()
        if not self.is_blinking and current_time > self.next_blink and self.estado_actual in ["esperando", "hablando"]:
            self.is_blinking = True
            self.blink_start = current_time
            self.next_blink = current_time + random.uniform(2.0, 6.0)
            
        if self.is_blinking:
            # Duración del parpadeo: 0.15s bajar, 0.15s subir
            elapsed = current_time - self.blink_start
            if elapsed < 0.1:
                self.target_eye_openness = 0.05 # Cerrando
            elif elapsed < 0.2:
                self.target_eye_openness = 1.0  # Abriendo
            else:
                self.is_blinking = False
                
        # Reacciones de los ojos al estado
        if self.estado_actual == "escuchando":
            target_color = self.color_resplandor_escuchando
            # Abre más los ojos al escuchar
            if not self.is_blinking:
                self.target_eye_openness = 1.15
                self.target_eye_width_scale = 1.05
                
        elif self.estado_actual == "pensando":
            target_color = self.color_resplandor_pensando
            # Achina los ojos al pensar
            if not self.is_blinking:
                self.target_eye_openness = 0.4 + math.sin(self.time_counter * 3) * 0.1
                self.target_eye_width_scale = 0.9
                
        elif self.estado_actual == "hablando":
            target_color = self.color_resplandor_hablando
            # Pulso con la voz
            vol = min(1.0, self.energia_actual / 80.0)
            if not self.is_blinking:
                self.target_eye_openness = 0.8 + (vol * 0.5)
                
        elif self.estado_actual == "hibernando":
            target_color = QColor(20, 20, 20)
            if not self.is_blinking:
                self.target_eye_openness = 0.1
                
        # Interpolar Apertura de Ojos (Suavizado)
        self.eye_openness += (self.target_eye_openness - self.eye_openness) * 0.2
        self.eye_width_scale += (self.target_eye_width_scale - self.eye_width_scale) * 0.1
        
        # Interpolación de Colores (Desactivada para el modo blanco y negro)
        # self.current_glow_color.setRgb(int(r), int(g), int(b), int(a))
        
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) # Activado para círculos perfectos
        
        w = self.width()
        h = self.height()
        center_x = w / 2
        center_y = h / 2
        
        # 1. Fondo Mate (Mismo celeste Phantom pero muy oscuro / ghost)
        painter.fillRect(0, 0, int(w), int(h), QColor(8, 15, 25))

        # 2. Configuración de los Ojos
        eye_base_w = 200
        eye_base_h = 200
        eye_spacing = 150 # Espacio entre ojos
        
        # Distancia del centro para cada ojo
        offset_x = (eye_base_w / 2) + (eye_spacing / 2)
        
        # Ojo Izquierdo y Derecho
        self.draw_eye(painter, center_x - offset_x, center_y)
        self.draw_eye(painter, center_x + offset_x, center_y)
        
        # 3. Efecto Retro 1-Bit (Líneas de pantalla sutiles de monitor viejo)
        painter.setPen(QPen(QColor(0, 0, 0, 30), 1))
        for y_line in range(0, int(h), 4):
            painter.drawLine(0, y_line, int(w), y_line)

    def draw_eye(self, painter, x, y):
        # Ojos circulares, el alto cambia al parpadear
        w = 180 * self.eye_width_scale
        h = 180 * max(0.01, self.eye_openness)
        
        # Simular movimiento flotante suave
        float_y = math.sin(self.time_counter * 1.5) * 10
        y += float_y
        
        # Ojo Físico (Círculo Celeste Phantom Mate)
        painter.setBrush(QBrush(self.color_base_ojos))
        painter.setPen(Qt.GlobalColor.transparent)
        
        # Dibujar como elipse (círculo perfecto cuando está abierto)
        painter.drawEllipse(QPointF(x, y), w/2, h/2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Iniciar gestor de widgets si existe
    try:
        import ui_widgets
        widget_manager = ui_widgets.WidgetManager()
    except Exception as e:
        print(f"Error al cargar ui_widgets: {e}")
        
    widget = JarvisFaceWidget()
    sys.exit(app.exec())
