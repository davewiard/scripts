<#
.DESCRIPTION
    Script for downloading YouTube audio files.

.PARAMETER url
    The YouTube URL of the video to download audio from.
#>
Param(
    [string]$url = ""
)

$downloadsPath = (New-Object -ComObject Shell.Application).Namespace('shell:Downloads').Self.Path

while ($url -eq "") {
    $url = (Read-Host "YouTube URL").Trim()
}

$ytDlpArgs = @(
    '--format'
    "bv+ba/b"
    '--merge-output-format'
    'mkv'
    '--remux-video'
    'mkv'
    '--output'
    '%(title)s.%(ext)s'
    $url
)

Start-Process `
    -FilePath 'yt-dlp' `
    -ArgumentList $ytDlpArgs `
    -NoNewWindow `
    -Wait `
    -PassThru

$inputFile = Get-ChildItem -File -Filter '*.mkv' |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1 -ExpandProperty Name

# $inputFile  = "video.mkv"
$outputFile = "[Q] $inputFile"

$ffmpegArgs = "-i `"$inputFile`" -map 0:v:0 -map 0:a:0 -c:v copy -af `"volume=-6dB`" -c:a aac -b:a 192k `"$outputFile`""

Start-Process `
    -FilePath 'ffmpeg' `
    -ArgumentList $ffmpegArgs `
    -NoNewWindow `
    -Wait `
    -PassThru

if ($?) {
    Move-Item -Path ".\*.mkv" -Destination $downloadsPath
} else {
    Write-Output "Download failed"
}

$a = Read-Host "Press enter to continue"
