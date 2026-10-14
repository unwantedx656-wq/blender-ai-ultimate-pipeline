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

## 🎛️ Panel de Control Visual: Blender AI Ultimate Studio

El repositorio incluye una interfaz web interactiva tipo dashboard para seleccionar visualmente el motor, configurar credenciales, auditar el hardware local y ejecutar el pipeline:

```bash
# Iniciar el servidor local de Studio
python studio/server.py 5050
```
Luego abre tu navegador en: **`http://localhost:5050`**

### Capacidades del Studio:
1. **Selector Visual de Motor**:
   - ☁️ **Meshy-6 API**: Remesh quad de alta fidelidad (10/10) con PBR completo (predeterminado).
   - 💻 **Microsoft TRELLIS**: Reconstrucción local en `D:\AI_Tools\trellis` (8.8/10), 100% gratuita y sin consumo de tokens.
2. **Configuración de Credenciales**:
   - Input interactivo para `MESHY_API_KEY` con validación y prueba en vivo contra los servidores de Meshy.
   - Guía paso a paso integrada para obtener la clave con 100 créditos gratis.
3. **Auditoría de Hardware Local**:
   - Monitoreo de CPU (AMD Ryzen 7 5700X), RAM (64 GB DDR4) y GPU (Intel Arc A750 8GB).
   - Verificación de integridad del submódulo `FlexiCubes` y estado del Disco D: (evitando saturar el Disco C:).
4. **Telemetría y Conexión Blender MCP**:
   - Comprobación en tiempo real del socket `localhost:9876` e ingesta directa de modelos a la escena.

---

## 🔑 Cómo Obtener tu API Key Gratuita de Meshy (100 Créditos)

1. Ingresa a [https://www.meshy.ai/](https://www.meshy.ai/) y presiona **"Get Started Free"**.
2. Regístrate con tu cuenta de Google, GitHub o correo electrónico. Al crear la cuenta gratuita recibirás **100 créditos de bienvenida**.
3. Ve a tu panel de usuario: **Settings &rarr; API Keys** (o directamente a [https://www.meshy.ai/settings/api-keys](https://www.meshy.ai/settings/api-keys)).
4. Haz clic en **"Create API Key"**, copia la clave generada (comienza con `msy_`).
5. Pégala en el panel de **Blender AI Ultimate Studio** (`http://localhost:5050`) y presiona **"Guardar y Probar"** o configúrala en `config/pipeline_config.json`.

---

## 💻 Adaptación Local de Microsoft TRELLIS (Disco D:)

Para garantizar el rendimiento óptimo del sistema y proteger los recursos de la máquina:
- **Directorio de Instalación**: `D:\AI_Tools\trellis` con el submódulo `flexicubes` clonado.
- **Protección de Almacenamiento**: Todos los checkpoints y pesos se dirigen a `D:\AI_Tools\models` o `D:\AI_Tools\cache`, conservando íntegro el espacio del Disco C:.
- **Aceleración Hardware**: Optimizado para aprovechar la memoria de 64 GB RAM y los 16 hilos del Ryzen 7 5700X, junto con la GPU Intel Arc A750 de 8 GB VRAM.

---

## 📁 Estructura del Repositorio

```text
blender-ai-ultimate-pipeline/
├── .agents/
│   └── skills/
│       └── blender-ultimate-artist/    # Skill Maestra unificada para Antigravity / Claude
│           └── SKILL.md
├── config/
│   └── pipeline_config.json            # Configuración de motores, API keys y puertos
├── core/
│   ├── hybrid_3d_engine.py             # Orquestador híbrido Meshy API + TRELLIS
│   ├── image_to_3d_client.py           # Cliente Image-to-3D
│   ├── camera_cinematics.py            # Generador de animaciones y cámaras 360°
│   ├── animation_engine.py             # Los 12 principios de animación de Disney
│   └── blender_mcp_bridge.py           # Enlace socket TCP 9876 con Blender
├── studio/                             # Interfaz Web Visual (Dashboard Glassmorphism)
│   ├── server.py                       # Servidor HTTP local en puerto 5050
│   └── static/                         # Frontend Vanilla HTML5/CSS3/JS
│       ├── index.html
│       ├── style.css
│       ├── app.js
│       └── referencia.jpg
├── tools/                              # Herramientas de texturas y exportación
│   ├── polyhaven-studio-setup/
│   ├── polyhaven-texture-apply/
│   ├── product-polish/
│   └── threejs-export/
├── examples/                           # Scripts de prueba y recetas
├── docs/                               # Documentación técnica
├── requirements.txt                    # Dependencias de Python
└── README.md
```

---

## 🛠️ Instalación y Configuración Rápida

### 1. Iniciar el Studio Web
```powershell
python studio/server.py 5050
```

### 2. Uso Programático del Orquestador Híbrido
```python
from core.hybrid_3d_engine import Hybrid3DEngine

engine = Hybrid3DEngine()

# Seleccionar motor: "meshy" o "trellis_local"
engine.set_engine("meshy")

# Configurar API Key
engine.set_meshy_api_key("msy_tu_clave_aqui")

# Verificar estado de todo el sistema
status = engine.get_full_status()
print(status)
```

---

## 📄 Licencia
Distribuido bajo la Licencia **MIT**. Consulta `LICENSE` para más información.
