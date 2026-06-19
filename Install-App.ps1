param(
    [switch]$NoClose,
    [switch]$SkipWebView2
)

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

$sourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceExePath = Join-Path $sourceDir "BAND.exe"
$webView2SetupPath = Join-Path $sourceDir "MicrosoftEdgeWebview2Setup.exe"
$webView2DownloadUrl = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"
$programsRoot = Join-Path ([Environment]::GetFolderPath("LocalApplicationData")) "Programs"
$installDir = Join-Path $programsRoot "BAND"
$pendingDir = Join-Path $programsRoot "BAND_pending_update"
$exePath = Join-Path $installDir "BAND.exe"
$appName = "BAND"
$desktop = [Environment]::GetFolderPath("DesktopDirectory")
$programs = Join-Path ([Environment]::GetFolderPath("StartMenu")) "Programs"
$files = @(
    "BAND.exe",
    "Microsoft.Web.WebView2.Core.dll",
    "Microsoft.Web.WebView2.WinForms.dll",
    "WebView2Loader.dll",
    "README.md"
)

if (-not (Test-Path -LiteralPath $sourceExePath)) {
    Write-Host "Cannot find BAND.exe. Please extract the whole BAND package first, then run the installer again."
    exit 1
}

function Test-WebView2Runtime {
    $keys = @(
        "HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}",
        "HKCU:\Software\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}",
        "HKLM:\SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
    )

    foreach ($key in $keys) {
        try {
            $value = (Get-ItemProperty -LiteralPath $key -Name "pv" -ErrorAction Stop).pv
            if (-not [string]::IsNullOrWhiteSpace($value) -and $value -ne "0.0.0.0") {
                return $true
            }
        } catch {
        }
    }
    return $false
}

function Copy-WithRetry {
    param(
        [string]$Source,
        [string]$Destination
    )

    for ($attempt = 1; $attempt -le 8; $attempt++) {
        try {
            Copy-Item -LiteralPath $Source -Destination $Destination -Force -ErrorAction Stop
            return
        } catch {
            if ($attempt -eq 8) {
                throw
            }
            Start-Sleep -Milliseconds 500
        }
    }
}

function Copy-AppFiles {
    param([string]$TargetDir)

    New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
    foreach ($file in $files) {
        $source = Join-Path $sourceDir $file
        if (Test-Path -LiteralPath $source) {
            Copy-WithRetry -Source $source -Destination (Join-Path $TargetDir $file)
        }
    }
}

function Escape-PowerShellString {
    param([string]$Value)
    return $Value.Replace('`', '``').Replace('"', '`"')
}

function New-AppShortcut {
    param(
        [string]$ShortcutPath,
        [string]$TargetPath,
        [string]$WorkingDirectory
    )

    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($ShortcutPath)
    $shortcut.TargetPath = $TargetPath
    $shortcut.WorkingDirectory = $WorkingDirectory
    $shortcut.Description = $appName
    $shortcut.IconLocation = "$TargetPath,0"
    $shortcut.Save()
}

function Install-WebView2RuntimeIfNeeded {
    if (Test-WebView2Runtime) {
        return
    }

    Write-Host "Microsoft Edge WebView2 Runtime is missing. Installing it now..."

    $runtimeTempDir = Join-Path $env:TEMP "BAND-WebView2"
    New-Item -ItemType Directory -Force -Path $runtimeTempDir | Out-Null
    $runtimeSetupPath = Join-Path $runtimeTempDir "MicrosoftEdgeWebview2Setup.exe"

    if (Test-Path -LiteralPath $webView2SetupPath) {
        Copy-Item -LiteralPath $webView2SetupPath -Destination $runtimeSetupPath -Force
    } else {
        try {
            Invoke-WebRequest -Uri $webView2DownloadUrl -OutFile $runtimeSetupPath -UseBasicParsing
        } catch {
            Write-Host "Cannot download Microsoft Edge WebView2 Runtime installer."
            Write-Host "Please install it manually from: https://developer.microsoft.com/microsoft-edge/webview2/"
            exit 1
        }
    }

    $process = Start-Process -FilePath $runtimeSetupPath -ArgumentList "/silent", "/install" -Wait -PassThru
    if ($process.ExitCode -ne 0) {
        Write-Host "WebView2 Runtime installer failed. Exit code: $($process.ExitCode)"
        Write-Host "Please install Microsoft Edge WebView2 Runtime manually, then run this installer again."
        exit $process.ExitCode
    }

    Start-Sleep -Seconds 2
    if (-not (Test-WebView2Runtime)) {
        Write-Host "WebView2 Runtime still was not detected after installation."
        Write-Host "Please restart Windows or install Microsoft Edge WebView2 Runtime manually, then open BAND again."
    }
}

function New-PendingUpdateLauncher {
    $finishPs1 = Join-Path $pendingDir "Finish-BAND-Update.ps1"
    $finishCmd = Join-Path $desktop "Finish-BAND-Update.cmd"
    $finishCnCmd = Join-Path $desktop "完成BAND更新.cmd"
    $escapedInstallDir = Escape-PowerShellString $installDir
    $escapedPendingDir = Escape-PowerShellString $pendingDir
    $escapedDesktop = Escape-PowerShellString $desktop
    $escapedPrograms = Escape-PowerShellString $programs

    $finishContent = @"
`$ErrorActionPreference = "Stop"
`$installDir = "$escapedInstallDir"
`$pendingDir = "$escapedPendingDir"
`$desktop = "$escapedDesktop"
`$programs = "$escapedPrograms"
`$exePath = Join-Path `$installDir "BAND.exe"
`$files = @(
    "BAND.exe",
    "Microsoft.Web.WebView2.Core.dll",
    "Microsoft.Web.WebView2.WinForms.dll",
    "WebView2Loader.dll",
    "README.md"
)

`$runningApps = @(Get-Process BAND -ErrorAction SilentlyContinue)
if (`$runningApps.Count -gt 0) {
    Write-Host "BAND is still running. Please close BAND first, then run this file again."
    exit 1
}

New-Item -ItemType Directory -Force -Path `$installDir | Out-Null
foreach (`$file in `$files) {
    `$source = Join-Path `$pendingDir `$file
    if (Test-Path -LiteralPath `$source) {
        Copy-Item -LiteralPath `$source -Destination (Join-Path `$installDir `$file) -Force
    }
}

New-Item -ItemType Directory -Force -Path `$programs | Out-Null
`$shell = New-Object -ComObject WScript.Shell
foreach (`$shortcutPath in @((Join-Path `$desktop "BAND.lnk"), (Join-Path `$programs "BAND.lnk"))) {
    `$shortcut = `$shell.CreateShortcut(`$shortcutPath)
    `$shortcut.TargetPath = `$exePath
    `$shortcut.WorkingDirectory = `$installDir
    `$shortcut.Description = "BAND"
    `$shortcut.IconLocation = "`$exePath,0"
    `$shortcut.Save()
}

Remove-Item -LiteralPath `$pendingDir -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "BAND update completed. You can open BAND from the desktop shortcut now."
"@

    Set-Content -LiteralPath $finishPs1 -Value $finishContent -Encoding UTF8

    $cmdContent = @"
@echo off
setlocal
set "PS=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if exist "%SystemRoot%\Sysnative\WindowsPowerShell\v1.0\powershell.exe" set "PS=%SystemRoot%\Sysnative\WindowsPowerShell\v1.0\powershell.exe"
if not exist "%PS%" set "PS=powershell.exe"
"%PS%" -NoProfile -ExecutionPolicy Bypass -File "$finishPs1"
if errorlevel 1 pause
"@
    Set-Content -LiteralPath $finishCmd -Value $cmdContent -Encoding ASCII
    Set-Content -LiteralPath $finishCnCmd -Value $cmdContent -Encoding ASCII
}

if (-not $SkipWebView2) {
    Install-WebView2RuntimeIfNeeded
} else {
    Write-Host "Skipping WebView2 Runtime check."
}

$runningApps = @(Get-Process BAND -ErrorAction SilentlyContinue)
if ($runningApps.Count -gt 0 -and $NoClose) {
    if (Test-Path -LiteralPath $pendingDir) {
        Remove-Item -LiteralPath $pendingDir -Recurse -Force -ErrorAction SilentlyContinue
    }
    Copy-AppFiles -TargetDir $pendingDir
    New-PendingUpdateLauncher
    Write-Host "BAND is running, so the update was prepared without closing it."
    Write-Host "When you are ready, close BAND and run the desktop file: Finish-BAND-Update.cmd"
    exit 0
}

if ($runningApps.Count -gt 0) {
    foreach ($process in $runningApps) {
        try {
            Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
            [void]$process.WaitForExit(5000)
        } catch {
        }
    }
    Start-Sleep -Milliseconds 700
}

Copy-AppFiles -TargetDir $installDir

New-Item -ItemType Directory -Force -Path $programs | Out-Null
New-AppShortcut -ShortcutPath (Join-Path $desktop "$appName.lnk") -TargetPath $exePath -WorkingDirectory $installDir
New-AppShortcut -ShortcutPath (Join-Path $programs "$appName.lnk") -TargetPath $exePath -WorkingDirectory $installDir

Write-Host "Installed $appName to $installDir"
