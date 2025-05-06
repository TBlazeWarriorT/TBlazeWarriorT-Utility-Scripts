# Image Color (Palette) Remapping Script

Functionality:
This script replaces specific colors on images with new ones, using old and new color palette files, with bulk compatibility and safety features.
'palette_old.bmp' must contain the old colors to be replaced, and 'palette_new.bmp' must contain the new corresponding colors to be applied.
The color mapping is determined by pixel-by-pixel correspondence between the palette files.
Modified images will have their original versions backed up in a './_recolor_backups' folder.

Requirements:
1. Must be run with Python 3.
2. './palette_old.bmp' and './palette_new.bmp' must exist and have the same size (in the same directory as this script).

Usage methods:
1. Drag and drop one or more image files (.bmp, .png, .jpg, etc. - Pillow supported formats) on this script.
2. Provide one or more image file paths as command-line arguments: py <script_path> <file_path_1> {<file_path_2>?} ...
3. Provide a single folder path as a command-line argument: py <script_path> <folder_path>. The script will then ask if it should process files recursively.

Additional configuration:
The "Customizable Variables" section below can be modified for extra flexibility.
