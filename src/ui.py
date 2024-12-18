import flet as ft
from capture import list_monitors, list_windows, capture_monitor, capture_window
import base64
from PIL import Image
import io
import asyncio


def encode_image(data, width, height):
    """Encodes raw RGB image data to base64 PNG."""
    try:
        image = Image.frombytes("RGB", (width, height), data)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()
    except Exception as e:
        print(f"Error encoding image to base64: {e}")
        return None


def encode_image_from_data(data):
    """Encodes binary image data (e.g. from a window capture) to base64 PNG."""
    try:
        image = Image.open(io.BytesIO(data))
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()
    except Exception as e:
        print(f"Error encoding window data to base64: {e}")
        return None


def run_ui():
    """Runs the main UI of the application."""

    def main(page: ft.Page):
        page.title = "Screen Sharing App"
        page.window.width = 800
        page.window.height = 600
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # Obtener listas de monitores y ventanas
        try:
            monitor_list = list_monitors()
            window_list = list_windows()
        except Exception as e:
            print(f"Error fetching monitors or windows: {e}")
            monitor_list, window_list = [], []

        if not monitor_list:
            print("No monitors found!")
        if not window_list:
            print("No windows found!")

        monitor_options = [ft.dropdown.Option("Select Monitor")] + [
            ft.dropdown.Option(f"Monitor {m['id']}") for m in monitor_list
        ]

        window_options = [ft.dropdown.Option("Select Window")] + [
            ft.dropdown.Option(f"{w['title']} (ID: {w['id']})") for w in window_list
        ]

        monitor_dropdown = ft.Dropdown(
            label="Monitor", options=monitor_options, width=300
        )
        window_dropdown = ft.Dropdown(label="Window", options=window_options, width=300)

        # Inicializar el preview sin imagen
        preview_image = ft.Image(width=720, height=480)

        running_task = None  # Variable para almacenar la tarea de actualización

        async def start_preview(source_type, source_id):
            """Actualiza la vista previa periódicamente."""
            while True:
                try:
                    base64_image = None
                    if source_type == "monitor":
                        pb = capture_monitor(source_id)
                        width, height = pb.get_width(), pb.get_height()
                        data = pb.get_pixels()
                        base64_image = encode_image(data, width, height)
                    elif source_type == "window":
                        window_data = capture_window(source_id)
                        base64_image = encode_image_from_data(window_data)

                    if base64_image:
                        preview_image.src_base64 = base64_image
                    else:
                        print("Failed to encode image data to base64.")
                        preview_image.src_base64 = None
                    page.update()
                    await asyncio.sleep(0.010)  # Ajusta este valor para cambiar los FPS
                except Exception as e:
                    print(f"Error updating preview: {e}")
                    preview_image.src_base64 = None
                    page.update()
                    break

        def start_sharing(e):
            """Inicia la vista previa."""
            nonlocal running_task
            selected_monitor = monitor_dropdown.value
            selected_window = window_dropdown.value

            if running_task:
                running_task.cancel()  # Detener tarea previa si existe

            async def preview_wrapper():
                if selected_monitor and selected_monitor != "Select Monitor":
                    monitor_id = int(selected_monitor.split()[-1])
                    await start_preview("monitor", monitor_id)
                elif selected_window and selected_window != "Select Window":
                    window_id = int(selected_window.split("ID: ")[-1].rstrip(")"))
                    await start_preview("window", window_id)

            running_task = page.run_task(preview_wrapper)

        def stop_sharing(e):
            """Detiene la vista previa."""
            nonlocal running_task
            if running_task:
                running_task.cancel()
                running_task = None
            preview_image.src_base64 = None
            page.update()

        # Botones
        start_button = ft.ElevatedButton("Start Sharing", on_click=start_sharing)
        stop_button = ft.ElevatedButton("Stop Sharing", on_click=stop_sharing)

        # Layout
        page.add(
            ft.Column(
                [
                    ft.Row(
                        [monitor_dropdown, window_dropdown],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [start_button, stop_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(content=preview_image, alignment=ft.alignment.center),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

    ft.app(target=main)
