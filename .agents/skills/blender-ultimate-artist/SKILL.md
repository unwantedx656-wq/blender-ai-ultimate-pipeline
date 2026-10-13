---
name: blender-ultimate-artist
description: Compendio definitivo y pipeline híbrido de Blender 3D para artistas profesionales. Integra reconstrucción neuronal Image-to-3D (Meshy/TRELLIS), anatomía y morfología orgánica de alta precisión, los 12 principios de animación de Disney implementados en Graph Editor/Lattices, físicas y telas, sombreado PBR Principled BSDF v2, iluminación cinematográfica y exportación para Unreal Engine y Web.
license: MIT
metadata:
  author: unwantedx656-wq & Antigravity AI
  version: "3.0.0"
  domain: blender-3d-mastery
  role: lead-technical-artist
  triggers: blender, 3d, bpy, render, cycles, eevee, modelado, shader, material, iluminación, cámara, textura, geom, mesh, fbx, gltf, glb, animacion, anatomia, disney, image-to-3d, meshy, rigging
---

# 🎨 Blender Ultimate Artist: Manual Técnico y Pipeline Definitivo

Guía y especificación maestra para operar como un **Lead Technical Artist & 3D Generalist AAA** en Blender 5.x/4.x mediante el protocolo MCP (`mcp-for-blender`) y Python (`bpy`).

---

## 1. Arquitectura del Pipeline Híbrido (Fidelidad 99.99%)

Para lograr una similitud de nivel profesional (99.99%) con respecto a ilustraciones 2D de referencia sin caer en mallas toscas ("estilo Roblox"):

```text
[Imagen 2D de Referencia / Prompt]
               │
               ▼
  ┌─────────────────────────────┐
  │ 1. Reconstrucción Neuronal  │ ──> Meshy-6 API (Nube) / TRELLIS (Local en D:\AI_Tools\)
  └──────────────┬──────────────┘     Genera malla Quad limpia con mapas PBR (Albedo/Normal/Roughness)
                 │
                 ▼
  ┌─────────────────────────────┐
  │ 2. Ingesta y Limpieza MCP   │ ──> Importa GLB a Blender vía socket 9876
  └──────────────┬──────────────┘     Fusiona vértices, aplica escala, recalcula normales
                 │
                 ▼
  ┌─────────────────────────────┐
  │ 3. Perfeccionamiento Artístico │ ──> Escultura anatómica, proporciones, ropa, accesorios
  └──────────────┬──────────────┘
                 │
                 ▼
  ┌─────────────────────────────┐
  │ 4. Rigging & 12 Principios  │ ──> Esqueleto humanoide, Lattices Squash/Stretch, Curvas Bézier
  └──────────────┬──────────────┘
                 │
                 ▼
  ┌─────────────────────────────┐
  │ 5. Chiaroscuro & Cycles     │ ──> Iluminación de 5 puntos, SSS para piel, Bloom / Glare
  └─────────────────────────────┘
```

---

## 2. Los 12 Principios de Animación de Disney en Blender

Cada principio debe traducirse en configuraciones técnicas reales de Blender:

### 1. Squash and Stretch (Estirar y Encoger)
- **Concepto:** Da flexibilidad, masa y peso a los objetos orgánicos manteniendo constante el volumen total ($X \cdot Y \cdot Z = \text{constante}$).
- **Implementación en Blender:**
  - Asignar un modificador `Lattice` enlazado a un objeto `Lattice` envolvente.
  - O en huesos (Armature): Configurar huesos tipo *B-Bone* o usar un constraint de tipo `Stretch To` con la opción `Volume Variation = STRICT_VOLUME` (o factor 1.0).

### 2. Anticipación (Anticipation)
- **Concepto:** Prepara la vista del espectador antes de una acción importante (ej. agacharse antes de saltar, llevar la mano hacia atrás antes de lanzar).
- **Implementación en Blender:**
  - En la línea de tiempo, insertar keyframes en dirección opuesta al movimiento principal de 3 a 8 fotogramas antes del golpe/salto.
  - Asegurar que la silueta en la pose de anticipación sea completamente legible.

### 3. Puesta en Escena (Staging)
- **Concepto:** Presentar una idea de forma clara e inequívoca mediante la cámara, la iluminación y la pose del personaje.
- **Implementación en Blender:**
  - Composición de cámara con `Composition Guides` activadas (`Rule of Thirds`, `Golden Ratio`).
  - Lentes de retrato cinematográfico (50mm a 85mm) para evitar distorsiones de perspectiva en personajes.
  - Encuadre de siluetas de alto contraste sobre fondos oscuros o controlados.

### 4. Acción Directa y Pose a Pose (Straight Ahead vs. Pose to Pose)
- **Concepto:** *Pose to Pose* para movimientos controlados (Keyframes extremos, breakdowns, e in-betweens). *Straight Ahead* para elementos dinámicos impredecibles (fuego, agua, tela).
- **Implementación en Blender:**
  - Bloqueo en *Stepped Curves* (Interpolación `CONSTANT`) para afinar el timing de las poses clave antes de suavizar a curvas Bézier.

### 5. Acción Continuada y Superpuesta (Follow Through and Overlapping Action)
- **Concepto:** Las distintas partes del cuerpo no se detienen al mismo tiempo. El cabello, los vestidos, y las colas continúan moviéndose tras el cese del movimiento del torso.
- **Implementación en Blender:**
  - Desfasar los keyframes de extremidades y accesorios entre 2 y 5 frames hacia adelante respecto al hueso raíz (`Hips` / `Spine`).
  - Uso de modificadores de tela (`Cloth`) o físicas con vertex groups de pinning en Blender.

### 6. Aceleración y Desaceleración (Slow In and Slow Out)
- **Concepto:** El movimiento natural no es lineal; acelera al inicio y desacelera al final.
- **Implementación en Blender:**
  - En el **Graph Editor**, usar interpolación `BEZIER`.
  - Ajustar las manijas de las curvas F (`F-Curves`) aplanándolas en los extremos para entradas y salidas suaves (*Ease In / Ease Out*).

### 7. Arcos (Arcs)
- **Concepto:** Casi todos los movimientos mecánicos y biológicos siguen trayectorias curvas o parabólicas, no líneas rectas.
- **Implementación en Blender:**
  - Habilitar `Motion Paths` en el objeto o esqueleto para inspeccionar y corregir visualmente la trayectoria parabólica de manos, cabeza y pies.

### 8. Acción Secundaria (Secondary Action)
- **Concepto:** Movimientos adicionales que enriquecen y dan profundidad a la acción principal (ej. un parpadeo, el balanceo de los brazos al caminar, respiración).
- **Implementación en Blender:**
  - Capas de animación en la NLA (*Non-Linear Animation*) para mezclar ciclos de respiración o gesticulación sobre la acción principal.

### 9. Timing y Espaciado
- **Concepto:** La cantidad de frames entre poses determina la velocidad, el peso perceptual y la intención emocional.
- **Implementación en Blender:**
  - Objetos pesados requieren más frames para acelerar y desacelerar. Movimientos ligeros y rápidos requieren pocos frames con frenados secos.

### 10. Exageración (Exaggeration)
- **Concepto:** Llevar la silueta o el movimiento un 20-30% más allá de la realidad física para lograr impacto y claridad visual.
- **Implementación en Blender:**
  - Acentuar la torsión de la columna (`Spine`) y la inclinación de la pelvis para enfatizar dinamismo.

### 11. Dibujo Sólido (Solid Drawing)
- **Concepto:** Considerar las formas en el espacio 3D con volumen, peso, equilibrio y anatomía consistente.
- **Implementación en Blender:**
  - Verificar el modelo desde todos los ángulos (cámara de 360° o `look` con vistas `front`, `right`, `three_quarter`).
  - Evitar planos coincidentes (*z-fighting*), normales invertidas o mallas que se colapsen sobre sí mismas.

### 12. Appeal (Carisma y Atractivo)
- **Concepto:** Diseño visual cautivador, silueta icónica y proporciones armónicas que conectan emocionalmente con el espectador.
- **Implementación en Blender:**
  - Contraste armónico de formas (formas curvas contrapuestas con líneas rectas de tensión).
  - Siluetas legibles incluso si el personaje se reduce a negro sólido.

---

## 3. Morfología, Fisionomía y Anatomía Femenina Estilizada

1. **Proporciones de la Cabeza y Rostro**:
   - Rostro dividido en tres tercios: línea del cabello a cejas, cejas a base de la nariz, y base de la nariz a mentón.
   - Ojos ubicados a la mitad exacta de la altura total de la cabeza.
   - Labios carnosos con arco de Cupido pronunciado y ligero sombreado en las comisuras.

2. **Silueta de Reloj de Arena (Hourglass)**:
   - **Busto:** Proyección voluptuosa hacia el frente (+Y) y ligeramente hacia los lados, con escote pronunciado (*cleavage indentation*) y soporte anatómico firme.
   - **Cintura:** Estrechamiento pronunciado entre la caja torácica y la cresta ilíaca ($Z \approx 0.95 - 1.05\text{m}$), con un ancho de cintura equivalente al 60-65% del ancho de las caderas.
   - **Caderas y Glúteos:** Curvatura amplia y voluptuosa que se extiende hacia los muslos superiores, otorgando peso y feminidad a la silueta.

3. **Manos y Extremidades**:
   - Manos con dedos finos y curvatura relajada o en postura de garras estilizadas, respetando los arcos de longitud (dedo medio más largo, índice y anular equilibrados, meñique más corto).

---

## 4. Shading PBR y Render Cinematográfico en Cycles

### Material de Piel de Alabastro con SSS
```python
# Principled BSDF v2 para Piel
bsdf.inputs["Base Color"].default_value = (0.92, 0.90, 0.88, 1.0)
bsdf.inputs["Roughness"].default_value = 0.35
bsdf.inputs["Subsurface Weight"].default_value = 0.12
bsdf.inputs["Subsurface Radius"].default_value = (1.0, 0.45, 0.30) # Dispersión roja/cálida interna
bsdf.inputs["Subsurface Scale"].default_value = 0.02
```

### Tejido Negro Profundo (Terciopelo / Látex Gótico)
```python
bsdf.inputs["Base Color"].default_value = (0.008, 0.008, 0.010, 1.0)
bsdf.inputs["Roughness"].default_value = 0.75
bsdf.inputs["Sheen Weight"].default_value = 0.70 # Resplandor de borde suave
```

### Emisión Pura para Halos y Auras
```python
# Nodo Emission
emission_node.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)
emission_node.inputs["Strength"].default_value = 45.0
```

### Iluminación de 5 Puntos (Chiaroscuro)
- **Luz Clave (Key Light):** Frontal suave o ligeramente ladeada a 45°, iluminando rostro y torso (80-120W).
- **Luz de Rostro (Face Light):** Foco dedicado de bajo radio dirigido al interior de capuchas o velos para resaltar labios y mirada (35-45W).
- **Luz de Relleno (Fill Light):** Luz suave de temperatura fría opuesta a la clave (30-40W).
- **Kickers / Rim Lights (Izquierda y Derecha):** Dos luces de recorte ubicadas detrás del personaje a 135° para recortar la silueta en fondos negros.
- **Luz de Acento de Halo:** Brillo volumétrico que envuelve la espalda y la cabeza.

---

## 5. Automatización de Cámara y Showcase

El pipeline incorpora animaciones cinemáticas de cámara:
- **Turntable 360°:** Órbita circular suave alrededor del centro de masa del personaje.
- **Slow Zoom:** Acercamiento progresivo con curva Bézier para revelar microdetalles de escote, rostro o joyería.
- **Dolly Rotate:** Traslación frontal simultánea con paneo angular dramático.
- **Crane Shot:** Revelación vertical ascendente desde los pies hasta la corona luminosa.

---

## 6. Exportación Estándar para Motores de Juego (Unreal Engine & Web)

1. **Unreal Engine 5 (FBX):**
   - Escala: 1.0 con unidades métricas aplicadas (`apply_unit_scale=True`, `bake_space_transform=True`).
   - Sistema de coordenadas: Z-Up, Y-Forward.
   - Suavizado: `mesh_smooth_type='FACE'`.

2. **Web / Three.js (GLB):**
   - Formato binario `.glb` con compresión Draco y texturas PBR embebidas.
