# laser_slicer
Laser slicer add-on for Blender.


## Description
The Laser Slicer cuts up a Blender object and exports the slices to SVG files for cutting on a laser cutter or other post-processing.

More details and link to tutorial video can be found at: https://blendscript.blogspot.com/2019/01/blender-28-laser-slicer.html

This project is a fork of the [laser_slicer](https://github.com/rgsouthall/laser_slicer) repo from [Ryan Southall](https://github.com/rgsouthall), thank you so much Ryan !!

The intention of the fork is to:
* Reorganize the code as per my personal preferences
* Add features I find useful for my personal workflow


## Setup
* Either:
    * Download the [zip file of the add-on](https://github.com/clvLabs/laser_slicer/archive/refs/heads/master.zip).
    * Extract it in your `~/.config/blender/<VERSION>/scripts/addons` folder (or equivalent).
* or:
    * Clone this project in your `~/.config/blender/<VERSION>/scripts/addons` folder (or equivalent).
* Open Blender.
* Go to `Edit > Preferences > Add-ons`.
* Refresh the list.
* Activate the `Laser Slicer` add-on.
* A new `Laser` tab will appear in `View3D > Sidebar`.

## Usage
* Select the object you want to slice.
* Activate the side panel with `n`.
* Select the `Laser` tab.
* Configure your material settings.
* Configure your cut settings.
* Click the `Slice the object` button.
* A new `Slices` object will be created.
* If you specified an output file, it will be generated.
