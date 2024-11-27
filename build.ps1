# Use BuildTools 2022 path
$VcVarsPath = "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

if (-not (Test-Path $VcVarsPath)) {
    Write-Host "Error: Could not find vcvars64.bat at $VcVarsPath" -ForegroundColor Red
    exit 1
}

Write-Host "Found BuildTools at: $VcVarsPath" -ForegroundColor Green
Write-Host "Initializing Visual Studio BuildTools environment..." -ForegroundColor Cyan

# Initialize VS environment
$VsVars = cmd /c "`"$VcVarsPath`" && set"
foreach ($VsVar in $VsVars) {
    if ($VsVar -match "^([^=]+)=(.*)$") {
        $Name = $Matches[1]
        $Value = $Matches[2]
        Set-Item -Path "env:$Name" -Value $Value
    }
}

Write-Host "Building llama.cpp..." -ForegroundColor Cyan

# Make sure we're in the correct directory
$llamaPath = Join-Path $PSScriptRoot "llama.cpp"
Set-Location $llamaPath

Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
mkdir build
Set-Location build

Write-Host "Running CMake with CUDA support..." -ForegroundColor Cyan
$env:CC = "cl.exe"
$env:CXX = "cl.exe"

# Updated to use GGML_CUDA instead of LLAMA_CUBLAS
cmake .. -G "Ninja" -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=ON

if ($LASTEXITCODE -eq 0) {
    Write-Host "CMake configuration successful. Building..." -ForegroundColor Green
    cmake --build .
} else {
    Write-Host "CMake configuration failed!" -ForegroundColor Red
    Write-Host "Please ensure CUDA toolkit is installed." -ForegroundColor Yellow
    exit 1
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host "You can find the built executables in the 'build' directory." -ForegroundColor Cyan
} else {
    Write-Host "Build failed!" -ForegroundColor Red
}