import subprocess
import re  # Importar el módulo de expresiones regulares
import gi

gi.require_version("Gdk", "3.0")
from gi.repository import Gdk


def list_monitors():
    """Lista los monitores disponibles."""
    display = Gdk.Display.get_default()
    monitors = []
    for i in range(display.get_n_monitors()):
        monitor = display.get_monitor(i)
        geometry = monitor.get_geometry()
        monitors.append({"id": i, "width": geometry.width, "height": geometry.height})
    return monitors


def list_windows():
    """Obtiene una lista de ventanas activas usando xwininfo."""
    try:
        result = subprocess.run(
            ["xwininfo", "-root", "-tree"], stdout=subprocess.PIPE, text=True
        )
        windows = []
        for line in result.stdout.splitlines():
            match = re.search(
                r"0x([0-9a-fA-F]+) .*\"(.+)\"", line
            )  # Usar re para buscar ventanas
            if match:
                window_id = match.group(1)
                title = match.group(2)
                if title.strip():
                    windows.append({"id": window_id, "title": title})
        return windows
    except Exception as e:
        print(f"Error al obtener las ventanas: {e}")
        return []


def capture_monitor(monitor_id):
    """Captura la pantalla del monitor seleccionado."""
    display = Gdk.Display.get_default()
    monitor = display.get_monitor(monitor_id)
    geometry = monitor.get_geometry()
    root_window = Gdk.get_default_root_window()
    pb = Gdk.pixbuf_get_from_window(
        root_window, geometry.x, geometry.y, geometry.width, geometry.height
    )
    if pb:
        return pb
    else:
        raise RuntimeError(f"No se pudo capturar el monitor {monitor_id}.")


def capture_window(window_id):
    """Captura una ventana específica usando xwd."""
    try:
        result = subprocess.run(
            ["xwd", "-id", f"0x{window_id}", "-silent"], stdout=subprocess.PIPE
        )
        return result.stdout  # Devuelve los bytes de la captura
    except Exception as e:
        raise RuntimeError(f"Error al capturar ventana {window_id}: {e}")
