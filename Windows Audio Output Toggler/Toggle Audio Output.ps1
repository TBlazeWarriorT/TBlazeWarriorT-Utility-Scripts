# Define device keywords (adjust to match your system)
$device1 = "Headset"
$device2 = "Speakers"

# Get current playback audio device
$CurrentAudio = Get-AudioDevice -Playback

# Get current device name
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