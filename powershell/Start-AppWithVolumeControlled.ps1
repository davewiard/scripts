<#
.DESCRIPTION
    Starts an application with the volume controlled by SoundVolumeView.
#>

[CmdletBinding()]
Param(
    [Parameter(Mandatory=$true)]
    [string]$AppName,

    [Parameter(Mandatory=$false)]
    [string]$TargetVolume = "10"
)

$SoundVolumeViewExePath = "C:\Program Files\soundvolumeview-x64\SoundVolumeView.exe"
$PollingDelay = 5

switch ($AppName) {
    "Asphalt8" {
        $ProcessPath = Get-AppxPackage *Asphalt* | Select-Object -ExpandProperty InstallLocation
        $processName = "Asphalt8.exe"
        Write-Host "Starting Asphalt8..."
        Write-Host "Process path: $ProcessPath"
        Write-Host "processName: $processName"
    }
    "foobar2000" {
        $ProcessPath = "C:\Program Files\foobar2000"
        $processName = "foobar2000.exe"
    }
}

# start the game and go to sleep for 15 seconds while the game starts up
Start-Process -FilePath "$ProcessPath\$processName"
Start-Sleep -Seconds $PollingDelay

while ($true) {
    $Process = Get-Process -Name ([IO.Path]::GetFileNameWithoutExtension($processName)) -ErrorAction SilentlyContinue

    if ($Process) {
        Start-Process -FilePath "$SoundVolumeViewExePath" -ArgumentList "/SetVolume", $processName, $TargetVolume
        Start-Sleep -Seconds $PollingDelay
    } else {
        Exit
    }
}
