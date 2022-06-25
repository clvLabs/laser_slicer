import bpy

class LaserSlicer_Panel(bpy.types.Panel):
  '''Base class for LaserSlicer panels'''
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"
  bl_context = "objectmode"
  bl_category = "Laser"


class OBJECT_PT_LaserSlicer_About_Panel(LaserSlicer_Panel):
  '''About panel'''
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
  '''Material settings panel'''
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
  '''Cut settings panel'''
  bl_label = "Cut settings"

  def draw(self, context):
    layout = self.layout
    prefs = bpy.context.preferences.addons[__package__.split('.')[0]].preferences

    layout.row().prop(prefs, "dpi")
    layout.row().prop(prefs, "cut_line_color")
    layout.row().prop(prefs, "cut_line_thickness")
    layout.row().prop(prefs, "laser_kerf")

    layout.separator()
    layout.row().operator(
      "object.op_laser_slicer_preferences_reset",
      text='Reset cut defaults',
      icon='LOOP_BACK').mode = "CUT"


class OBJECT_PT_LaserSlicer_Slice_Panel(LaserSlicer_Panel):
  '''Slice panel'''
  bl_label = "Slice"

  def draw(self, context):
    scene = context.scene
    layout = self.layout
    prefs = bpy.context.preferences.addons[__package__.split('.')[0]].preferences

    layout.row().prop(prefs, "slice_gap")
    layout.row().prop(prefs, "output_file")
    layout.row().prop(prefs, "separate_files")
    if prefs.separate_files:
      layout.row().prop(prefs, "svg_position", text="Pos")

    layout.separator()
    layout.row().operator(
      "object.op_laser_slicer_preferences_reset",
      text='Reset slice defaults',
      icon='LOOP_BACK').mode = "SLICE"

    # --- Previes/Slice buttons ---

    if context.active_object \
      and context.active_object.select_get() \
      and context.active_object.type == 'MESH' \
      and context.active_object.data.polygons:

      row = layout.row()
      _factor = 1000 * context.scene.unit_settings.scale_length / (prefs.material_thickness + prefs.slice_gap)
      slice_count = context.active_object.dimensions[2] * _factor
      row.label(text = 'No. of slices : {:.0f}'.format(slice_count))

      split = layout.split()
      if not bpy.data.filepath and not prefs.output_file:
        col = split.column()
        col.alert = True
        col.label(text="Please save file before slicing")
      else:
        col = split.column()
        col.operator("object.laser_slicer_preview", text="Preview", icon='HIDE_OFF')
        col = split.column()
        col.operator("object.laser_slicer_slice", text="Slice", icon='PLAY')

    else:
      split = layout.split()
      col = split.column()
      col.alert = True
      col.label(text="Please select an object to slice")


class OBJECT_PT_LaserSlicer_Reset_Panel(LaserSlicer_Panel):
  '''Reset panel'''
  bl_label = "Reset"
  bl_options = {'DEFAULT_CLOSED'}

  def draw(self, context):
    layout = self.layout

    row = layout.row()
    row.alert = True
    row.operator(
      "object.op_laser_slicer_preferences_reset",
      text='Reset ALL preferences',
      icon='LOOP_BACK').mode = "ALL"

# --------------------------------------------------------------------------------

EXPORTED_CLASSES = (
  OBJECT_PT_LaserSlicer_About_Panel,
  OBJECT_PT_LaserSlicer_Material_Panel,
  OBJECT_PT_LaserSlicer_Cut_Panel,
  OBJECT_PT_LaserSlicer_Slice_Panel,
  OBJECT_PT_LaserSlicer_Reset_Panel,
)
