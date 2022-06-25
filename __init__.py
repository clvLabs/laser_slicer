# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

#
# THIS IS A FORKED PROJECT
#
# The original Laser Slicer project's author is Ryan Southall (https://github.com/rgsouthall)
# You can find it at https://github.com/rgsouthall/laser_slicer
#

bl_info = {
     "name": "Laser Slicer",
     "author": "Tony Aguilar",
     "version": (0, 9, 2),
     "blender": (3, 2, 0),
     "location": "3D View > Tools Panel",
     "description": "Makes a series of cross-sections and exports an svg file for laser cutting",
     "warning": "",
     "doc_url": "tba",
     "tracker_url": "https://github.com/clvLabs/laser_slicer/issues",
     "support": "COMMUNITY",
     "category": "Object"}

import bpy
import importlib

from .src import preferences
from .src import panel
from .src import operator
from .src import slicer

ALL_MODULES = [preferences, panel, operator, slicer]
BPY_MODULES = [preferences, panel, operator]

def register():
  for module in ALL_MODULES:
    importlib.reload(module)

  for module in BPY_MODULES:
    for cls in module.EXPORTED_CLASSES:
      bpy.utils.register_class(cls)

def unregister():
  for module in BPY_MODULES:
    for cls in module.EXPORTED_CLASSES:
      bpy.utils.unregister_class(cls)
