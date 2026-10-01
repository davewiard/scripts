Param(
    [string]$searchFor = ""
)

While ($searchFor.length -lt 3) {
    Write-Output "Search string is too short. Please specify at least 4 characters."
    $searchFor = Read-Host "New search pattern"
}

Write-Output $searchFor

Get-AppxPackage | Where-Object Name -like $searchFor | Format-Table

Write-Output "Please specify package name to uninstall."
$packageName = Read-Host "Package name"

$package = Get-AppxPackage | Where-Object Name -EQ $packageName
$package | Format-Table

$defaultValue = "Y"
$prompt = Read-Host "Uninstall this package? [$($defaultValue)]"
$prompt = ($defaultValue,$prompt)[[bool]$prompt]

if ($prompt -eq $defaultValue) {
    Write-Output "Uninstalling $packageName"
    Get-AppxPackage | Where-Object Name -EQ $packageName | Remove-AppxPackage
} else {
    Write-Output "Not uninstalling $packageName"
}
