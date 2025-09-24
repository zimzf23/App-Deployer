# ======================
# install_nssm.ps1
# ======================

$VerbosePreference = "Continue"

Write-Host "[+] NSSM Installer starting..." -ForegroundColor Cyan

$NSSM_URL = "https://nssm.cc/release/nssm-2.24.zip"
$PreferredDir = "C:\nssm"

# Pick directory (fallback to LOCALAPPDATA if not admin)
$NSSM_DIR = $PreferredDir
if (-not (Test-Path $NSSM_DIR)) {
    try {
        New-Item -ItemType Directory -Path $NSSM_DIR -Force | Out-Null
    } catch {
        $NSSM_DIR = "$env:LOCALAPPDATA\nssm"
        New-Item -ItemType Directory -Path $NSSM_DIR -Force | Out-Null
    }
}

$NSSM_ZIP = Join-Path $NSSM_DIR "nssm.zip"
$NSSM_EXE = Join-Path $NSSM_DIR "nssm.exe"
$ExtractedDir = Join-Path $NSSM_DIR "nssm-2.24"

Write-Host "[DEBUG] NSSM_DIR      = $NSSM_DIR"
Write-Host "[DEBUG] NSSM_ZIP      = $NSSM_ZIP"
Write-Host "[DEBUG] NSSM_EXE      = $NSSM_EXE"
Write-Host "[DEBUG] EXTRACTED_DIR = $ExtractedDir"

# Skip if already present
if (Test-Path $NSSM_EXE) {
    Write-Host "[i] nssm.exe already exists at $NSSM_EXE"
} else {
    Write-Host "[+] Downloading NSSM..."
    Invoke-WebRequest -Uri $NSSM_URL -OutFile $NSSM_ZIP -UseBasicParsing

    Write-Host "[+] Extracting..."
    Expand-Archive -Path $NSSM_ZIP -DestinationPath $NSSM_DIR -Force
    Copy-Item "$ExtractedDir\win64\nssm.exe" $NSSM_EXE -Force

    Remove-Item $NSSM_ZIP -Force
    if (Test-Path $ExtractedDir) { Remove-Item $ExtractedDir -Recurse -Force }
}

# Add to user PATH
$d = $NSSM_DIR.TrimEnd('\')
$u = [Environment]::GetEnvironmentVariable("Path","User")
if (-not $u) { $u = "" }
$parts = $u -split ";" | Where-Object { $_ }
$norm  = $parts | ForEach-Object { $_.TrimEnd('\') }

if (-not ($norm -contains $d)) {
    $new = ($u.TrimEnd(';') + ";" + $d).Trim(';')
    [Environment]::SetEnvironmentVariable("Path",$new,"User")
    Write-Host "  -> USER PATH updated"
} else {
    Write-Host "  -> USER PATH already contains it"
}

Write-Host "`n✅ NSSM installed at $NSSM_EXE"
Write-Host "   Try in NEW terminal:  where nssm ; nssm.exe --version"

# === pause at the end ===
Read-Host "`nPress ENTER to close"
