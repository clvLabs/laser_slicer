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
      prefs.property_unset('separate_files')
      prefs.property_unset('svg_position')
      prefs.property_unset('cut_thickness')
      prefs.property_unset('accuracy')
      prefs.property_unset('ofile')

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
    soft_max=50,
    step=0.1,
    default=2,
    )

  material_width: bpy.props.FloatProperty(
    name="Width",
    description="Width of the cutting material (mm)",
    min=1,
    soft_max=5000,
    step=10,
    default=450,
    )

  material_height: bpy.props.FloatProperty(
    name="Height",
    description="Height of the cutting material (mm)",
    min=1,
    soft_max=5000,
    step=10,
    default=450,
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
    name="Line color",
    description="Color of the generated SVG line",
    subtype ='COLOR',
    default=[1.0, 0.0, 0.0],
    )

  cut_line_thickness: bpy.props.IntProperty(
    name="Line thickness",
    description="Thickness of the generated SVG line (pixels)",
    min=0,
    soft_max=5,
    default=1,
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

  cut_thickness: bpy.props.FloatProperty(
    name="Cut thickness",
    description="Thickness of the laser cut (mm)",
    min=0,
    soft_max=5,
    default=1,
    )

  accuracy: bpy.props.BoolProperty(
    name="Generate SVG polygons",
    description="Control the speed and accuracy of the slicing",
    default=False,
    )

  # ------------------------------------------------------------------------
  # Slice settings

  ofile: bpy.props.StringProperty(
    name="Output file",
    description="Location of the exported file",
    subtype="FILE_PATH",
    default="",
    )


# --------------------------------------------------------------------------------

EXPORTED_CLASSES = (
  Slicer_Preferences,
  Slicer_Preferences_Reset,
)
