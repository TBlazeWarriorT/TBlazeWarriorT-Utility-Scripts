import re, os, requests, time
import xml.sax.saxutils

PRINT_COMMANDS = ""
PRINT_FUNCTIONS = ""
COUNT_CONSTANTS = 0
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(SCRIPT_DIR, "GitHubCache")
CACHE_DURATION = 600  # 10 minutes in seconds

def get_github_file_content(file_path):
	url = f"https://raw.githubusercontent.com/rathena/rathena/master/{file_path}"
	
	# Create cache directory if it doesn't exist
	os.makedirs(CACHE_DIR, exist_ok=True)

	# Generate a cache file path based on the URL
	cache_file_name = f"{file_path.replace('/', '_')}.cache"
	cache_file_path = os.path.join(CACHE_DIR, cache_file_name)

	# Check if a valid cached file exists
	if os.path.exists(cache_file_path):
		last_modified_time = os.path.getmtime(cache_file_path)
		if (time.time() - last_modified_time) < CACHE_DURATION:
			print(f"Loading from cache: {file_path}")
			with open(cache_file_path, 'r', encoding='utf-8', errors='ignore') as f:
				return f.read()

	# If cache is not valid, fetch from GitHub
	print(f"Fetching from GitHub: {file_path}")
	try:
		response = requests.get(url)
		response.raise_for_status()  # Raise an exception for bad status codes
		content = response.text

		# Write to cache
		with open(cache_file_path, 'w', encoding='utf-8') as f:
			f.write(content)

		return content
	except requests.exceptions.RequestException as e:
		print(f"Error fetching file {url}: {e}")
		return None

# --- Helpers ---
def escape_xml(s):
	return xml.sax.saxutils.escape(s).replace('"', '&quot;')

def is_meaningful_line(s):
	return len(re.findall(r'[A-Za-z0-9]', s)) >= 4

# --- Script Commands Parser ---
def parse_script_commands(lines):
	entries = []
	i = 0
	while i < len(lines):
		match = re.match(r'^\*(\w+)\s*(.*)', lines[i]) # Look for *command
		if not match:
			i += 1
			continue

		aliases = [(match.group(1), match.group(2).strip())]
		j = i + 1
		while j < len(lines):
			alias_match = re.match(r'^\*(\w+\d?)\s*(.*)', lines[j].strip())
			if alias_match:
				aliases.append((alias_match.group(1), alias_match.group(2).strip()))
				j += 1
			elif lines[j].strip():
				break
			else:
				j += 1

		description_lines = []
		desc_limit = 4
		for k in range(j, len(lines)):
			if re.match(r'^\*(\w+\d?)', lines[k].strip()):
				break
			text = lines[k].strip()
			if not is_meaningful_line(text):
				continue
			description_lines.append(text)
			if len(description_lines) == desc_limit:
				if k + 1 < len(lines) and is_meaningful_line(lines[k + 1]):
					description_lines[-1] += " [...]"
				break
		description = escape_xml("\n" + "\n".join(description_lines))

		for name, params in aliases:
			if name == "Name": continue
			global PRINT_COMMANDS
			PRINT_COMMANDS += "*" + name + "\n"
			param_str = re.sub(r"^\(|\)$", "", params.strip()).rstrip(';')
			param_str = escape_xml(param_str)
			entries.append((name.lower(), f'''\
		<KeyWord name="{name}" func="yes">
			<Overload retVal="*" descr="{description}">
				<Param name="{param_str}" />
			</Overload>
		</KeyWord>'''))
		i = max(j, i + 1)
	return entries

# --- Global Functions Parser ---
def parse_global_functions(lines):
	entries = []
	last_desc = None
	i = 0
	while i < len(lines):
		line = lines[i]
		if line.startswith("///"):
			# Capture description block
			desc_lines = []
			j = i + 1
			while j < len(lines):
				textline = lines[j].strip()
				if not textline.startswith("//"):
					break
				if textline.startswith("// --") or textline.startswith("// callfunc") or "Examples" in textline:
					break
				txt = textline[2:].strip()
				if is_meaningful_line(txt):
					desc_lines.append(txt)
				if len(desc_lines) == 4:
					if j + 1 < len(lines) and is_meaningful_line(lines[j + 1]):
						desc_lines[-1] += " [...]"
					break
				j += 1
			last_desc = desc_lines
			i = j
			continue

		# Look for any function definition
		func_match = re.match(r'^function	script	([^	]+)	\{', line)
		if func_match:
			name = func_match.group(1)
			global PRINT_FUNCTIONS
			PRINT_FUNCTIONS += name + "()\n"
			# Determine return type
			retVal = "Global Function" if name.startswith("F_") else "*"
			# Build description if available
			description = ""
			if last_desc:
				description = escape_xml("\n" + "\n".join(last_desc))
			entries.append((name.lower(), f'''\
		<KeyWord name="{name}" func="yes">
			<Overload retVal="{retVal}" descr="{description}">
				<Param name="" />
			</Overload>
		</KeyWord>'''))
		# Continue scanning
		i += 1
	return entries

# --- Script Constants Parser ---
def parse_script_constants(lines):
	entries = ""
	i = 0
	while i < len(lines):
		line = lines[i]
		match2 = re.match(r'\s*export_constant2\s?\("(\w+)",', line)
		match1 = re.match(r'\s*export_constant\s?\((\w+)\)', line)
		global COUNT_CONSTANTS
		if match2:
			name = match2.group(1)
			entries += f'\n\t\t<KeyWord name="{name}" />'
			COUNT_CONSTANTS += 1
		elif match1:
			name = match1.group(1)
			entries += f'\n\t\t<KeyWord name="{name}" />'
			COUNT_CONSTANTS += 1
		i += 1
	return entries

# --- Request, Cache and Generate ---
doc_path = r"doc/script_commands.txt"
global_path = r"npc/other/Global_Functions.txt"
constants_path = r"src/map/script_constants.hpp"

doc_content = get_github_file_content(doc_path)
global_content = get_github_file_content(global_path)
constants_content = get_github_file_content(constants_path)

script_entries = parse_script_commands(doc_content.splitlines())
global_entries = parse_global_functions(global_content.splitlines())
constant_entries = parse_script_constants(constants_content.splitlines())

xml_output = '''<?xml version="1.0" encoding="Windows-1252" ?>
<NotepadPlus>
	<AutoComplete language="rAthena">
		<Environment ignoreCase="no" startFunc="(" stopFunc=")" paramSeparator="," terminal=";" />
'''
xml_output += "\n".join(e[1] for e in sorted(script_entries + global_entries, key=lambda x: x[0]))
xml_output += constant_entries
xml_output += '''
	</AutoComplete>
</NotepadPlus>'''

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rathena.xml')
with open(output_path, 'w', encoding='utf-8') as f:
	f.write(xml_output)

print(f'Found Commands:\n{PRINT_COMMANDS}')
print()
print(f'Found Functions:\n{PRINT_FUNCTIONS}')
print()
print(f"Autocomplete XML generated successfully and saved to '{output_path}'")
print(f"Total script commands parsed: {len(script_entries)}")
print(f"Total global functions parsed: {len(global_entries)}")
print(f"Total script constants parsed: {COUNT_CONSTANTS}")
