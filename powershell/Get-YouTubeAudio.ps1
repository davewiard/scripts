Param(
    [string]$uri = ""
)

$outputType = "opus"
$downloadsPath = (New-Object -ComObject Shell.Application).Namespace('shell:Downloads').Self.Path

Start-Process -Wait -FilePath "yt-dlp" -ArgumentList            `
    "-x",                                                       `
    "--audio-quality 0",                                        `
    "--audio-format $outputType",                               `
    "--windows-filenames",                                      `
    "$uri"

if ($?) {
    Move-Item -Path ".\*.opus" -Destination $downloadsPath
} else {
    Write-Output "Download failed"
}

#$a = Read-Host "Press enter to continue"

