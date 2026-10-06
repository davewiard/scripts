<#
.DESCRIPTION
    Starts the Asphalt 8 start-up script with administrator privileges. This is
    needed to allow the script to launch the WindwsApp executable for the game.
#>
Start-Process -Verb RunAs -FilePath "powershell.exe" -ArgumentList "C:\Projects\scripts\powershell\Start-Asphalt8.ps1"
