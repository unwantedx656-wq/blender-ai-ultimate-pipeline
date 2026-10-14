"""
Blender MCP Low-Level Socket Bridge
Communicates directly with the mcp-for-blender addon running inside Blender on localhost:9876.
"""

import socket
import json
from typing import Dict, Any, Optional

class BlenderBridge:
    def __init__(self, host: str = "localhost", port: int = 9876, timeout: float = 30.0):
        self.host = host
        self.port = port
        self.timeout = timeout

    def send_code(self, code: str) -> Dict[str, Any]:
        """Envía un fragmento de código Python a Blender para su ejecución inmediata."""
        payload = {
            "type": "execute_code",
            "params": {
                "code": code
            }
        }
        data_str = json.dumps(payload) + "\n"
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.timeout)
            s.connect((self.host, self.port))
            s.sendall(data_str.encode("utf-8"))
            
            response = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
                try:
                    data = json.loads(response.decode("utf-8"))
                    return data
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
        
        return json.loads(response.decode("utf-8")) if response else {}

    def check_connection(self) -> bool:
        """Verifica si el servidor de Blender está escuchando en el puerto configurado."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0)
                s.connect((self.host, self.port))
                return True
        except (socket.error, ConnectionRefusedError):
            return False
