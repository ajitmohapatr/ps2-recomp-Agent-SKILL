<#
.SYNOPSIS
Autonomous build script for PS2xRuntime to be used by LLM agents.
.DESCRIPTION
Invokes CMake + Clang-CL + Ninja via Visual Studio Developer Command Prompt.
REFUSES to compile with vanilla MSVC — Clang+Ninja are MANDATORY.

.EXAMPLE
.\build_daemon.ps1 -SourceDir "C:\Users\Joe\Desktop\ps2xRuntime"
.\build_daemon.ps1 -SourceDir ".\ps2xRuntime" -BuildType Release
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$SourceDir,
    [string]$BuildType = "Debug"
)

# ── Locate vcvars64.bat (dynamic — supports ANY VS install location) ──
$vcvars = $null

# Method 1: vswhere.exe (works even if VS is on D:\ or custom paths)
$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
if (Test-Path $vswhere) {
    $vsPath = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath 2>$null
    if ($vsPath) {
        $candidate = Join-Path $vsPath "VC\Auxiliary\Build\vcvars64.bat"
        if (Test-Path $candidate) {
            $vcvars = $candidate
        }
    }
}

# Method 2: Fallback to standard paths
if (-not $vcvars) {
    $fallbackPaths = @(
        "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat",
        "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat",
        "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat"
    )
    foreach ($path in $fallbackPaths) {
        if (Test-Path $path) {
            $vcvars = $path
            break
        }
    }
}

if (-not $vcvars) {
    Write-Error "[Build-Daemon] ERROR: Could not locate vcvars64.bat. Is Visual Studio 2022 with C++ workload installed?"
    exit 1
}

# ── MANDATORY: Verify Clang-CL + Ninja ──────────────────────────────
$hasNinja = $null -ne (Get-Command ninja -ErrorAction SilentlyContinue)
$hasClang = $null -ne (Get-Command clang-cl -ErrorAction SilentlyContinue)

if (-not $hasClang -or -not $hasNinja) {
    Write-Error "[Build-Daemon] ❌ FATAL: Clang-CL and Ninja are MANDATORY for PS2Recomp builds."
    Write-Host ""
    if (-not $hasClang) {
        Write-Host "[Build-Daemon] MISSING: clang-cl"
        Write-Host "  → Open Visual Studio Installer → Individual Components → enable 'C++ Clang Compiler for Windows'"
    }
    if (-not $hasNinja) {
        Write-Host "[Build-Daemon] MISSING: ninja"
        Write-Host "  → Open Visual Studio Installer → Individual Components → enable 'C++ CMake tools for Windows'"
    }
    Write-Host ""
    Write-Host "[Build-Daemon] After installing, restart your terminal and re-run this script."
    Write-Host "[Build-Daemon] Vanilla MSVC takes 25+ hours for 29,000 files. Clang+Ninja does it in ~1 hour."
    exit 1
}

Write-Host "[Build-Daemon] ⚡ TURBO MODE: Clang-CL + Ninja confirmed."
Write-Host "[Build-Daemon] Compiling $SourceDir ..."
Write-Host "[Build-Daemon] WARNING: Heavy CPU usage incoming. Keep .h modifications to an absolute minimum."

# ── Build ────────────────────────────────────────────────────────────
$cmd = "call `"$vcvars`" && cd /d `"$SourceDir`""

if (-not (Test-Path "$SourceDir\build")) {
    Write-Host "[Build-Daemon] build/ directory not found. Running CMake configure..."
    $cmd += " && cmake -S . -B build -G `"Ninja`" -DCMAKE_C_COMPILER=clang-cl -DCMAKE_CXX_COMPILER=clang-cl -DCMAKE_BUILD_TYPE=$BuildType"
}

# Smart thread count: leave 2 cores free to prevent system freeze
$threads = [Math]::Max(1, [Environment]::ProcessorCount - 2)
Write-Host "[Build-Daemon] Using $threads parallel threads (CPU cores: $([Environment]::ProcessorCount), reserved: 2)"

$cmd += " && cd build && cmake --build . -j $threads"

cmd.exe /c $cmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[Build-Daemon] ✅ SUCCESS: Build completed without errors."
}
else {
    Write-Host "`n[Build-Daemon] ❌ ERROR: Build failed. Check the compiler output above."
}
exit $LASTEXITCODE
