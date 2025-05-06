# PowershellAudioOutputToggler
3 files that can allow you to change your audio output device in one click after setup.
This shortcut + bat file + powershell script bundle will run a ps script that can be pinned to your taskbar and will switch between two pre-defined audio output devices in your computer.
# Setup
1. Make sure the shortcut points to the .bat file properly in the shortcut properties
2. Make sure the .bat file points to the .ps1 script properly
3. Make sure the .ps1 script matches your device names. By default, it will look for (and require) a device with Speakers on the name (e.g. "Speakers (Realtek(R) Audio)" is valid) and one with Headset on the name.
Either rename your device to that, or change the variable in the script.
4. Pin the script to your taskbar and click

![image](https://github.com/user-attachments/assets/64c25728-ba27-4d47-a88f-5d9e3c946062)
