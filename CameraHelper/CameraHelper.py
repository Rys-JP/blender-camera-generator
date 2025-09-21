bl_info = {
    "name": "CameraHelper",
    "author": "Rys",
    "version": (1,0,0),
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
        target_loc = Vector((0,0,0)) #(0,0,0) is tuple, Vector()  

    #ターゲットエンプティを生成
    bpy.ops.object.empty_add(location=(0,0,0))
    target_empty = bpy.context.active_object
    target_empty.name = "Target_empty"

    #カメラリグを生成
    bpy.ops.object.empty_add(location=(0,-10,0))
    camera_rig = bpy.context.active_object
    camera_rig.name = "Camera_rig"
    camera_rig.parent = target_empty
    
    #カメラを生成
    bpy.ops.object.camera_add(location=(0,-10,0)) #World座標内
    camera = bpy.context.active_object
    camera.name = "Camera"
    constraint = camera.constraints.new(type="TRACK_TO")
    constraint.target = target_empty
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"
    bpy.context.view_layer.update()
    camera.matrix_world = camera.matrix_world.copy()
    camera.constraints.remove(constraint)
    camera.location = (0,0,0) #local座標内
    camera.parent = camera_rig
    #対象とエンプティは親子付けしない
        
    return target_loc, target_empty, camera_rig, camera

#Pan
def do_pan(target_loc, target_empty, camera):
    camera.rotation_euler.z = radians(20)
    camera.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
    #rotation_euler.zはdata_path="rotation_euler", index=2に対応
    camera.rotation_euler.z = radians(-20)
    camera.keyframe_insert(data_path="rotation_euler", index=2, frame=50)
    
    target_empty.location = target_loc
    return
    
#Tilt
def do_tilt(target_loc, target_empty, camera):
    camera.rotation_euler.x = radians(70)
    camera.keyframe_insert(data_path="rotation_euler", index=0, frame=1)
    camera.rotation_euler.x = radians(110)
    camera.keyframe_insert(data_path="rotation_euler", index=0, frame=50)
    
    target_empty.location = target_loc
    return

#Dolly
def do_dolly(target_loc, target_empty, camera_rig):
    camera_rig.location.y = -10
    camera_rig.keyframe_insert(data_path="location", index=1, frame=1)
    camera_rig.location.y = -5
    camera_rig.keyframe_insert(data_path="location", index=1, frame=50)
    
    target_empty.location = target_loc
    return
    
#Truck
def do_truck(target_loc, target_empty, camera_rig):
    camera_rig.location.x = -5
    camera_rig.keyframe_insert(data_path="location", index=0, frame=1)
    camera_rig.location.x = 5
    camera_rig.keyframe_insert(data_path="location", index=0, frame=50)
    #Z
    camera_rig.location.z = 0
    camera_rig.keyframe_insert(data_path="location", index=2, frame=1)
    camera_rig.keyframe_insert(data_path="location", index=2, frame=50)
    
    target_empty.location = target_loc
    return
        
#Orbit
def do_orbit(target_loc, target_empty):
    target_empty.rotation_euler.z = radians(0)
    target_empty.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
    target_empty.rotation_euler.z = radians(360)
    target_empty.keyframe_insert(data_path="rotation_euler", index=2, frame=50)
    
    target_empty.rotation_euler.x = radians(0)
    target_empty.keyframe_insert(data_path="rotation_euler", index=0, frame=1)
    target_empty.rotation_euler.x = radians(0)
    target_empty.keyframe_insert(data_path="rotation_euler", index=0, frame=50)
    
    target_empty.location = target_loc
    return
 
#Zoom
def do_zoom(target_loc, target_empty, camera):
    camera.data.lens = 50
    camera.data.keyframe_insert(data_path="lens", frame=1)
    camera.data.lens = 100
    camera.data.keyframe_insert(data_path="lens", frame=50)
    
    target_empty.location = target_loc
    return

#Operator
class OBJECT_OT_camera_helper(bpy.types.Operator):
    bl_idname = "object.camera_helper" 
    bl_label = "CameraHelper"
    
    def execute(self, context): 
        target_loc, target_empty, camera_rig, camera = create_camera_setup()           
        if bpy.context.scene.pan_checkbox == True:
            do_pan(target_loc, target_empty, camera)
            bpy.context.scene.pan_checkbox = False
        else: pass
        if bpy.context.scene.tilt_checkbox == True:
            do_tilt(target_loc, target_empty, camera)
            bpy.context.scene.tilt_checkbox = False
        else: pass
        if bpy.context.scene.dolly_checkbox == True:
            do_dolly(target_loc, target_empty, camera_rig)
            bpy.context.scene.dolly_checkbox = False
        else: pass
        if bpy.context.scene.truck_checkbox == True:
            do_truck(target_loc, target_empty, camera_rig)
            bpy.context.scene.truck_checkbox = False
        else: pass
        if bpy.context.scene.orbit_checkbox == True:
            do_orbit(target_loc, target_empty)
            bpy.context.scene.orbit_checkbox = False
        else: pass
        if bpy.context.scene.zoom_checkbox == True:
            do_zoom(target_loc, target_empty, camera)
            bpy.context.scene.zoom_checkbox = False
        else: pass
        return {'FINISHED'}
                
#Panel        
class OBJECT_PT_camera_helper(bpy.types.Panel):
    bl_label = "CameraHelper"
    bl_idname = "OBJECT_PT_helper_panel"
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
        layout.operator("object.camera_helper", text="Create")
       
def register():
    bpy.utils.register_class(OBJECT_OT_camera_helper)
    bpy.utils.register_class(OBJECT_PT_camera_helper)
    bpy.types.Scene.pan_checkbox = bpy.props.BoolProperty(name="Pan")
    bpy.types.Scene.tilt_checkbox = bpy.props.BoolProperty(name="Tilt")
    bpy.types.Scene.dolly_checkbox = bpy.props.BoolProperty(name="Dolly")
    bpy.types.Scene.truck_checkbox = bpy.props.BoolProperty(name="Truck")
    bpy.types.Scene.orbit_checkbox = bpy.props.BoolProperty(name="Orbit")
    bpy.types.Scene.zoom_checkbox = bpy.props.BoolProperty(name="Zoom")
      
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_camera_helper)
    bpy.utils.unregister_class(OBJECT_PT_camera_helper)
    del bpy.types.Scene.pan_checkbox
    del bpy.types.Scene.tilt_checkbox
    del bpy.types.Scene.dolly_checkbox
    del bpy.types.Scene.truck_checkbox
    del bpy.types.Scene.orbit_checkbox
    del bpy.types.Scene.zoom_checkbox

if __name__ == "__main__":
    register()