import imageio
import numpy as np
from capture import get_screen_bytes


def compress_frame():
    """Comprime una captura de pantalla en formato JPEG y la devuelve como bytes."""
    frame_bytes = get_screen_bytes()
    frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
    return imageio.imwrite("<bytes>", frame_array, format="jpeg", quality=75)
