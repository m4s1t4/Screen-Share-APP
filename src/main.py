from PyQt5.QtWidgets import QApplication
from ui import ScreenSharingApp


def main():
    app = QApplication([])  # Crear la aplicación PyQt
    window = ScreenSharingApp()  # Instanciar la ventana principal
    window.show()
    app.exec_()  # Iniciar el bucle de eventos


if __name__ == "__main__":
    main()
