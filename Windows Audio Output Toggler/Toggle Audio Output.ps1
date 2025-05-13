# Define device keywords (adjust to match your system)
$device1 = "Headset"
$device2 = "Speakers"

# Create or update the shortcut in a pinnable way
$WshShell = New-Object -ComObject WScript.Shell
$shortcutPath = Join-Path $PSScriptRoot 'Toggle Audio Output.lnk'
$shortcut = $WshShell.CreateShortcut($shortcutPath)
# Use powershell.exe directly (needed for pinning)
$shortcut.TargetPath = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
$shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$PSScriptRoot\Toggle Audio Output.ps1`""
# Set characteristics
$shortcut.IconLocation = "shell32.dll,168"
$shortcut.WindowStyle = 7
$shortcut.Hotkey = "CTRL+ALT+A"
$shortcut.WorkingDirectory = "C:\"
$shortcut.Description = "Toggle Audio Output"
$shortcut.Save()

# Get current playback audio device
$CurrentAudio = Get-AudioDevice -Playback
$CurrentDeviceName = $CurrentAudio.Name

# Function to switch audio device based on keyword
function Set-AudioDeviceByKeyword {
  param(
    [string] $ActiveDeviceKeyword,
    [string] $InactiveDeviceKeyword
  )

  # Get list of available audio devices
  $Devices = Get-AudioDevice -List

  # Find devices matching keywords
  $ActiveDevice = $Devices | Where-Object Name -like "*$ActiveDeviceKeyword*"
  $InactiveDevice = $Devices | Where-Object Name -like "*$InactiveDeviceKeyword*"

  # Check if devices were found
  if (-not $ActiveDevice -or -not $InactiveDevice) {
    Write-Warning "Could not find devices for keywords '$ActiveDeviceKeyword' and '$InactiveDeviceKeyword'."
    return
  }

  # Determine if switch is needed
  if ($CurrentDeviceName -like "*$ActiveDeviceKeyword*") {
    # Set inactive device as default
    $InactiveDevice | Set-AudioDevice
  } else {
    # Set active device as default
    $ActiveDevice | Set-AudioDevice
  }

  # Write success message
  Write-Output "Audio device switched successfully."
}

# Call function to switch device
Set-AudioDeviceByKeyword -ActiveDeviceKeyword $device1 -InactiveDeviceKeyword $device2