param(
    [string]$SourceRoot = "",
    [string]$CodexHome = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($SourceRoot)) {
    $SourceRoot = Join-Path (Split-Path -Parent $PSScriptRoot) "skill"
}

if (-not (Test-Path -LiteralPath $SourceRoot -PathType Container)) {
    throw "Skill source directory not found: $SourceRoot"
}

if ([string]::IsNullOrWhiteSpace($CodexHome)) {
    $CodexHome = $env:CODEX_HOME
}

if ([string]::IsNullOrWhiteSpace($CodexHome)) {
    if ([string]::IsNullOrWhiteSpace($env:USERPROFILE)) {
        throw "Neither CODEX_HOME nor USERPROFILE is set."
    }
    $CodexHome = Join-Path $env:USERPROFILE ".codex"
}

$TargetRoot = Join-Path $CodexHome "skills"
New-Item -ItemType Directory -Force -Path $CodexHome | Out-Null
New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

$skillFiles = Get-ChildItem -LiteralPath $SourceRoot -Recurse -Filter "SKILL.md" -File
if (-not $skillFiles) {
    Write-Host "No skills found under $SourceRoot"
    exit 0
}

$seen = @{}
$copied = 0

foreach ($skillFile in $skillFiles) {
    $skillDir = $skillFile.Directory
    $skillName = $skillDir.Name

    if ($seen.ContainsKey($skillName)) {
        throw "Duplicate skill directory name '$skillName': $($seen[$skillName]) and $($skillDir.FullName)"
    }
    $seen[$skillName] = $skillDir.FullName

    $targetDir = Join-Path $TargetRoot $skillName
    if (Test-Path -LiteralPath $targetDir) {
        Remove-Item -LiteralPath $targetDir -Recurse -Force
    }

    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    Get-ChildItem -LiteralPath $skillDir.FullName -Force | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $targetDir -Recurse -Force
    }
    Write-Host "Copied skill: $skillName -> $targetDir"
    $copied += 1
}

Write-Host "Done. Copied $copied skill(s) to $TargetRoot"
