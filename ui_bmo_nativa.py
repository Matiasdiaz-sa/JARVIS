import sys
import os
import math

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QRect, QPointF
from PyQt6.QtGui import QColor, QPainter, QBrush, QPen, QPainterPath

import motor_audio

class AudioWorker(QThread):
    update_signal = pyqtSignal(str, float, float)

    def run(self):
        def callback(estado, energia, conf):
            self.update_signal.emit(estado, energia, conf)
            
        print("[UI] Iniciando Hilo de Audio (BMO Nativo a Pantalla Completa)...")
        try:
            motor_audio.escuchar_continuo(callback_ui=callback)
        except Exception as e:
            print(f"[UI] Error en motor de audio: {e}")

class BmoNativeFace(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configuración a Pantalla Completa
        self.showFullScreen()
        
        # Fondo turquesa de BMO para todo el marco exterior
        self.setStyleSheet("background-color: #5abcb9;")
        
        # Variables de estado
        self.estado_actual = "esperando"
        self.time_counter = 0.0
        
        # Texto de estado
        self.status_label = QLabel("INICIANDO...", self)
        self.status_label.setStyleSheet("color: rgba(44, 68, 78, 200); font-size: 40px; font-weight: bold; font-family: 'Courier New', monospace;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Pantalla central (El cristal verde donde vive la cara)
        self.screen_frame = QFrame()
        self.screen_frame.setStyleSheet("""
            QFrame {
                background-color: #c9e2b1;
                border: 30px solid #2c444e;
                border-radius: 80px;
            }
        """)
        
        screen_layout = QVBoxLayout(self.screen_frame)
        
        # Widget personalizado (Canvas) donde pintaremos los ojos y la boca con aceleración gráfica
        self.face_canvas = FaceCanvas(self)
        screen_layout.addWidget(self.face_canvas, stretch=1)
        
        # Contenedor del texto
        text_layout = QHBoxLayout()
        text_layout.addWidget(self.status_label)
        screen_layout.addLayout(text_layout)
        
        # Agregar el monitor central al cuerpo principal, con márgenes simulando el chasis de BMO
        main_layout.addWidget(self.screen_frame, stretch=1)
        
        # Estos márgenes definen el grosor del plástico turquesa alrededor de la pantalla verde
        main_layout.setContentsMargins(150, 100, 150, 250)
        
        # --- Lógica Interna ---
        self.worker = AudioWorker()
        self.worker.update_signal.connect(self.on_audio_update)
        self.worker.start()
        
        # Timer de animación (60 FPS para que sea súper fluido)
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_animation)
        self.anim_timer.start(16)

    def keyPressEvent(self, event):
        # Salir con la tecla Esc
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def mouseDoubleClickEvent(self, event):
        # Salir con doble clic en cualquier parte de la pantalla
        self.close()

    def on_audio_update(self, estado, energia, conf):
        if self.estado_actual != estado:
            self.estado_actual = estado
            self.status_label.setText(estado.upper())
            
            # Cambios de color de la pantalla según la "emoción" o "estado"
            if estado == "grabando":
                # Pantalla rosa/roja al escuchar atentamente
                self.face_canvas.eye_color = QColor("#ff3333")
                self.screen_frame.setStyleSheet("QFrame { background-color: #ffd6d6; border: 30px solid #2c444e; border-radius: 80px; }")
            elif estado == "pensando":
                # Pantalla azul claro procesando
                self.face_canvas.eye_color = QColor("#0066cc")
                self.screen_frame.setStyleSheet("QFrame { background-color: #d6ebff; border: 30px solid #2c444e; border-radius: 80px; }")
            elif estado == "hibernando":
                # Pantalla grisácea oscura durmiendo
                self.face_canvas.eye_color = QColor("#1a1a1a")
                self.screen_frame.setStyleSheet("QFrame { background-color: #8da477; border: 30px solid #2c444e; border-radius: 80px; }")
            else:
                # BMO clásico verde
                self.face_canvas.eye_color = QColor("#1a1a1a")
                self.screen_frame.setStyleSheet("QFrame { background-color: #c9e2b1; border: 30px solid #2c444e; border-radius: 80px; }")

    def update_animation(self):
        self.time_counter += 0.1
        
        # Obtener medidas actuales de la pantalla verde
        w = self.face_canvas.width()
        h = self.face_canvas.height()
        
        center_x = w // 2
        center_y = h // 2
        
        # Geometría base de los rasgos
        eye_spacing = 300
        left_eye_x = center_x - eye_spacing // 2
        right_eye_x = center_x + eye_spacing // 2
        eye_y = center_y - 80
        
        mouth_x = center_x
        mouth_y = center_y + 120
        
        e_w = 60
        e_h = 100
        m_w = 200
        m_h = 60
        
        # Lógica matemática de las animaciones nativas
        if self.estado_actual == "esperando":
            # Parpadeo cíclico orgánico
            if (int(self.time_counter) % 40) < 2:
                e_h = 10  # Cierra el ojo
                eye_y += 45 # Lo baja ligeramente para centrar el cerrado
        elif self.estado_actual == "grabando":
            # Ojos emocionados dilatándose y contrayéndose (Pulsación)
            pulso = math.sin(self.time_counter * 3) * 15
            e_w += int(pulso)
            e_h += int(pulso)
            
            # Boca redonda de sorpresa/escucha
            m_w = 80
            m_h = 80
        elif self.estado_actual == "pensando":
            # Ojos de lado a lado analizando datos
            mirada = math.sin(self.time_counter * 2) * 50
            left_eye_x += int(mirada)
            right_eye_x += int(mirada)
            
            # Boca en línea recta de concentración
            m_w = 100
            m_h = 20
        elif self.estado_actual == "hablando":
            # Ojos achinados feliz
            e_h = 30
            eye_y += 35
            
            # Efecto de ecualizador en la boca
            onda = math.sin(self.time_counter * 7) * 40
            m_h += int(onda)
            if m_h < 15: m_h = 15
        elif self.estado_actual == "hibernando":
            # Ojos de línea apagados
            e_h = 10
            eye_y += 45
            
            # Boca plana pequeña
            m_w = 100
            m_h = 10

        # Enviar nuevas coordenadas calculadas al Canvas
        self.face_canvas.update_geometry(
            left_eye_x, eye_y, e_w, e_h,
            right_eye_x, eye_y, e_w, e_h,
            mouth_x, mouth_y, m_w, m_h,
            self.estado_actual
        )


class FaceCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Transparente para no estorbar clics en la pantalla principal
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        # Variables actuales calculadas
        self.lx = 0; self.ly = 0; self.lw = 0; self.lh = 0
        self.rx = 0; self.ry = 0; self.rw = 0; self.rh = 0
        self.mx = 0; self.my = 0; self.mw = 0; self.mh = 0
        self.estado = "esperando"
        self.eye_color = QColor("#1a1a1a")
        
        # Variables de pintado real (para Lerp / Transiciones elásticas)
        self.clx = 0; self.cly = 0; self.clw = 60; self.clh = 100
        self.crx = 0; self.cry = 0; self.crw = 60; self.crh = 100
        self.cmx = 0; self.cmy = 0; self.cmw = 200; self.cmh = 60

    def lerp(self, current, target, speed=0.35):
        # Linear Interpolation: Acorta la distancia entre el tamaño/posición actual y el destino
        # Esto genera ese efecto gomoso/suave tipo cubic-bezier
        return current + (target - current) * speed

    def update_geometry(self, lx, ly, lw, lh, rx, ry, rw, rh, mx, my, mw, mh, estado):
        self.lx = lx; self.ly = ly; self.lw = lw; self.lh = lh
        self.rx = rx; self.ry = ry; self.rw = rw; self.rh = rh
        self.mx = mx; self.my = my; self.mw = mw; self.mh = mh
        self.estado = estado
        
        # Inicialización en el primer frame
        if self.clx == 0:
            self.clx = lx; self.cly = ly
            self.crx = rx; self.cry = ry
            self.cmx = mx; self.cmy = my
            
        self.update() # Llama a paintEvent automáticamente

    def paintEvent(self, event):
        # 1. Aplicar la física elástica antes de pintar
        self.clx = self.lerp(self.clx, self.lx)
        self.cly = self.lerp(self.cly, self.ly)
        self.clw = self.lerp(self.clw, self.lw)
        self.clh = self.lerp(self.clh, self.lh)
        
        self.crx = self.lerp(self.crx, self.rx)
        self.cry = self.lerp(self.cry, self.ry)
        self.crw = self.lerp(self.crw, self.rw)
        self.crh = self.lerp(self.crh, self.rh)
        
        self.cmx = self.lerp(self.cmx, self.mx)
        self.cmy = self.lerp(self.cmy, self.my)
        self.cmw = self.lerp(self.cmw, self.mw)
        self.cmh = self.lerp(self.cmh, self.mh)

        # 2. Configurar el pintor de alto rendimiento
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # === DIBUJAR OJOS ===
        painter.setBrush(QBrush(self.eye_color))
        painter.setPen(Qt.GlobalColor.transparent)
        
        # Ojo Izquierdo
        painter.drawRoundedRect(
            int(self.clx - self.clw/2), int(self.cly - self.clh/2), 
            int(self.clw), int(self.clh), 
            int(self.clw/2), int(self.clw/2)
        )
        
        # Ojo Derecho
        painter.drawRoundedRect(
            int(self.crx - self.crw/2), int(self.cry - self.crh/2), 
            int(self.crw), int(self.crh), 
            int(self.crw/2), int(self.crw/2)
        )
        
        # === DIBUJAR BOCA ===
        # Siempre dibujamos la boca color negra
        mouth_color = QColor("#1a1a1a")
        
        if self.estado == "grabando":
            # Boca circular con borde (Oh!)
            painter.setBrush(Qt.GlobalColor.transparent)
            painter.setPen(QPen(mouth_color, 20, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawEllipse(
                int(self.cmx - self.cmw/2), int(self.cmy - self.cmh/2),
                int(self.cmw), int(self.cmh)
            )
        elif self.estado == "hablando":
            # Boca píldora rellena (cambia de altura rápidamente)
            painter.setBrush(QBrush(mouth_color))
            painter.setPen(Qt.GlobalColor.transparent)
            painter.drawRoundedRect(
                int(self.cmx - self.cmw/2), int(self.cmy - self.cmh/2),
                int(self.cmw), int(self.cmh),
                int(self.cmw/4), int(self.cmh/4)
            )
        elif self.estado in ["pensando", "hibernando"]:
            # Boca línea recta o concentrada
            painter.setBrush(QBrush(mouth_color))
            painter.setPen(Qt.GlobalColor.transparent)
            painter.drawRoundedRect(
                int(self.cmx - self.cmw/2), int(self.cmy - self.cmh/2),
                int(self.cmw), int(self.cmh),
                int(self.cmh/2), int(self.cmh/2)
            )
        else:
            # Estado normal: Sonrisa clásica de BMO
            rect = QRect(
                int(self.cmx - self.cmw/2), int(self.cmy - self.cmh*2),
                int(self.cmw), int(self.cmh*2.5)
            )
            # Arco: inicio 0 (derecha), longitud -180 (hasta la izquierda por abajo)
            painter.setPen(QPen(mouth_color, 25, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.setBrush(Qt.GlobalColor.transparent)
            painter.drawArc(rect, 0 * 16, -180 * 16)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BmoNativeFace()
    sys.exit(app.exec())
