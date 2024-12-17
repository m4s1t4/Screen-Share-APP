import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaStreamTrack
from av import VideoFrame
from capture import get_screen_bytes


class ScreenShareTrack(MediaStreamTrack):
    """Track personalizado para compartir la pantalla como flujo de video."""

    kind = "video"

    async def recv(self):
        """Envía una captura de pantalla como frame de video."""
        frame = get_screen_bytes()
        video_frame = VideoFrame.from_ndarray(frame)
        return video_frame


async def start_transmission():
    pc = RTCPeerConnection()
    screen_track = ScreenShareTrack()
    pc.addTrack(screen_track)

    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    print("SDP Local:", pc.localDescription.sdp)

    await asyncio.Future()  # Mantén la conexión activa
