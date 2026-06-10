# CleanRAM.ps1 — Kill RAM hogs, disable auto-restart services
# Must run as Administrator

param([switch]$SelfElevated)

# ── Self-elevate if not admin ──────────────────────────────────────────────────
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Not running as admin. Relaunching elevated..." -ForegroundColor Yellow
    $scriptPath = $MyInvocation.MyCommand.Path
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`" -SelfElevated" -Verb RunAs -Wait
    exit
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CleanRAM — Running as Administrator  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ── Helper: stop service + disable it ─────────────────────────────────────────
function Kill-Service {
    param([string]$Name, [string]$Label)
    $svc = Get-Service -Name $Name -ErrorAction SilentlyContinue
    if ($svc) {
        try {
            Set-Service -Name $Name -StartupType Disabled -ErrorAction Stop
            Stop-Service -Name $Name -Force -ErrorAction SilentlyContinue
            Write-Host "  [OK] Service disabled+stopped: $Label" -ForegroundColor Green
        } catch {
            Write-Host "  [WARN] $Label : $_" -ForegroundColor Yellow
        }
    }
}

# ── Helper: kill process by name ──────────────────────────────────────────────
function Kill-Proc {
    param([string]$Name)
    $procs = Get-Process -Name $Name -ErrorAction SilentlyContinue
    if ($procs) {
        $mb = [math]::Round(($procs | Measure-Object WorkingSet64 -Sum).Sum / 1MB, 0)
        # Use taskkill /F /T to also kill child processes, bypass self-protection
        & taskkill.exe /F /T /IM "$Name.exe" 2>$null | Out-Null
        $still = Get-Process -Name $Name -ErrorAction SilentlyContinue
        if ($still) {
            Write-Host "  [FAIL] Could not kill: $Name" -ForegroundColor Red
        } else {
            Write-Host "  [OK] Killed: $Name ($mb MB freed)" -ForegroundColor Green
        }
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# 1. McAFEE — disable all services first, then kill processes
# ══════════════════════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "[ McAfee ]" -ForegroundColor Magenta
$mcServices = @(
    @{Name='mc-fw-host';          Label='McAfee Framework Host'},
    @{Name='McAfee WebAdvisor';   Label='McAfee WebAdvisor'},
    @{Name='McmSvc';              Label='Mobile Connectivity Management'},
    @{Name='McpManagementService';Label='McAfee Management Service'},
    @{Name='mc-wps-secdashboardservice'; Label='McAfee Security Dashboard'},
    @{Name='mc-wps-update';       Label='McAfee Software Update'}
)
foreach ($s in $mcServices) { Kill-Service $s.Name $s.Label }
Start-Sleep -Milliseconds 1500
Kill-Proc 'mc-fw-host'
Kill-Proc 'McUICnt'
Kill-Proc 'mcshield'

# ══════════════════════════════════════════════════════════════════════════════
# 2. ASUS ArmouryCrate — disable all services, then kill
# ══════════════════════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "[ ASUS ArmouryCrate ]" -ForegroundColor Magenta
$asusServices = @(
    @{Name='ArmouryCrateService';       Label='Armoury Crate Service'},
    @{Name='ArmouryCrateControlInterface'; Label='Armoury Crate Control Interface'},
    @{Name='asus';                      Label='ASUS Update Service (asus)'},
    @{Name='AsusAppService';            Label='ASUS App Service'},
    @{Name='asusm';                     Label='ASUS Update Service (asusm)'},
    @{Name='AsusMsControl';             Label='ASUS MS Control'},
    @{Name='ASUSOptimization';          Label='ASUS Optimization'},
    @{Name='AsusPTPService';            Label='AsusPTPService'},
    @{Name='ASUSSoftwareManager';       Label='ASUS Software Manager'},
    @{Name='ASUSSwitch';                Label='ASUS Switch'},
    @{Name='ASUSSystemAnalysis';        Label='ASUS System Analysis'},
    @{Name='ASUSSystemDiagnosis';       Label='ASUS System Diagnosis'}
)
foreach ($s in $asusServices) { Kill-Service $s.Name $s.Label }
Start-Sleep -Milliseconds 1500
Kill-Proc 'ArmouryCrate.UserSessionHelper'
Kill-Proc 'ArmouryCrate.Service'
Kill-Proc 'ArmouryCrateControlInterface'
Kill-Proc 'AsusSoftwareManagerAgent'

# ══════════════════════════════════════════════════════════════════════════════
# 3. AnyDesk — stop service, kill process
# ══════════════════════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "[ AnyDesk ]" -ForegroundColor Magenta
Kill-Service 'AnyDesk' 'AnyDesk Service'
Start-Sleep -Milliseconds 800
Kill-Proc 'AnyDesk'

# ══════════════════════════════════════════════════════════════════════════════
# 4. Adobe Creative Cloud (background daemons — not the main app)
# ══════════════════════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "[ Adobe Creative Cloud daemons ]" -ForegroundColor Magenta
Kill-Proc 'Creative Cloud'
Kill-Proc 'Creative Cloud UI Helper'
Kill-Proc 'Adobe Desktop Service'
Kill-Proc 'CoreSync'
Kill-Proc 'Creative Cloud Helper'
Kill-Proc 'AdobeUpdateService'
Kill-Proc 'AdobeIPCBroker'
Kill-Proc 'node'   # CC spawns node.exe background workers

# ══════════════════════════════════════════════════════════════════════════════
# 5. Windows Phone Link
# ══════════════════════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "[ Phone Link ]" -ForegroundColor Magenta
Kill-Proc 'PhoneExperienceHost'

# ══════════════════════════════════════════════════════════════════════════════
# 6. Misc background apps
# ══════════════════════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "[ Misc background apps ]" -ForegroundColor Magenta
Kill-Proc 'WhatsApp.Root'
Kill-Proc 'TurboVPN'
Kill-Proc 'ollama'
Kill-Proc 'TeamViewer'
Kill-Proc 'BlueStacksServices'
Kill-Proc 'HD-Player'          # BlueStacks player
Kill-Proc 'RadeonSoftware'
Kill-Proc 'OneDrive'

# msedgewebview2 is spawned by the apps above — kill after parents are gone
Start-Sleep -Milliseconds 1000
Kill-Proc 'msedgewebview2'

# ══════════════════════════════════════════════════════════════════════════════
# 7. Disable startup entries for these apps
# ══════════════════════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "[ Disabling startup entries ]" -ForegroundColor Magenta
$startupKeys = @(
    'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run',
    'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run',
    'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run'
)
$startupBlockNames = @('OneDrive','TurboVPN','AnyDesk','ArmouryCrate','BlueStacks','Creative Cloud','ollama')
foreach ($key in $startupKeys) {
    if (Test-Path $key) {
        $vals = Get-ItemProperty -Path $key -ErrorAction SilentlyContinue
        foreach ($name in $startupBlockNames) {
            $match = $vals.PSObject.Properties | Where-Object { $_.Name -like "*$name*" }
            foreach ($m in $match) {
                try {
                    Remove-ItemProperty -Path $key -Name $m.Name -ErrorAction Stop
                    Write-Host "  [OK] Removed startup: $($m.Name)" -ForegroundColor Green
                } catch {
                    Write-Host "  [WARN] Could not remove startup: $($m.Name)" -ForegroundColor Yellow
                }
            }
        }
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# 8. Final RAM report
# ══════════════════════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "           FINAL RAM STATUS           " -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
$available = (Get-Counter '\Memory\Available MBytes').CounterSamples[0].CookedValue
$total = (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB
Write-Host ""
Write-Host "Total RAM  : $([math]::Round($total,1)) GB" -ForegroundColor White
Write-Host "Available  : $([math]::Round($available/1024,1)) GB" -ForegroundColor Green
Write-Host "In use     : $([math]::Round($total - $available/1024,1)) GB" -ForegroundColor Yellow
Write-Host ""
Write-Host "Top 20 processes by RAM:" -ForegroundColor White
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 20 Name, @{N='RAM(MB)';E={[math]::Round($_.WorkingSet64/1MB,1)}} | Format-Table -AutoSize

Write-Host ""
Write-Host "Done. Press any key to close..." -ForegroundColor Cyan
if ($SelfElevated) { $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown') }
