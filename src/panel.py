import bpy

class LaserSlicer_Panel(bpy.types.Panel):
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"
  bl_context = "objectmode"
  bl_category = "Laser"


class OBJECT_PT_LaserSlicer_About_Panel(LaserSlicer_Panel):
  bl_label = "Laser Slicer"
  bl_options = {'DEFAULT_CLOSED'}

  def draw(self, context):
    layout = self.layout

    col = layout.column()
    col.label(text="Laser slicer add-on for Blender.")
    op = col.operator(
        'wm.url_open',
        text='See on Github',
        icon='URL'
        )
    op.url = 'https://github.com/clvLabs/laser_slicer'


class OBJECT_PT_LaserSlicer_Material_Panel(LaserSlicer_Panel):
  bl_label = "Material settings"

  def draw(self, context):
    layout = self.layout
    prefs = bpy.context.preferences.addons[__package__.split('.')[0]].preferences

    layout.row().prop(prefs, "material_thickness")
    layout.row().prop(prefs, "material_width")
    layout.row().prop(prefs, "material_height")

    layout.separator()
    layout.row().operator(
      "object.op_laser_slicer_preferences_reset",
      text='Reset material defaults',
      icon='LOOP_BACK').mode = "MATERIAL"


class OBJECT_PT_LaserSlicer_Cut_Panel(LaserSlicer_Panel):
  bl_label = "Cut settings"

  def draw(self, context):
    layout = self.layout
    prefs = bpy.context.preferences.addons[__package__.split('.')[0]].preferences

    layout.row().prop(prefs, "dpi")
    layout.row().prop(prefs, "cut_line_color")
    layout.row().prop(prefs, "cut_line_thickness")
    layout.row().prop(prefs, "cut_thickness")

    layout.separator()
    layout.row().operator(
      "object.op_laser_slicer_preferences_reset",
      text='Reset cut defaults',
      icon='LOOP_BACK').mode = "CUT"


class OBJECT_PT_LaserSlicer_Slice_Panel(LaserSlicer_Panel):
  bl_label = "Slice"

  def draw(self, context):
    scene = context.scene
    layout = self.layout
    prefs = bpy.context.preferences.addons[__package__.split('.')[0]].preferences

    layout.row().prop(prefs, "ofile")
    layout.row().prop(prefs, "separate_files")
    if prefs.separate_files:
      layout.row().prop(prefs, "svg_position", text="Pos")
    layout.row().prop(prefs, "preview")

    layout.separator()
    layout.row().operator(
      "object.op_laser_slicer_preferences_reset",
      text='Reset slice defaults',
      icon='LOOP_BACK').mode = "SLICE"

    # --- Slice button ---

    if context.active_object \
      and context.active_object.select_get() \
      and context.active_object.type == 'MESH' \
      and context.active_object.data.polygons:

      row = layout.row()
      slice_count = context.active_object.dimensions[2] * 1000 * context.scene.unit_settings.scale_length / prefs.material_thickness
      row.label(text = 'No. of slices : {:.0f}'.format(slice_count))

      split = layout.split()
      col = split.column()
      if not bpy.data.filepath and not prefs.ofile:
        col.alert = True
        col.label(text="Please save file before slicing")
      else:
        col.operator("object.laser_slicer", text="Slice the object", icon='PLAY')

    else:
      split = layout.split()
      col = split.column()
      col.alert = True
      col.label(text="Please select an object to slice")

# --------------------------------------------------------------------------------

EXPORTED_CLASSES = (
  OBJECT_PT_LaserSlicer_About_Panel,
  OBJECT_PT_LaserSlicer_Material_Panel,
  OBJECT_PT_LaserSlicer_Cut_Panel,
  OBJECT_PT_LaserSlicer_Slice_Panel,
)
