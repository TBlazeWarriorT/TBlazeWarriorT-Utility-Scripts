"""
Image Color (Palette) Remapping Script

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
"""

# --- Customizable Variables ---
BACKUP_DIRECTORY = "./_recolor_backups/"
COLOR_TO_SKIP = False  # False to skip no colors, or a hex color string (e.g., "#FF00FF")
SUPPORTED_EXTENSIONS = (".bmp", ".png", ".jpg", ".jpeg", ".tiff") # Add other Pillow-supported extensions if needed
# --- End Customizable Variables ---

from PIL import Image
import sys
import os
import shutil

def hex_to_rgb(hex_color): # Converts a hex color string (e.g., '#FF00FF') to an RGB tuple (e.g., (255, 0, 255)).
	hex_color = hex_color.lstrip('#')
	return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def is_within_tolerance(color1, color2, tolerance): # Checks if two RGB colors are within the specified tolerance (percentage).
	for c1, c2 in zip(color1, color2):
		if not (c2 * (1 - tolerance) <= c1 <= c2 * (1 + tolerance)):
			return False
	return True

def remap_colors_and_backup(input_path, old_palette_path="palette_old.bmp", new_palette_path="palette_new.bmp"):
	try:
		# Create the backup directory if it doesn't exist
		os.makedirs(BACKUP_DIRECTORY, exist_ok=True)

		input_image = Image.open(input_path).convert("RGB")
		input_width, input_height = input_image.size
		pixels_input = input_image.load()

		inverted_image = Image.new("RGB", (input_width, input_height))
		inverted_pixels = inverted_image.load()

		for y in range(input_height):
			for x in range(input_width):
				r, g, b = pixels_input[x, y]
				inverted_pixels[x, y] = (255 - r, 255 - g, 255 - b)

		# Move the original file to the backup directory
		base_name = os.path.basename(input_path)
		backup_path = os.path.join(BACKUP_DIRECTORY, base_name)
		#shutil.move(input_path, backup_path)

		# Save the inverted image with the original name
		inverted_image.save(input_path)

		print(f"Inverted '{base_name}': original kept at '{backup_path}'.")

	except FileNotFoundError:
		print(f"Error: Input file '{input_path}' was not found.")
	except Exception as e:
		print(f"An error occurred: {e}")

def process_path(path): # Processes a single file path, checking if it's an image and then remapping colors.
	if os.path.isfile(path) and path.lower().endswith(SUPPORTED_EXTENSIONS):
		print(f"Processing file: {path}")
		remap_colors_and_backup(path)
	elif os.path.isdir(path):
		recursive = input(f"Include all subfolders in '{path}'? (Y/N): ").strip().lower()
		if recursive == 'y':
			for root, _, files in os.walk(path):
				for name in files:
					if name.lower().endswith(SUPPORTED_EXTENSIONS):
						file_path = os.path.join(root, name)
						print(f"Processing file: {file_path}")
						remap_colors_and_backup(file_path)
		elif recursive == 'n':
			for name in os.listdir(path):
				if name.lower().endswith(SUPPORTED_EXTENSIONS):
					file_path = os.path.join(path, name)
					print(f"Processing file: {file_path}")
					remap_colors_and_backup(file_path)
		else:
			print("Invalid input. Skipping folder.")
	else:
		print(f"Skipping invalid path: {path}")

if __name__ == "__main__":
	if len(sys.argv) > 1:
		paths_to_process = sys.argv[1:]
		if len(paths_to_process) == 1 and os.path.isdir(paths_to_process[0]):
			process_path(paths_to_process[0])
		else:
			for path in paths_to_process:
				process_path(path)
	else:
		print("Please drag and drop one or more image files onto this script,")
		print("or run it from the command line with file or folder paths.")

	input("Press Enter to exit.")