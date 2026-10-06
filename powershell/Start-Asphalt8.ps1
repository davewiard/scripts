<#
.DESCRIPTION
    Sets the volume for a specific application using SoundVolumeView.
#>

$SoundVolumeViewPath = "C:\Program Files\soundvolumeview-x64"
$processName = "Asphalt8.exe"
$targetVolume = "10"
$delay = 5

$AsphaltPath = Get-AppxPackage *Asphalt* | Select-Object -ExpandProperty InstallLocation

# start the game and go to sleep for 15 seconds while the game starts up
Start-Process -FilePath "$AsphaltPath\$processName"
Start-Sleep -Seconds $delay

while ($true) {
    $GameProcess = Get-Process -Name ([IO.Path]::GetFileNameWithoutExtension($processName)) -ErrorAction SilentlyContinue

    if ($GameProcess) {
        Start-Process -FilePath "$SoundVolumeViewPath\SoundVolumeView.exe" -ArgumentList "/SetVolume", $processName, $targetVolume
        Start-Sleep -Seconds $delay
    } else {
        Exit
    }
}
