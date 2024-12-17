from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QPushButton,
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QImage
from capture import list_monitors, list_windows, capture_monitor, capture_window
import io


class ScreenPreviewWindow(QMainWindow):
    """Ventana de preview que actualiza la captura en tiempo real."""

    def __init__(self, selection):
        super().__init__()
        self.setWindowTitle("Preview de la Transmisión")
        self.setGeometry(100, 100, 1280, 720)  # Tamaño base para 720p
        self.selection = selection

        # QLabel para mostrar la captura
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.image_label)

        # Configurar un timer para actualizar la captura
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_preview)
        self.timer.start(100)  # Actualización cada 100 ms

    def update_preview(self):
        """Actualiza la captura de la fuente seleccionada."""
        try:
            if self.selection["type"] == "monitor":
                pb = capture_monitor(self.selection["id"])
                width, height = pb.get_width(), pb.get_height()
                data = pb.get_pixels()
                qimage = QImage(data, width, height, QImage.Format_RGB888)
            elif self.selection["type"] == "window":
                window_data = capture_window(self.selection["id"])
                qimage = QImage.fromData(window_data, "xwd")

            # Redimensionar la imagen a 720p (1280x720)
            qimage = qimage.scaled(
                1280, 720, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

            # Convertir a QPixmap y mostrar en QLabel
            pixmap = QPixmap.fromImage(qimage)
            self.image_label.setPixmap(
                pixmap.scaled(
                    self.image_label.width(),
                    self.image_label.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )
        except Exception as e:
            print(f"Error al actualizar el preview: {e}")


class SelectionDialog(QDialog):
    """Diálogo para seleccionar monitor o ventana."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select source")
        self.selection = None
        layout = QVBoxLayout()

        # Dropdowns para monitores y ventanas
        self.monitor_combo = QComboBox()
        self.monitor_combo.addItem("Slect Monitor")
        for monitor in list_monitors():
            self.monitor_combo.addItem(f"Monitor {monitor['id']}", monitor["id"])

        self.window_combo = QComboBox()
        self.window_combo.addItem("Select Window")
        for window in list_windows():
            self.window_combo.addItem(
                f"{window['title']} (ID: {window['id']})", window["id"]
            )

        layout.addWidget(QLabel("Select a Monitor or a Window"))
        layout.addWidget(self.monitor_combo)
        layout.addWidget(self.window_combo)

        # Botones de acción
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_selection(self):
        """Devuelve la selección del usuario."""
        if self.monitor_combo.currentIndex() > 0:
            return {"type": "monitor", "id": self.monitor_combo.currentData()}
        elif self.window_combo.currentIndex() > 0:
            return {"type": "window", "id": self.window_combo.currentData()}
        return None


class ScreenSharingApp(QWidget):
    """Ventana principal."""

    def __init__(self):
        super().__init__()
        self.preview_window = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Screen Sharing App")
        layout = QVBoxLayout()

        self.start_button = QPushButton("Start Sharing Screen")
        self.start_button.clicked.connect(self.start_sharing)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Sharing Screen")
        self.stop_button.clicked.connect(self.stop_sharing)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def start_sharing(self):
        """Inicia la compartición mostrando una ventana de selección."""
        dialog = SelectionDialog()
        if dialog.exec_():
            selection = dialog.get_selection()
            if selection:
                self.preview_window = ScreenPreviewWindow(selection)
                self.preview_window.show()

    def stop_sharing(self):
        """Detiene la compartición cerrando la ventana de preview."""
        if self.preview_window:
            self.preview_window.close()
            self.preview_window = None
