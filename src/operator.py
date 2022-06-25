import bpy
from .slicer import slicer

class OBJECT_OT_LaserSlicer(bpy.types.Operator):
  bl_label = "Laser Slicer"
  bl_idname = "object.laser_slicer"

  def execute(self, context):
    prefs = bpy.context.preferences.addons[__package__.split('.')[0]].preferences
    slicer(prefs)
    return {'FINISHED'}

# --------------------------------------------------------------------------------

EXPORTED_CLASSES = (
  OBJECT_OT_LaserSlicer,
)
