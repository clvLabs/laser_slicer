import bpy


class Slicer_Preferences_Reset(bpy.types.Operator):
  ''' Reset settings for laser-slicer '''

  bl_idname = "object.op_laser_slicer_preferences_reset"
  bl_label = "Reset preferences"

  mode: bpy.props.StringProperty(default="ALL")


  def execute(self, context):
    prefs = bpy.context.preferences.addons[__package__.split('.')[0]].preferences
    mode = self.mode.upper()

    if mode == "":
      mode = "ALL"

    if mode == "ALL" or mode == "MATERIAL":
      prefs.property_unset('material_thickness')
      prefs.property_unset('material_width')
      prefs.property_unset('material_height')

    if mode == "ALL" or mode == "CUT":
      prefs.property_unset('dpi')
      prefs.property_unset('cut_line_color')
      prefs.property_unset('cut_line_thickness')
      prefs.property_unset('laser_kerf')

    if mode == "ALL" or mode == "SLICE":
      prefs.property_unset('ofile')
      prefs.property_unset('separate_files')
      prefs.property_unset('svg_position')
      prefs.property_unset('preview')

    return {'FINISHED'}


class Slicer_Preferences(bpy.types.AddonPreferences):
  ''' Settings for laser-slicer '''

  bl_idname=__package__.split('.')[0]

  # ------------------------------------------------------------------------
  # Material

  material_thickness: bpy.props.FloatProperty(
    name="Thickness",
    description="Thickness of the cutting material (mm)",
    min=0.1,
    soft_min=1,
    soft_max=10,
    step=0.1*100,
    default=3,
    )

  material_width: bpy.props.FloatProperty(
    name="Width",
    description="Width of the cutting material (mm)",
    min=1,
    soft_min=10,
    soft_max=700,
    step=10*100,
    default=210,
    )

  material_height: bpy.props.FloatProperty(
    name="Height",
    description="Height of the cutting material (mm)",
    min=1,
    soft_min=10,
    soft_max=500,
    step=10*100,
    default=297,
    )

  # ------------------------------------------------------------------------
  # Cut settings

  dpi: bpy.props.IntProperty(
    name="DPI",
    description="DPI of the laser cutter computer",
    min=1,
    soft_min=50,
    soft_max=500,
    default=96,
    )

  cut_line_color: bpy.props.FloatVectorProperty(
    name="SVG line color",
    description="Color of the generated SVG line",
    subtype ='COLOR',
    default=[1.0, 0.0, 0.0],
    )

  cut_line_thickness: bpy.props.IntProperty(
    name="SVG line thickness",
    description="Thickness of the generated SVG line (pixels)",
    min=0,
    soft_max=5,
    default=1,
    )

  laser_kerf: bpy.props.FloatProperty(
    name="Laser kerf",
    description="Thickness of the laser cut (mm)",
    min=0,
    soft_max=5,
    default=0.04,
    )

  # ------------------------------------------------------------------------
  # Slice settings

  ofile: bpy.props.StringProperty(
    name="Output file",
    description="Location of the exported file",
    subtype="FILE_PATH",
    default="",
    )

  separate_files: bpy.props.BoolProperty(
    name="Separate SVG",
    description="Write out separate SVG files",
    default=False,
    )

  svg_position: bpy.props.EnumProperty(
    name="SVG Position",
    description="Control the position of the SVG slice",
    items=[
      ('TL', 'Top left',  'Top left'),
      ('ST', 'Staggered', 'Staggered'),
      ('CT', 'Center',    'Center')
      ],
    default='TL',
    )

  preview: bpy.props.BoolProperty(
    name="Preview mode",
    description="Generates SVG segments instead of polygons, faster but not recommended for laser cut",
    default=True,
    )


# --------------------------------------------------------------------------------

EXPORTED_CLASSES = (
  Slicer_Preferences,
  Slicer_Preferences_Reset,
)
