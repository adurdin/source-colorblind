# Source-Colorblind

Colorblindness simulation for Source engine mappers.

Created by Andrew Durdin, <me@andy.durdin.net>.

## Overview

Three `.raw` color tables for use with the `color_correction` entity are
provided, that simulate the most common forms of colorblindness:

  * Deuteranomaly/deuteranopia (red/green), which affects about 5% of men.
  * Protanamoaly/protanopia (red/green), which affects about 2.5% of men.
  * Tritanomaly/tritanopia (blue/yellow), which affects less than 1% of men
    and women.

Using these color tables allows you to test the readability of your maps for
colorblind and partially colorblind people. A prefab and suggested keybinds
are provided for easy use within a map.

The simulation is based on the method described in [Digital Video Colourmaps
for Checking the Legibility of Displays by Dichromats][1] by Françoise Viénot,
Hans Brettel, and John D. Mollon.

Included in this package is a Python script for converting between `.raw`
color tables and `.tga` image files.

[1]: http://vision.psychol.cam.ac.uk/jdmollon/papers/colourmaps.pdf


## Installation

### Install the color tables:

1. Copy `protanopia.raw`, `deuteranopia.raw`, and `tritanopia.raw` into the
game directory, *Steam Folder*`\steamapps\`*account_name*`\`*game
name*`\`*game short name*`


### Create the prefab:

1. Open `colorblind_filters.vmf` in Hammer.
2. Select all entities.
3. Choose *Tools, Create Prefab*.
4. Enter `colorblind_filters` for the name.

### Setup keybinds::

1. Edit `autoexec.cfg` for the game in a text editor (Notepad will do). This
file is located in *Steam Folder*`\steamapps\`*account_name*`\`*game
name*`\`*game short name*`\cfg\autoexec.cfg`. Create the file if it doesn't
exist.

2. Add the following lines. You can replace F7 with another key if you prefer.

        alias "cycle_colorblind" "ent_fire relay_colorblind trigger"
        bind "F7" "cycle_colorblind"


## Usage

1. Use the entity tool to insert the `colorblind_filters` entity in test
builds of your map.

2. Load the map in the game, and press F7 to cycle between the different
filters.


## Using the Python script to convert other color tables

The Python script `colortable.py` allows you to convert a color table to a `.tga` image like this:

    python colortable.py my-color-table.raw my-color-table.tga

Or to convert such a `.tga` image back to a color table like this:

    python colortable.py another-color-table.tga another-color-table.raw

You must have Python 2.6 or greater installed, and run these commands from the shell or terminal.


## Copyright licence

Copyright (C) 2011 by Andrew Durdin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
