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
		old_palette_image = Image.open(old_palette_path).convert("RGB")
		new_palette_image = Image.open(new_palette_path).convert("RGB")

		old_width, old_height = old_palette_image.size
		new_width, new_height = new_palette_image.size
		input_width, input_height = input_image.size

		if (old_width != new_width) or (old_height != new_height):
			print(f"Warning: '{old_palette_path}' and '{new_palette_path}' have different dimensions. Color mapping might be incorrect.")

		pixels_input = input_image.load()
		pixels_old = old_palette_image.load()
		pixels_new = new_palette_image.load()

		color_map = {}
		color_to_skip_rgb = None
		if isinstance(COLOR_TO_SKIP, str):
			try:
				color_to_skip_rgb = hex_to_rgb(COLOR_TO_SKIP)
			except ValueError:
				print(f"Warning: Invalid hex color string '{COLOR_TO_SKIP}'. Skipping will be disabled for this run.")
				color_to_skip_rgb = None # Ensure it's None to disable skipping

		# Iterate through old_palette using nested loops
		for y_old in range(old_height):
			for x_old in range(old_width):
				old_color = pixels_old[x_old, y_old]

				if COLOR_TO_SKIP is not False and color_to_skip_rgb is not None and old_color == color_to_skip_rgb:
					continue  # Skip this color in old_palette

				if x_old < new_width and y_old < new_height:
					new_color = pixels_new[x_old, y_old]
					color_map[old_color] = new_color

		remapped_image = Image.new("RGB", (input_width, input_height))
		remapped_pixels = remapped_image.load()

		tolerance = 0.01  # 1% tolerance

		for y_input in range(input_height):
			for x_input in range(input_width):
				current_color = pixels_input[x_input, y_input]
				found_match = False
				for old_c, new_c in color_map.items():
					if is_within_tolerance(current_color, old_c, tolerance):
						remapped_pixels[x_input, y_input] = new_c
						found_match = True
						break  # Exit the inner loop once a match is found
				if not found_match:
					remapped_pixels[x_input, y_input] = current_color

		# Move the original file to the backup directory
		base_name = os.path.basename(input_path)
		backup_path = os.path.join(BACKUP_DIRECTORY, base_name)
		shutil.move(input_path, backup_path)

		# Save the remapped image with the original name
		remapped_image.save(input_path)

		print(f"Remapped '{base_name}': a copy was kept at '{backup_path}'.")

	except FileNotFoundError:
		print(f"Error: One or more palette files ('{old_palette_path}', '{new_palette_path}') or the input file '{input_path}' were not found.")
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