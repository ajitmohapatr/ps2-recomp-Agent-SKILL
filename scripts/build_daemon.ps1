<#
.SYNOPSIS
Autonomous build script for PS2xRuntime to be used by LLM agents.
.DESCRIPTION
Invokes MSBuild/CMake via Visual Studio Developer Command Prompt in the background
and streams the output. If a compilation error occurs, the agent can parse it.
.EXAMPLE
.\build_daemon.ps1 -SourceDir ".\ps2xRuntime"
#>

param(
    [string]$SourceDir = ".\ps2xRuntime",
    [string]$BuildType = "Debug"
)

# Hardcoded common vcvars64.bat locations for Visual Studio
$vcvarsPaths = @(
    "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat",
    "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat",
    "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat"
)

$vcvars = $null
foreach ($path in $vcvarsPaths) {
    if (Test-Path $path) {
        $vcvars = $path
        break
    }
}

if (-not $vcvars) {
    Write-Error "[Build-Daemon] ERROR: Could not locate vcvars64.bat. Is Visual Studio 2022 installed?"
    exit 1
}

Write-Host "[Build-Daemon] Compiling $SourceDir using $vcvars ..."
Write-Host "[Build-Daemon] WARNING: Heavy CPU usage incoming. Keep .h modifications to an absolute minimum."

# Execute msbuild via cmd, invoking vcvars first
$cmd = "call `"$vcvars`" && cd /d `"$SourceDir`""

# Check if build directory exists, if not configure it
if (-not (Test-Path "$SourceDir\build")) {
    Write-Host "[Build-Daemon] build/ directory not found. Running CMake configure..."
    $cmd += " && cmake -S . -B build -G `"Visual Studio 17 2022`" -A x64"
}

$cmd += " && cd build && cmake --build . --config $BuildType"

cmd.exe /c $cmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[Build-Daemon] ✅ SUCCESS: Build completed without errors."
}
else {
    Write-Host "`n[Build-Daemon] ❌ ERROR: Build failed. Check the MSVC output above."
}
exit $LASTEXITCODE
