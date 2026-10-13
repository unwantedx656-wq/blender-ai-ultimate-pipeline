"""
Camera Cinematics Automation for Blender 3D
Implements professional camera trajectories and showcase orbits via Python bpy.
"""

def generate_turntable_code(target_name: str = "Character_Body", frames: int = 120, height: float = 1.3, distance: float = 2.5) -> str:
    """Genera código bpy para rotación continua de cámara de 360 grados."""
    return f"""
import bpy
import math

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = {frames}

# Crear o reutilizar cámara
cam = bpy.data.objects.get("Camera_Turntable")
if not cam:
    cam_data = bpy.data.cameras.new("Camera_Turntable")
    cam = bpy.data.objects.new("Camera_Turntable", cam_data)
    scene.collection.objects.link(cam)
scene.camera = cam

# Empty para rotación en el centro
target = bpy.data.objects.get("{target_name}")
target_loc = target.location if target else (0, 0, {height})

empty = bpy.data.objects.get("Turntable_Center")
if not empty:
    empty = bpy.data.objects.new("Turntable_Center", None)
    scene.collection.objects.link(empty)
empty.location = (target_loc[0], target_loc[1], {height})

# Emparentar cámara
cam.parent = empty
cam.location = (0, -{distance}, 0)
cam.rotation_euler = (math.radians(90), 0, 0)

# Animación de rotación 360 grados
empty.animation_data_clear()
empty.rotation_euler = (0, 0, 0)
empty.keyframe_insert(data_path="rotation_euler", frame=1)
empty.rotation_euler = (0, 0, math.radians(360))
empty.keyframe_insert(data_path="rotation_euler", frame={frames})

# Configurar interpolación lineal en F-Curves para bucle perfecto
if empty.animation_data and empty.animation_data.action:
    for fcurve in empty.animation_data.action.fcurves:
        for kp in fcurve.keyframe_points:
            kp.interpolation = 'LINEAR'
print("Animación Turntable 360 configurada exitosamente.")
"""

def generate_slow_zoom_code(target_name: str = "Character_Body", frames: int = 90, start_dist: float = 3.2, end_dist: float = 1.6, height: float = 1.3) -> str:
    """Genera código bpy para acercamiento cinemático con desaceleración Bézier."""
    return f"""
import bpy

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = {frames}

cam = scene.camera
if cam:
    cam.animation_data_clear()
    cam.location = (0, -{start_dist}, {height})
    cam.keyframe_insert(data_path="location", frame=1)
    
    cam.location = (0, -{end_dist}, {height})
    cam.keyframe_insert(data_path="location", frame={frames})
    
    # Suavizado Bézier
    if cam.animation_data and cam.animation_data.action:
        for fcurve in cam.animation_data.action.fcurves:
            for kp in fcurve.keyframe_points:
                kp.interpolation = 'BEZIER'
                kp.easing = 'EASE_OUT'
print("Animación Slow Zoom configurada exitosamente.")
"""

def generate_crane_shot_code(frames: int = 100, start_z: float = 0.2, end_z: float = 2.0, distance: float = 2.4) -> str:
    """Genera código bpy para revelación vertical de grúa (de abajo hacia arriba)."""
    return f"""
import bpy
import math

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = {frames}

cam = scene.camera
if cam:
    cam.animation_data_clear()
    cam.location = (0, -{distance}, {start_z})
    cam.rotation_euler = (math.radians(80), 0, 0)
    cam.keyframe_insert(data_path="location", frame=1)
    cam.keyframe_insert(data_path="rotation_euler", frame=1)
    
    cam.location = (0, -{distance}, {end_z})
    cam.rotation_euler = (math.radians(98), 0, 0)
    cam.keyframe_insert(data_path="location", frame={frames})
    cam.keyframe_insert(data_path="rotation_euler", frame={frames})
    
    if cam.animation_data and cam.animation_data.action:
        for fcurve in cam.animation_data.action.fcurves:
            for kp in fcurve.keyframe_points:
                kp.interpolation = 'BEZIER'
print("Animación Crane Shot configurada exitosamente.")
"""
