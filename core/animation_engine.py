"""
Animation Engine: Implementation of Disney's 12 Principles in Blender 3D (bpy).
Provides programmatic recipes to apply professional animation techniques to 3D characters and props.
"""

def setup_squash_and_stretch_lattice(target_obj_name: str, lattice_name: str = "Anim_Lattice") -> str:
    """Implementa el Principio 1 (Squash & Stretch) mediante un deformador Lattice con conservación de volumen."""
    return f"""
import bpy

target = bpy.data.objects.get("{target_obj_name}")
if target:
    # Crear Lattice
    lat_data = bpy.data.lattices.new("{lattice_name}")
    lat_data.points_u = 3
    lat_data.points_v = 3
    lat_data.points_w = 4
    
    lat_obj = bpy.data.objects.new("{lattice_name}", lat_data)
    bpy.context.scene.collection.objects.link(lat_obj)
    
    # Alinear al objeto objetivo
    lat_obj.location = target.location
    lat_obj.dimensions = target.dimensions * 1.05
    
    # Añadir modificador Lattice al objetivo
    mod = target.modifiers.new("Squash_Stretch", 'LATTICE')
    mod.object = lat_obj
    print(f"Modificador Lattice Squash & Stretch asignado a {{target.name}}")
"""

def apply_bezier_slow_in_out(obj_name: str) -> str:
    """Implementa el Principio 6 (Slow In & Slow Out) ajustando manijas Bézier en el Graph Editor."""
    return f"""
import bpy

obj = bpy.data.objects.get("{obj_name}")
if obj and obj.animation_data and obj.animation_data.action:
    for fcurve in obj.animation_data.action.fcurves:
        for kp in fcurve.keyframe_points:
            kp.interpolation = 'BEZIER'
            kp.handle_left_type = 'AUTO_CLAMPED'
            kp.handle_right_type = 'AUTO_CLAMPED'
    print(f"Curvas Bézier con Slow In/Out aplicadas a {{obj.name}}")
"""

def apply_overlapping_action(bone_names: list, frame_delay: int = 3, armature_name: str = "Armature") -> str:
    """Implementa el Principio 5 (Follow Through & Overlapping Action) desfasando keyframes de cadenas articulares."""
    return f"""
import bpy

arm = bpy.data.objects.get("{armature_name}")
if arm and arm.animation_data and arm.animation_data.action:
    action = arm.animation_data.action
    bones = {bone_names}
    for idx, bname in enumerate(bones):
        delay = idx * {frame_delay}
        if delay == 0:
            continue
        # Desfasar F-Curves de este hueso
        for fcurve in action.fcurves:
            if f'pose.bones["{{bname}}"]' in fcurve.data_path:
                for kp in fcurve.keyframe_points:
                    kp.co[0] += delay
                    kp.handle_left[0] += delay
                    kp.handle_right[0] += delay
    print("Acción superpuesta (Overlapping Action) aplicada a la cadena de huesos.")
"""

def setup_anticipation_frame(obj_name: str, main_frame: int, ant_frames_back: int = 5, factor: float = -0.2) -> str:
    """Implementa el Principio 2 (Anticipación) insertando una pose previa en dirección contraria."""
    return f"""
import bpy

obj = bpy.data.objects.get("{obj_name}")
if obj and obj.animation_data and obj.animation_data.action:
    action = obj.animation_data.action
    ant_frame = {main_frame} - {ant_frames_back}
    for fcurve in action.fcurves:
        val_main = fcurve.evaluate({main_frame})
        val_start = fcurve.evaluate(1)
        delta = val_main - val_start
        ant_val = val_start + delta * {factor}
        fcurve.keyframe_points.insert(ant_frame, ant_val)
    print("Fotograma clave de anticipación calculado e insertado.")
"""
