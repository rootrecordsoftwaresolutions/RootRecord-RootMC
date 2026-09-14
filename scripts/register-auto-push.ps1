$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Name = 'RootRecord-RootMC-AutoPush'
$Python = (Get-Command pythonw -ErrorAction Stop).Source
$Script = Join-Path $Root 'scripts\auto-push-task.py'
$Action = New-ScheduledTaskAction -Execute $Python -Argument "`"$Script`"" -WorkingDirectory $Root
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 15) -RepetitionDuration (New-TimeSpan -Days 3650)
$Principal = New-ScheduledTaskPrincipal -UserId ([Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive -RunLevel Limited
$Settings = New-ScheduledTaskSettingsSet -Hidden
Register-ScheduledTask -TaskName $Name -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Force | Out-Null
Write-Host "$Name registered. It will auto-commit and push this checkout every 15 minutes."
