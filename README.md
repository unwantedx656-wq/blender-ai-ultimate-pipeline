# 🚀 Blender AI Ultimate Pipeline

**Pipeline Híbrido de Reconstrucción Neuronal 3D y Skill Maestra para Blender 5.x / 4.x**

Diseñado para empoderar a agentes de Inteligencia Artificial (Antigravity, Claude Code) y artistas técnicos con la capacidad de transformar imágenes y conceptos 2D en modelos 3D profesionales de alta fidelidad (99.99%), con riggs humanoides, los 12 principios de animación de Disney, sombreado PBR fotorrealista y cinemáticas de cámara.

---

## 🌟 Características Principales

1. **Reconstrucción 3D Neuronal Híbrida (Image-to-3D)**:
   - Integración con **Meshy-6 API** para remesh quad y mapas PBR listos para producción.
   - Soporte y fallback para modelos locales de código abierto (**Microsoft TRELLIS** / **TripoSR**) ubicados en discos de alta capacidad (`D:\AI_Tools\`).
2. **Skill Maestra Unificada (`blender-ultimate-artist`)**:
   - Una única fuente de verdad sin fragmentación que engloba anatomía, morfología, fisionomía, físicas de telas y pelo, y shaders Principled BSDF v2.
3. **Los 12 Principios de Animación de Disney Implementados en `bpy`**:
   - *Squash & Stretch* mediante deformadores Lattice con preservación de volumen.
   - *Anticipación* y *Overlapping Action* con desfase paramétrico de keyframes.
   - *Slow In / Slow Out* mediante suavizado de curvas Bézier en el Graph Editor.
   - *Staging* cinematográfico con lentes de retrato (50-85mm) y guías de composición.
4. **Cinemática de Cámaras y Showcase de Producto**:
   - *Turntable 360°*, *Slow Zoom*, *Crane Shot*, *Dolly Rotate* y *Perfect Loop*.
5. **Herramientas de Estudio y Shaders PolyHaven**:
   - Descarga e integración automática de HDRIs y materiales PBR de PolyHaven.
6. **Exportación Estándar para Motores de Juego**:
   - FBX validado para **Unreal Engine 5** (Z-Up, escala métrica).
   - GLB optimizado con compresión Draco para **Three.js** y la Web.

---

## 📁 Estructura del Repositorio

```text
blender-ai-ultimate-pipeline/
├── .agents/
│   └── skills/
│       └── blender-ultimate-artist/    # Skill Maestra para Antigravity / Claude
│           └── SKILL.md
├── core/
│   ├── image_to_3d_client.py           # Cliente híbrido de reconstrucción 3D
│   ├── camera_cinematics.py            # Generador de animaciones de cámara
│   ├── animation_engine.py             # Implementación de los 12 principios Disney
│   └── blender_mcp_bridge.py           # Enlace socket TCP 9876 con Blender
├── tools/                              # Herramientas de texturas y exportación
│   ├── polyhaven-studio-setup/
│   ├── polyhaven-texture-apply/
│   ├── product-polish/
│   └── threejs-export/
├── examples/                           # Scripts de prueba y recetas
├── docs/                               # Documentación técnica
├── requirements.txt                    # Dependencias ligeras de Python
└── README.md
```

---

## 🛠️ Instalación y Configuración Rápida

### 1. Requisitos Previos
- **Blender 4.2+ o 5.x LTS** instalado (ej. `D:\Blender\blender.exe`).
- Addon de Blender MCP activo escuchando en el puerto TCP `9876`.
- Python 3.10+ instalado.

### 2. Configurar Variables de Entorno (Opcional para Nube)
Para habilitar la generación neuronal en la nube:
```powershell
$env:MESHY_API_KEY = "tu_clave_de_meshy_aqui"
```

### 3. Conexión con Blender vía Socket
```python
from core.blender_mcp_bridge import BlenderBridge

bridge = BlenderBridge()
if bridge.check_connection():
    print("Conectado con éxito a Blender.")
```

### 4. Generar Animación Turntable 360°
```python
from core.camera_cinematics import generate_turntable_code
from core.blender_mcp_bridge import BlenderBridge

code = generate_turntable_code(target_name="MiModelo", frames=120)
bridge = BlenderBridge()
bridge.send_code(code)
```

---

## 📄 Licencia
Distribuido bajo la Licencia **MIT**. Consulta `LICENSE` para más información.
