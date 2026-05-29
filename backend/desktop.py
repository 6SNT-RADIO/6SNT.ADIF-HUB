"""Desktop launcher for 6SNT.ADIF-HUB.

Runs the FastAPI server (which also serves the built SPA) on a local port and
shows the UI inside a native desktop window via pywebview (Edge WebView2 on
Windows). Falls back to the default browser if no webview backend is available.
This module is the PyInstaller entry point.
"""

from __future__ import annotations

import socket
import threading
import time

import uvicorn

from app.main import app

HOST = "127.0.0.1"
PREFERRED_PORT = 8765
WINDOW_TITLE = "6SNT.ADIF-HUB"


def _pick_port() -> int:
    """Use the preferred port, falling back to an ephemeral free one if taken."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        try:
            probe.bind((HOST, PREFERRED_PORT))
            return PREFERRED_PORT
        except OSError:
            pass
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind((HOST, 0))
        return probe.getsockname()[1]


def _serve(port: int) -> None:
    uvicorn.run(app, host=HOST, port=port, log_level="warning")


def _wait_until_up(port: int, timeout: float = 20.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.settimeout(0.5)
            if probe.connect_ex((HOST, port)) == 0:
                return True
        time.sleep(0.2)
    return False


def main() -> None:
    port = _pick_port()
    url = f"http://{HOST}:{port}"
    print(f"6SNT.ADIF-HUB iniciando en {url}")

    threading.Thread(target=_serve, args=(port,), daemon=True).start()
    if not _wait_until_up(port):
        print("ADVERTENCIA: el servidor no respondio a tiempo")

    try:
        import webview

        webview.create_window(
            WINDOW_TITLE,
            url,
            width=1320,
            height=880,
            min_size=(1024, 720),
            background_color="#05080c",
        )
        webview.start()
    except Exception as exc:  # noqa: BLE001 - fall back to the browser on any GUI failure
        import webbrowser

        print(f"Sin ventana nativa ({exc}); abriendo en el navegador.")
        webbrowser.open(url)
        # Keep the server alive while the browser tab is open.
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
