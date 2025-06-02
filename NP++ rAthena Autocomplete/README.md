# rAthena Notepad++ Auto-complete

### Functionality:
**A**) Included .xml file: just install below and you'll get autocomplete.
It includes all script_commands and global functions with documentation (if available), and script_constants without documentation.
[ Insert image here ]

**B**) Included Python file: re-generates the XML file based on the latest main branch of the rAthena GitHub. May fetch and cache new data every 10 mins.

**C**) Not included User Defined Language and Theme: It's being worked on. For now, see below.

### Installation:
1. Get a rAthena User Defined Language.
1.1 - Notepadpp-rAthena-syntax-highlight.xml from https://github.com/Sehrentos/rAthena-syntax-highlight/tree/master should be compatible with this. I'll probably make an updated fork of it for this later
2. Place rathena.xml inside ".../Notepad++/autoCompletion/rathena.xml"
3. Restart Notepad++

### Updating autocomplete to latest rAthena (optional):
1. Download and run the Python script.