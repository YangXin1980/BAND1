$ErrorActionPreference = "Stop"

$appName = "BAND"
$desktopShortcut = Join-Path ([Environment]::GetFolderPath("DesktopDirectory")) "$appName.lnk"
$startShortcut = Join-Path (Join-Path ([Environment]::GetFolderPath("StartMenu")) "Programs") "$appName.lnk"
$installDir = Join-Path ([Environment]::GetFolderPath("LocalApplicationData")) "Programs\BAND"

Remove-Item -LiteralPath $desktopShortcut -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $startShortcut -Force -ErrorAction SilentlyContinue
if (Test-Path -LiteralPath $installDir) {
    Remove-Item -LiteralPath $installDir -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "Removed $appName shortcuts and program files"
Write-Host "User data is kept under: $([Environment]::GetFolderPath("LocalApplicationData"))\BandChat\data"
