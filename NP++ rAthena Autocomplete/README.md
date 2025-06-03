# rAthena Notepad++ Auto-complete

### Functionality:  
- **TL;DR**: This includes a very powerful auto-complete and a highlighter for rAthena.  
It includes all script_commands and global functions with documentation (if available), and script_constants without documentation.

- **A) Syntax Highlighting**:  
![image](https://github.com/user-attachments/assets/9ecfcd8f-fd09-4378-862c-86a9538dbff4)

- **B) AutoComplete**:  
![image](https://github.com/user-attachments/assets/c660a6b9-0daa-4743-b4fd-0633b96836ea)
![image](https://github.com/user-attachments/assets/372e61c5-56f5-4abf-a3e3-6d1f0ca30b2f)

- **C) Auto-Update**:
The auto-completion file can be automatically updated by simply running a script. Highlight file currently does not auto-update, but it's easy to manually/semi-auto update if you know Python.

### Installation:
- **Optional Step**: Read the next section to update.
- **Step 1 (A)**: `Language > User Defined Language > Define your language... > Import > rathena_importme.xml`
- **Step 2 (B)**: Step 1 is required for this. Place place the `/autoCompletion/` folder from this repo inside your `/Notepad++/` folder
- **Step 3**: Restart Notepad++  
- **Step 4 (using it)**: Enable rAthena language on a file. Make sure auto-complete stuff are enabled in settings. Start typing. To see hints, you'll need to open parenthesis '(', and can press CTRL+SHIFT+SPACE by default to force the tooltip to reopen.  

### Updating autocomplete to latest rAthena (optional):
- **Step 1 (C)**: Download and run the Python script.  
  - It re-generates the XML file based on the latest main branch of the rAthena GitHub. May fetch and cache new data every 10 mins.

### Personal Tip:
You can use .cpp files for scripts instead of .txt, for example. Or you could call them .rat files, I guess.
If you do so, it's easier to spot rAthena files, and to set defaults on your text editor for them. This can help prevent encoding issues too.
If you do, you can go to `Language > User Defined Language > Define your language... > rAthena > Ext.:` and add `cpp rat` to that list or whatever you want.

### Credits:
The included Syntax Highlighting file is a heavily modified version of [Sehrentos' rAthena Syntax Highlight](https://github.com/Sehrentos/rAthena-syntax-highlight/tree/master)
