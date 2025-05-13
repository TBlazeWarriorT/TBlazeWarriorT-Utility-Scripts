# Powershell Audio Output Device Toggler
This powershell script will switch between two pre-defined audio output devices in your computer.
It also automatically generates a shortcut that runs it and can be pinned to your taskbar.
# Setup
1. Setup the $device1 and $device2 variables and your Windows output device names to match.
2. (Optional). Place the ps1 file in your Desktop or a "Windows shortcut compatible" folder. After step 3, this will allow the generated shortcut to be activated via CTRL+SHIFT+A by default
3. Run the .ps1 file once to generate the shortcut. You can use `powershell -ExecutionPolicy Bypass -File "./Toggle Audio Output.ps1"` on a CMD Window in the script's directory. Feel free to pin the shortcut to your taskbar.
4. (Optional). If the script is moved, run the script again to automatically update the shortcut, and if pinned, pin it again to update the one in the taskbar.  

![image](https://github.com/user-attachments/assets/64c25728-ba27-4d47-a88f-5d9e3c946062)
