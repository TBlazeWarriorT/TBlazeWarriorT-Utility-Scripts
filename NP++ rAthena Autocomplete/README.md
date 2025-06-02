# rAthena Notepad++ Auto-complete

### Functionality:
- **TL;DR**: This includes a very powerful auto-complete that can be auto-updated, that depends on a partially included User Defined Language.
- **A**) Included .xml file: just install below and you'll get autocomplete.
It includes all script_commands and global functions with documentation (if available), and script_constants without documentation.
![image](https://github.com/user-attachments/assets/c660a6b9-0daa-4743-b4fd-0633b96836ea)
![image](https://github.com/user-attachments/assets/372e61c5-56f5-4abf-a3e3-6d1f0ca30b2f)


- **B**) Included Python file: re-generates the XML file based on the latest main branch of the rAthena GitHub. May fetch and cache new data every 10 mins.

- **C**) Not included User Defined Language and Theme: It's being worked on. For now, see below.
![image](https://github.com/user-attachments/assets/9ecfcd8f-fd09-4378-862c-86a9538dbff4)


### Installation:
- **1**. Get a rAthena User Defined Language setup (a) existing one, stable / b) included one, not polished).  
  - **1a**. `Notepadpp-rAthena-syntax-highlight.xml` from https://github.com/Sehrentos/rAthena-syntax-highlight/tree/master should be compatible with this. I'll probably make an updated fork of it for this later  
  - **1b**. You can also try to replace your NP++ UDL file in your `%appData%/Roaming` with the User Defined Language file inside the other folder in this repo, it's a heavily modified and already installed version of the above.  
I'm lazy to make a proper importer rn, and the file might not be final.  
- **2**. Place place the /autoCompletion/ folder from this repo inside your /Notepad++/ folder  
- **3**. Restart Notepad++  
  - **3.1**. Enable rAthena language on a file. Make sure auto-complete stuff are enabled in settings. Start typing. To see hints, you'll need to open parenthesis '(', and can press CTRL+SHIFT+SPACE by default to force the tooltip to reopen.  

### Updating autocomplete to latest rAthena (optional):
- 1. Download and run the Python script.
