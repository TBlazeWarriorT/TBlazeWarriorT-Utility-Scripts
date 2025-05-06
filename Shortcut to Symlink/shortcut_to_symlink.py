import sys
import os
import subprocess
from pylnk3 import parse
from colorama import Fore, Style, init
from send2trash import send2trash

# Initialize colorama for Windows compatibility
init(autoreset=True)

def create_symlink_from_shortcut(lnk_path):
	"""
	Creates a symbolic link in the same directory as the .lnk file,
	with the same name as the target directory.
	Then asks to move original shortcut to Recycle Bin.
	"""
	try:
		lnk_file = parse(lnk_path)
		target_path = _get_target_path(lnk_file)
		if not target_path:
			print(Fore.YELLOW + f"Warning: Could not determine target path from '{os.path.basename(lnk_path)}'." + Style.RESET_ALL)
			return

		lnk_dir, lnk_filename = os.path.split(lnk_path)
		target_name = os.path.basename(target_path)  # Extract the name of the target (file or folder)
		symlink_path = os.path.join(lnk_dir, target_name)

		print("Creating symbolic link:")
		print(f"  From: {Fore.CYAN + target_path + Style.RESET_ALL}")
		print(f"  To:   {Fore.CYAN + symlink_path + Style.RESET_ALL}")
		print()
		confirm = input("Proceed? (Y/N): ").lower()

		if confirm not in ('yes', 'y'):
			print("Symbolic link creation cancelled.")
			return

		symlink_exists = os.path.exists(symlink_path)
		if symlink_exists:
			print(Fore.RED + "Error: Symbolic link with that name already exists." + Style.RESET_ALL)

		success = _create_symlink(target_path, symlink_path)

		if success:
			print(Fore.GREEN + f"Symbolic link created successfully as '{target_name}'!" + Style.RESET_ALL)
		elif not symlink_exists:
			print(Fore.RED + "Error creating symbolic link." + Style.RESET_ALL)

		if symlink_exists or success:
			print()
			delete = input(f"Move '{Fore.CYAN + lnk_filename + Style.RESET_ALL}' to Recycle Bin? (Y/N): ").lower() if os.name == 'nt' else input(f"Delete shortcut '{lnk_filename}'? (Y/N): ").lower()
			if delete in ('yes', 'y'):
				_delete_shortcut(lnk_path)
			else:
				print("Shortcut not moved/deleted.")

	except FileNotFoundError:
		print(Fore.RED + f"Error: Shortcut file not found at '{lnk_path}'" + Style.RESET_ALL)
	except Exception as e:
		print(Fore.RED + f"An unexpected error occurred: {e}" + Style.RESET_ALL)

def _get_target_path(lnk_file):
	if hasattr(lnk_file, 'link_info'):
		if hasattr(lnk_file.link_info, 'local_base_path'):
			return lnk_file.link_info.local_base_path
		elif hasattr(lnk_file.link_info, 'common_path_suffix'):
			return lnk_file.link_info.common_path_suffix
		elif hasattr(lnk_file.link_info, 'network_share_info'):
			if hasattr(lnk_file.link_info.network_share_info, 'remote_path'):
				return lnk_file.link_info.network_share_info.remote_path
	elif hasattr(lnk_file, 'relative_path'):
		return lnk_file.relative_path
	elif hasattr(lnk_file, 'path'):
		return lnk_file.path
	return None

def _create_symlink(target, link):
	if os.name == 'nt':  # Windows
		command = ['mklink']
		if os.path.isdir(target):
			command.extend(['/D', link, target])
		else:
			command.extend([link, target])
		result = subprocess.run(command, capture_output=True, text=True, shell=True)
		return "symbolic link created" in result.stdout.lower() or "junction created" in result.stdout.lower()
	elif os.name == 'posix':  # macOS, Linux
		try:
			os.symlink(target, link)
			return True
		except OSError:
			return False
	else:
		print(Fore.YELLOW + "Warning: Operating system not fully supported." + Style.RESET_ALL)
		return False

def _delete_shortcut(path):
	lnk_filename = os.path.basename(path)
	if os.name == 'nt':
		try:
			send2trash(path)
			print(Fore.GREEN + f"Moved to Recycle Bin." + Style.RESET_ALL)
		except OSError as e:
			print(Fore.RED + f"Error moving shortcut to Recycle Bin: {e}" + Style.RESET_ALL)
	elif os.name == 'posix':
		try:
			os.remove(path)
			print(Fore.GREEN + f"Deleted shortcut '{lnk_filename}'." + Style.RESET_ALL)
		except OSError as e:
			print(Fore.RED + f"Error deleting shortcut: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
	if len(sys.argv) == 2:
		lnk_file_path = sys.argv[1]
		create_symlink_from_shortcut(lnk_file_path)
	else:
		print("Usage: python lnk_to_symlink.py <path_to_shortcut.lnk>")
		print("You can also drag and drop the .lnk file onto the script.")
	input("Press ENTER to EXIT")
