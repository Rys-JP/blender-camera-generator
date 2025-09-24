bl_info = {
    "name": "CameraGenerator",
    "author": "Yoshida Shun",
    "version": (1,0,3),
    "blender": (4,2,1),
    "location": "View3D > Tool Shelf",
    "description": "カメラワークを自動生成するアドオン"
}

import bpy
import math
from mathutils import Vector
from math import radians
        
def create_camera_setup():
    #対象物を選択
    if bpy.context.active_object:
        target_loc = bpy.context.active_object.location
    else:
        target_loc = Vector((0,0,0)) 

    #ターゲットを生成
    bpy.ops.object.empty_add(location=(0,0,0))
    target = bpy.context.active_object
    target.name = "Target"

    #エンプティを生成
    bpy.ops.object.empty_add(location=(0,-10,0))
    empty = bpy.context.active_object
    empty.name = "Empty"
    empty.parent = target
    
    #カメラを生成
    bpy.ops.object.camera_add(location=(0,-10,0)) #World座標内
    camera = bpy.context.active_object
    camera.name = "Camera"
    #カメラをターゲットに向ける
    constraint = camera.constraints.new(type="TRACK_TO")
    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"
    bpy.context.view_layer.update()
    #ベイクして制約解除
    camera.matrix_world = camera.matrix_world.copy()
    camera.constraints.remove(constraint)
    camera.location = (0,0,0) #Local座標内
    camera.parent = empty
    
    target.location = target_loc
    #対象とエンプティは親子付けしない    
    return target, empty, camera

#Pan
def do_pan(empty):
    empty.rotation_euler.z = radians(20)
    empty.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
    #rotation_euler.zはdata_path="rotation_euler", index=2に対応
    empty.rotation_euler.z = radians(-20)
    empty.keyframe_insert(data_path="rotation_euler", index=2, frame=50)
    return
    
#Tilt
def do_tilt(empty):
    empty.rotation_euler.x = radians(70)
    empty.keyframe_insert(data_path="rotation_euler", index=0, frame=1)
    empty.rotation_euler.x = radians(110)
    empty.keyframe_insert(data_path="rotation_euler", index=0, frame=50)
    return

#Dolly
def do_dolly(empty):
    empty.location.y = -10
    empty.keyframe_insert(data_path="location", index=1, frame=1)
    empty.location.y = -5
    empty.keyframe_insert(data_path="location", index=1, frame=50)
    return
    
#Truck
def do_truck(empty):
    empty.location.x = -5
    empty.keyframe_insert(data_path="location", index=0, frame=1)
    empty.location.x = 5
    empty.keyframe_insert(data_path="location", index=0, frame=50)
    #Z
    empty.location.z = 0
    empty.keyframe_insert(data_path="location", index=2, frame=1)
    empty.keyframe_insert(data_path="location", index=2, frame=50)
    return
        
#Orbit
def do_orbit(target):
    target.rotation_euler.z = radians(0)
    target.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
    target.rotation_euler.z = radians(360)
    target.keyframe_insert(data_path="rotation_euler", index=2, frame=50)
    
    target.rotation_euler.x = radians(0)
    target.keyframe_insert(data_path="rotation_euler", index=0, frame=1)
    target.rotation_euler.x = radians(0)
    target.keyframe_insert(data_path="rotation_euler", index=0, frame=50)
    return
 
#Zoom
def do_zoom(camera):
    camera.data.lens = 50
    camera.data.keyframe_insert(data_path="lens", frame=1)
    camera.data.lens = 100
    camera.data.keyframe_insert(data_path="lens", frame=50)
    return

#Operator
class OBJECT_OT_camera_generator(bpy.types.Operator):
    bl_idname = "object.camera_generator" 
    bl_label = "CameraGenerator"
    
    def execute(self, context): 
        target, empty, camera = create_camera_setup()           
        if bpy.context.scene.pan_checkbox == True:
            do_pan(camera)
            bpy.context.scene.pan_checkbox = False
        else: pass
        if bpy.context.scene.tilt_checkbox == True:
            do_tilt(camera)
            bpy.context.scene.tilt_checkbox = False
        else: pass
        if bpy.context.scene.dolly_checkbox == True:
            do_dolly(empty)
            bpy.context.scene.dolly_checkbox = False
        else: pass
        if bpy.context.scene.truck_checkbox == True:
            do_truck(empty)
            bpy.context.scene.truck_checkbox = False
        else: pass
        if bpy.context.scene.orbit_checkbox == True:
            do_orbit(target)
            bpy.context.scene.orbit_checkbox = False
        else: pass
        if bpy.context.scene.zoom_checkbox == True:
            do_zoom(camera)
            bpy.context.scene.zoom_checkbox = False
        else: pass
        return {'FINISHED'}
                
#Panel        
class OBJECT_PT_camera_generator(bpy.types.Panel):
    bl_label = "CameraGenerator"
    bl_idname = "OBJECT_PT_generator_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Camera'       

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "pan_checkbox", text="Pan")
        layout.prop(context.scene, "tilt_checkbox", text="Tilt")
        layout.prop(context.scene, "dolly_checkbox", text="Dolly")
        layout.prop(context.scene, "truck_checkbox", text="Truck")
        layout.prop(context.scene, "orbit_checkbox", text="Orbit")
        layout.prop(context.scene, "zoom_checkbox", text="Zoom")
        layout.operator("object.camera_generator", text="Create")
       
def register():
    bpy.utils.register_class(OBJECT_OT_camera_generator)
    bpy.utils.register_class(OBJECT_PT_camera_generator)
    bpy.types.Scene.pan_checkbox = bpy.props.BoolProperty(name="Pan")
    bpy.types.Scene.tilt_checkbox = bpy.props.BoolProperty(name="Tilt")
    bpy.types.Scene.dolly_checkbox = bpy.props.BoolProperty(name="Dolly")
    bpy.types.Scene.truck_checkbox = bpy.props.BoolProperty(name="Truck")
    bpy.types.Scene.orbit_checkbox = bpy.props.BoolProperty(name="Orbit")
    bpy.types.Scene.zoom_checkbox = bpy.props.BoolProperty(name="Zoom")
      
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_camera_generator)
    bpy.utils.unregister_class(OBJECT_PT_camera_generator)
    del bpy.types.Scene.pan_checkbox
    del bpy.types.Scene.tilt_checkbox
    del bpy.types.Scene.dolly_checkbox
    del bpy.types.Scene.truck_checkbox
    del bpy.types.Scene.orbit_checkbox
    del bpy.types.Scene.zoom_checkbox

if __name__ == "__main__":
    register()