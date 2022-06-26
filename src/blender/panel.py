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

    row = layout.row()
    row.alert = True
    row.operator(
      "object.op_laser_slicer_preferences_reset",
      text='Reset ALL defaults',
      icon='LOOP_BACK').mode = "ALL"


class OBJECT_PT_LaserSlicer_MaterialSettings_Panel(LaserSlicer_Panel):
  '''Material settings panel'''
  bl_label = "Material settings"
  bl_options = {'DEFAULT_CLOSED'}

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


class OBJECT_PT_LaserSlicer_CutSettings_Panel(LaserSlicer_Panel):
  '''Cut settings panel'''
  bl_label = "Cut settings"
  bl_options = {'DEFAULT_CLOSED'}

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


class OBJECT_PT_LaserSlicer_3DPreviewSettings_Panel(LaserSlicer_Panel):
  '''3D preview settings panel'''
  bl_label = "3D preview settings"
  bl_options = {'DEFAULT_CLOSED'}

  def draw(self, context):
    layout = self.layout
    prefs = bpy.context.preferences.addons[__package__.split('.')[0]].preferences

    layout.row().prop(prefs, "extrude_slices")
    layout.row().label(text="Translate preview:")
    layout.row().prop(prefs, "preview_x_translate", text="X")
    layout.row().prop(prefs, "preview_y_translate", text="Y")
    layout.row().prop(prefs, "preview_z_translate", text="Z")

    layout.separator()
    layout.row().operator(
      "object.op_laser_slicer_preferences_reset",
      text='Reset 3D preview defaults',
      icon='LOOP_BACK').mode = "3DPREVIEW"


class OBJECT_PT_LaserSlicer_SliceSettings_Panel(LaserSlicer_Panel):
  '''Slice settings panel'''
  bl_label = "Slice settings"
  bl_options = {'DEFAULT_CLOSED'}

  def draw(self, context):
    scene = context.scene
    layout = self.layout
    prefs = bpy.context.preferences.addons[__package__.split('.')[0]].preferences

    layout.row().prop(prefs, "slice_gap")
    layout.row().prop(prefs, "slice_range")
    if prefs.slice_range == "S":
      layout.row().prop(prefs, "single_slice_pct")
    elif prefs.slice_range == "R":
      layout.row().prop(prefs, "slice_range_start_pct")
      layout.row().prop(prefs, "slice_range_end_pct")
    layout.row().prop(prefs, "output_file")
    layout.row().prop(prefs, "separate_files")
    if prefs.separate_files:
      layout.row().prop(prefs, "svg_position", text="Pos")

    layout.separator()
    layout.row().operator(
      "object.op_laser_slicer_preferences_reset",
      text='Reset slice defaults',
      icon='LOOP_BACK').mode = "SLICE"


class OBJECT_PT_LaserSlicer_Slice_Panel(LaserSlicer_Panel):
  '''Slice panel'''
  bl_label = "Slice"

  def draw(self, context):
    scene = context.scene
    layout = self.layout
    prefs = bpy.context.preferences.addons[__package__.split('.')[0]].preferences

    selected_object_count = len(bpy.context.selected_objects)

    valid_object_selected = context.active_object \
      and selected_object_count == 1 \
      and context.active_object.select_get() \
      and context.active_object.type == 'MESH' \
      and context.active_object.data.polygons

    slicing_allowed = valid_object_selected

    stats = [f"{selected_object_count} objects selected."]
    warning_str = ""

    if valid_object_selected:

      # stats: Object size
      _fac = 1000 * context.scene.unit_settings.scale_length
      _dim = context.active_object.dimensions
      _str = f"Size: {int(_dim[0]*_fac)}x{int(_dim[1]*_fac)}x{int(_dim[2]*_fac)}"
      stats.append(_str)

      # stats: Slice count
      _factor = 1000 * context.scene.unit_settings.scale_length / (prefs.material_thickness + prefs.slice_gap)
      slice_count = context.active_object.dimensions[2] * _factor
      stats.append(f"{slice_count:.0f} slices")

      # warning: Slicing DISABLED
      if not bpy.data.filepath and not prefs.output_file:
        slicing_allowed = False
        warning_str = "Slicing DISABLED: Save or specify output to enable."
    else:
      # warning: No valid object selected
      if not selected_object_count:
        warning_str = "Select an object to slice."
      elif selected_object_count > 1:
        warning_str = "Select a SINGLE object to slice."

    # Show stats
    for stats_str in stats:
      row = layout.row()
      row.label(text=stats_str)

    # Show warning
    if warning_str:
      row = layout.row()
      row.alert = True
      row.label(text=warning_str)

    # Show action buttons
    split = layout.split()

    col = split.column()
    col.operator("object.laser_slicer_preview", text="Preview", icon='HIDE_OFF')
    if not valid_object_selected:
      col.enabled = False

    col = split.column()
    col.operator("object.laser_slicer_slice", text="Slice", icon='FILE_TICK')
    if not slicing_allowed:
      col.enabled = False

# --------------------------------------------------------------------------------

EXPORTED_CLASSES = (
  OBJECT_PT_LaserSlicer_About_Panel,
  OBJECT_PT_LaserSlicer_MaterialSettings_Panel,
  OBJECT_PT_LaserSlicer_CutSettings_Panel,
  OBJECT_PT_LaserSlicer_3DPreviewSettings_Panel,
  OBJECT_PT_LaserSlicer_SliceSettings_Panel,
  OBJECT_PT_LaserSlicer_Slice_Panel,
)
