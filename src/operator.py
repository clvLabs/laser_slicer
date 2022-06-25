import bpy
import time
from .slicer import slicer

class OBJECT_OT_LaserSlicer_preview(bpy.types.Operator):
  '''Preview result of slicing'''
  bl_label = "Laser Slicer - Preview"
  bl_idname = "object.laser_slicer_preview"

  def execute(self, context):
    run_slicer(self, True)
    return {'FINISHED'}


class OBJECT_OT_LaserSlicer_slice(bpy.types.Operator):
  '''Slice selected object'''
  bl_label = "Laser Slicer - Slice"
  bl_idname = "object.laser_slicer_slice"

  def execute(self, context):
    run_slicer(self, False)
    return {'FINISHED'}

# --------------------------------------------------------------------------------

def run_slicer(operator, preview):
  prefs = bpy.context.preferences.addons[__package__.split('.')[0]].preferences
  prefs.preview = preview

  start_time = time.time()
  slicer(prefs)

  elapsed = time.time() - start_time
  msg = f"[laser-slicer] FINISHED in {elapsed:5.2f}s"
  operator.report({'INFO'}, msg)

# --------------------------------------------------------------------------------

EXPORTED_CLASSES = (
  OBJECT_OT_LaserSlicer_preview,
  OBJECT_OT_LaserSlicer_slice,
)
