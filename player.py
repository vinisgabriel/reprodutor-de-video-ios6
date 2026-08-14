import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QFileDialog, 
                             QHBoxLayout, QVBoxLayout, QPushButton, 
                             QSlider, QLabel, QFrame, QGraphicsView, 
                             QGraphicsScene)
from PyQt6.QtCore import Qt, QUrl, QTime, QRectF, QTimer, QEvent
from PyQt6.QtGui import QPainter, QColor, QPolygonF, QPen, QBrush
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem

class WindowControlButton(QPushButton):
    def __init__(self, color_type="close", parent=None):
        super().__init__(parent)
        self.color_type = color_type
        self.setFixedSize(14, 14)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("background: transparent; border: none;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.color_type == "close":
            bg_top = QColor(255, 95, 86)
            border_col = QColor(180, 30, 25)
        elif self.color_type == "minimize":
            bg_top = QColor(39, 201, 63)
            border_col = QColor(15, 120, 30)
        else:
            bg_top = QColor(255, 189, 46)
            border_col = QColor(180, 120, 10)

        painter.setPen(QPen(border_col, 1))
        painter.setBrush(QBrush(bg_top))
        painter.drawEllipse(1, 1, 12, 12)

class IOS6Button(QPushButton):
    def __init__(self, mode="play", parent=None):
        super().__init__(parent)
        self.mode = mode
        self.setFixedSize(50, 42)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("background: transparent; border: none;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = QColor(255, 255, 255) if not self.isDown() else QColor(66, 111, 204)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)

        w, h = self.width(), self.height()

        if self.mode == "play":
            poly = QPolygonF([
                QRectF(w*0.3, h*0.15, w*0.45, h*0.7).topLeft(),
                QRectF(w*0.3, h*0.15, w*0.45, h*0.7).bottomLeft(),
                QRectF(w*0.3, h*0.15, w*0.45, h*0.7).topRight() + QRectF(0, h*0.35, 0, 0).topLeft()
            ])
            painter.drawPolygon(poly)

        elif self.mode == "pause":
            bar_w = 6
            gap = 6
            start_x = (w - (bar_w * 2 + gap)) / 2
            painter.drawRect(int(start_x), int(h*0.18), bar_w, int(h*0.64))
            painter.drawRect(int(start_x + bar_w + gap), int(h*0.18), bar_w, int(h*0.64))

        elif self.mode == "rw":
            painter.drawRect(int(w*0.15), int(h*0.22), 4, int(h*0.56))
            t1 = QPolygonF([
                QRectF(w*0.22, h*0.22, w*0.3, h*0.56).topRight(),
                QRectF(w*0.22, h*0.22, w*0.3, h*0.56).bottomRight(),
                QRectF(w*0.22, h*0.22, w*0.3, h*0.56).topLeft() + QRectF(0, h*0.28, 0, 0).topLeft()
            ])
            t2 = QPolygonF([
                QRectF(w*0.52, h*0.22, w*0.3, h*0.56).topRight(),
                QRectF(w*0.52, h*0.22, w*0.3, h*0.56).bottomRight(),
                QRectF(w*0.52, h*0.22, w*0.3, h*0.56).topLeft() + QRectF(0, h*0.28, 0, 0).topLeft()
            ])
            painter.drawPolygon(t1)
            painter.drawPolygon(t2)

        elif self.mode == "ff":
            t1 = QPolygonF([
                QRectF(w*0.18, h*0.22, w*0.3, h*0.56).topLeft(),
                QRectF(w*0.18, h*0.22, w*0.3, h*0.56).bottomLeft(),
                QRectF(w*0.18, h*0.22, w*0.3, h*0.56).topRight() + QRectF(0, h*0.28, 0, 0).topLeft()
            ])
            t2 = QPolygonF([
                QRectF(w*0.48, h*0.22, w*0.3, h*0.56).topLeft(),
                QRectF(w*0.48, h*0.22, w*0.3, h*0.56).bottomLeft(),
                QRectF(w*0.48, h*0.22, w*0.3, h*0.56).topRight() + QRectF(0, h*0.28, 0, 0).topLeft()
            ])
            painter.drawRect(int(w*0.81), int(h*0.22), 4, int(h*0.56))
            painter.drawPolygon(t1)
            painter.drawPolygon(t2)

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.parent_win = parent
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def mouseDoubleClickEvent(self, event):
        self.parent_win.toggle_maximize()
        super().mouseDoubleClickEvent(event)

class IOS6MediaPlayer(QWidget):
    def __init__(self, video_path=None):
        super().__init__()
        self.setWindowTitle("iOS 6 Video Player")
        self.resize(850, 520)
        self.setStyleSheet("background-color: #000000;")
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMouseTracking(True)
        self._drag_pos = None

        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        # Timer para ocultar controles (3 segundos)
        self.hide_timer = QTimer(self)
        self.hide_timer.setInterval(3000)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide_controls)

        self.init_ui()

        if video_path and os.path.exists(video_path):
            self.load_video(video_path)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Barra de título superior
        self.title_bar = QFrame()
        self.title_bar.setFixedHeight(32)
        self.title_bar.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-bottom: 1px solid #2d2d2d;
            }
        """)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(12, 0, 12, 0)
        title_layout.setSpacing(10)

        self.lbl_title = QLabel("iOS 6 Video Player")
        self.lbl_title.setStyleSheet("color: #a0a0a0; font-size: 12px; font-family: 'Segoe UI', sans-serif;")

        window_controls_layout = QHBoxLayout()
        window_controls_layout.setSpacing(8)

        self.btn_green = WindowControlButton("minimize")
        self.btn_yellow = WindowControlButton("maximize")
        self.btn_red = WindowControlButton("close")

        self.btn_green.clicked.connect(self.showMinimized)
        self.btn_yellow.clicked.connect(self.toggle_maximize)
        self.btn_red.clicked.connect(self.close)

        window_controls_layout.addWidget(self.btn_green)
        window_controls_layout.addWidget(self.btn_yellow)
        window_controls_layout.addWidget(self.btn_red)

        title_layout.addWidget(self.lbl_title)
        title_layout.addStretch()
        title_layout.addLayout(window_controls_layout)

        self.title_bar.mousePressEvent = self.title_bar_mouse_press
        self.title_bar.mouseMoveEvent = self.title_bar_mouse_move

        # Barra de progresso iOS 6
        self.top_bar = QFrame()
        self.top_bar.setFixedHeight(52)
        self.top_bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #2c3545, stop:0.48 #18202d, stop:0.49 #0a0f18, stop:1 #111722);
                border-bottom: 1px solid #000000;
            }
        """)
        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(12, 6, 12, 6)
        top_layout.setSpacing(8)

        self.btn_done = QPushButton("Done")
        self.btn_done.setFixedSize(64, 32)
        self.btn_done.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_done.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #6f9bf7, stop:0.48 #426FCC, stop:0.49 #2453b3, stop:1 #3567d6);
                border: 1px solid #163675;
                border-radius: 6px;
                color: #ffffff;
                font-weight: bold;
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #84adff, stop:0.48 #5381e0, stop:0.49 #3162c7, stop:1 #4778ea);
            }
            QPushButton:pressed {
                background: #193f8a;
            }
        """)
        self.btn_done.clicked.connect(self.close)

        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        self.timeline_slider.setRange(0, 0)
        self.timeline_slider.setFixedHeight(28)
        self.timeline_slider.setStyleSheet(self.get_ios_slider_style())
        self.timeline_slider.sliderMoved.connect(self.set_position)

        self.lbl_time = QLabel("-00:00")
        self.lbl_time.setStyleSheet("color: #7b8b9e; font-weight: bold; font-size: 14px; font-family: Arial; margin-left: 4px; margin-right: 8px;")

        top_layout.addWidget(self.btn_done)
        top_layout.addWidget(self.timeline_slider, stretch=1)
        top_layout.addWidget(self.lbl_time)

        # Área do Vídeo
        self.scene = QGraphicsScene(self)
        self.view = CustomGraphicsView(self.scene, self)
        self.view.setStyleSheet("background: black; border: none;")
        self.view.setMouseTracking(True)
        self.view.viewport().setMouseTracking(True)

        self.video_item = QGraphicsVideoItem()
        self.scene.addItem(self.video_item)
        self.media_player.setVideoOutput(self.video_item)

        # Painel Flutuante
        self.floating_panel = QFrame()
        self.floating_panel.setFixedSize(380, 105)
        self.floating_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(80, 95, 115, 0.45),
                            stop:0.48 rgba(35, 45, 60, 0.50),
                            stop:0.49 rgba(15, 20, 30, 0.55),
                            stop:1 rgba(25, 32, 45, 0.55));
                border: 1.5px solid rgba(255, 255, 255, 0.40);
                border-radius: 12px;
            }
        """)

        panel_layout = QVBoxLayout(self.floating_panel)
        panel_layout.setContentsMargins(22, 10, 22, 12)
        panel_layout.setSpacing(4)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(36)
        
        self.btn_rw = IOS6Button(mode="rw")
        self.btn_play = IOS6Button(mode="pause")
        self.btn_ff = IOS6Button(mode="ff")

        self.btn_play.clicked.connect(self.toggle_play)
        self.btn_rw.clicked.connect(self.rewind)
        self.btn_ff.clicked.connect(self.fast_forward)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_rw)
        btn_layout.addWidget(self.btn_play)
        btn_layout.addWidget(self.btn_ff)
        btn_layout.addStretch()

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedHeight(28)
        self.audio_output.setVolume(0.7)
        self.volume_slider.setStyleSheet(self.get_ios_slider_style())
        self.volume_slider.valueChanged.connect(self.set_volume)

        panel_layout.addLayout(btn_layout)
        panel_layout.addWidget(self.volume_slider)

        self.panel_proxy = self.scene.addWidget(self.floating_panel)
        self.panel_proxy.setZValue(10)

        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.top_bar)
        main_layout.addWidget(self.view, stretch=1)

        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

        # Event Filters para detectar movimentação do mouse
        self.installEventFilter(self)
        self.view.viewport().installEventFilter(self)

        self.hide_timer.start()

    def eventFilter(self, watched, event):
        if event.type() in (QEvent.Type.MouseMove, QEvent.Type.MouseButtonPress, QEvent.Type.HoverMove):
            self.show_controls()
        return super().eventFilter(watched, event)

    def show_controls(self):
        if not self.top_bar.isVisible():
            self.top_bar.show()
        if not self.panel_proxy.isVisible():
            self.panel_proxy.show()
        self.hide_timer.start()

    def hide_controls(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.top_bar.hide()
            self.panel_proxy.hide()

    def title_bar_mouse_press(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def title_bar_mouse_move(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        vw_w = self.view.width()
        vw_h = self.view.height()

        self.scene.setSceneRect(0, 0, vw_w, vw_h)
        self.video_item.setSize(self.scene.sceneRect().size())

        fp_w = self.floating_panel.width()
        fp_h = self.floating_panel.height()

        x = (vw_w - fp_w) / 2
        y = vw_h - fp_h - 22
        self.panel_proxy.setPos(x, y)

    def load_video(self, path):
        self.media_player.setSource(QUrl.fromLocalFile(path))
        self.media_player.play()
        self.btn_play.mode = "pause"
        self.btn_play.update()

    def toggle_play(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
            self.btn_play.mode = "play"
            self.show_controls()
            self.hide_timer.stop()
        else:
            self.media_player.play()
            self.btn_play.mode = "pause"
            self.hide_timer.start()
        self.btn_play.update()

    def rewind(self):
        self.media_player.setPosition(max(0, self.media_player.position() - 10000))
        self.show_controls()

    def fast_forward(self):
        self.media_player.setPosition(min(self.media_player.duration(), self.media_player.position() + 10000))
        self.show_controls()

    def set_position(self, position):
        self.media_player.setPosition(position)
        self.show_controls()

    def set_volume(self, value):
        self.audio_output.setVolume(value / 100.0)
        self.show_controls()

    def position_changed(self, position):
        self.timeline_slider.setValue(position)
        remaining = self.media_player.duration() - position
        if remaining < 0:
            remaining = 0
        t = QTime(0, 0, 0).addMSecs(remaining)
        self.lbl_time.setText(f"-{t.toString('mm:ss')}")

    def duration_changed(self, duration):
        self.timeline_slider.setRange(0, duration)

    def get_ios_slider_style(self):
        return """
            QSlider {
                background: transparent;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #e0e0e0;
                border-radius: 4px;
                border: 1px solid #777777;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                            stop:0 #6f9bf7, stop:0.48 #426FCC, stop:0.49 #2453b3, stop:1 #3567d6);
                border-radius: 4px;
                border: 1px solid #163675;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                            stop:0 #ffffff, stop:0.5 #e0e0e0, stop:0.51 #b5b5b5, stop:1 #cccccc);
                border: 1px solid #222222;
                width: 22px;
                height: 22px;
                margin-top: -8px;
                margin-bottom: -8px;
                border-radius: 12px;
            }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_path = sys.argv[1] if len(sys.argv) > 1 else None
    player = IOS6MediaPlayer(video_path)
    player.show()
    sys.exit(app.exec())