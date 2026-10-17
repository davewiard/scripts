[CmdletBinding()]
Param(
    [Parameter(Mandatory=$true)]
    [string]$AppName
)

$ScriptPath = "C:\Projects\scripts\powershell\Start-AppWithVolumeControlled.ps1"

switch ($AppName) {
    "Asphalt8" {
        Start-Process -Verb RunAs -FilePath "powershell.exe" -ArgumentList $ScriptPath, "$AppName"
    }
    "foobar2000" {
        Start-Process -NoNewWindow -FilePath "powershell.exe" -ArgumentList $ScriptPath, "$AppName"
    }
}
