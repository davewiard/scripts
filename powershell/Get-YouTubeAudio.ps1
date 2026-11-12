<#
.DESCRIPTION
    Script for downloading YouTube audio files.

.PARAMETER url
    The YouTube URL of the video to download audio from.
#>
Param(
    [string]$url = ""
)

$outputType = "opus"
$downloadsPath = (New-Object -ComObject Shell.Application).Namespace('shell:Downloads').Self.Path

do {
    $url = (Read-Host "YouTube URL").Trim()
    if ($url -eq "") {
        Exit
    }

    Start-Process -Wait -FilePath "yt-dlp" -ArgumentList            `
        "-x",                                                       `
        "--audio-quality 0",                                        `
        "--audio-format $outputType",                               `
        "--windows-filenames",                                      `
        "$url"

    if ($?) {
        Move-Item -Path ".\*.opus" -Destination $downloadsPath
    } else {
        Write-Output "Download failed"
    }

    $url = ""
} while ($url -eq "")
