$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogDir = Join-Path $Root '.runtime\logs'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
& { python (Join-Path $Root 'core\boot.py') 2>&1 | Tee-Object -FilePath (Join-Path $LogDir 'install.log') -Append }
if ($LASTEXITCODE -ne 0) { throw 'RootMC bootstrap failed' }
Write-Host "RootMC bootstrap complete. Logs: $LogDir"
