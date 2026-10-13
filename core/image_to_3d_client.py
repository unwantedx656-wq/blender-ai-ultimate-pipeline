"""
Image-to-3D Hybrid Client
Connects 2D reference images to 3D meshes using Meshy API and local reconstructors.
Automates downloading, quad-remeshing, and importing into Blender via MCP.
"""

import os
import time
import base64
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List

class ImageTo3DClient:
    def __init__(self, api_key: Optional[str] = None, output_dir: str = "D:\\AI_Tools\\models"):
        self.api_key = api_key or os.environ.get("MESHY_API_KEY", "")
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise ValueError("MESHY_API_KEY no configurada. Configure la variable de entorno o pásela al constructor.")
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def file_to_data_uri(self, file_path: str) -> str:
        """Convierte una imagen local a Data URI Base64."""
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(file_path)[1].lower().replace(".", "")
        mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"
        return f"data:{mime};base64,{encoded}"

    def create_image_to_3d_task(
        self,
        image_input: str,
        ai_model: str = "meshy-6",
        topology: str = "quad",
        target_polycount: int = 35000,
        enable_pbr: bool = True
    ) -> str:
        """Inicia una tarea de reconstrucción 3D a partir de una imagen."""
        image_url = image_input
        if os.path.exists(image_input):
            image_url = self.file_to_data_uri(image_input)

        url = "https://api.meshy.ai/openapi/v1/image-to-3d"
        payload = {
            "image_url": image_url,
            "ai_model": ai_model,
            "enable_pbr": enable_pbr,
            "should_remesh": True,
            "should_texture": True,
            "topology": topology,
            "target_polycount": target_polycount,
            "target_formats": ["glb", "fbx"]
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=self._get_headers(),
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("result", "")

    def poll_task(self, task_id: str, interval: int = 10, max_wait: int = 600) -> Dict[str, Any]:
        """Monitorea el progreso de la reconstrucción hasta completarse."""
        url = f"https://api.meshy.ai/openapi/v1/image-to-3d/{task_id}"
        start_time = time.time()

        while time.time() - start_time < max_wait:
            req = urllib.request.Request(url, headers=self._get_headers(), method="GET")
            try:
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    status = data.get("status")
                    progress = data.get("progress", 0)
                    print(f"[{time.strftime('%X')}] Tarea {task_id}: {status} ({progress}%)")
                    
                    if status == "SUCCEEDED":
                        return data
                    elif status in ["FAILED", "EXPIRED"]:
                        raise RuntimeError(f"La tarea falló con estado: {status} - {data.get('task_error')}")
            except urllib.error.HTTPError as e:
                print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
            
            time.sleep(interval)
        raise TimeoutError(f"Tiempo de espera agotado ({max_wait}s) para la tarea {task_id}.")

    def download_asset(self, model_urls: Dict[str, str], filename_prefix: str = "generated_mesh") -> str:
        """Descarga el archivo .glb generado en el directorio configurado en D:"""
        glb_url = model_urls.get("glb")
        if not glb_url:
            raise ValueError("No se encontró URL para formato GLB en la respuesta.")
        
        output_path = os.path.join(self.output_dir, f"{filename_prefix}.glb")
        urllib.request.urlretrieve(glb_url, output_path)
        print(f"Asset 3D guardado exitosamente en: {output_path}")
        return output_path
