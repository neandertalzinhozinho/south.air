# Runs the IDA batch decompiler and stops IDA as soon as the report appears.
#
# The database MUST be the one built from the normalized PE
# (dumpsooth/soothe3_unpacked.dll, ImageBase 0x180000000, 30.859 .pdata
# functions). Opening ida_run\soothe3_unpacked_mem.bin (the 136.990.720 B raw
# memory dump) silently yields a DB with no functions - that was the root cause
# of the empty batches, see PLANO_MOTOR_AUDIO.md §19.
$root = "D:\PROJETOS\soultree"
$db = "C:\Users\tromb\AppData\Local\Temp\opencode\ida_pe\soothe3_pe.dll.i64"
$report = Join-Path $root "checks\ida_batch.txt"
$log = "C:\Users\tromb\AppData\Local\Temp\opencode\ida_pe\batch.log"

Remove-Item $report -ErrorAction SilentlyContinue
$p = Start-Process -FilePath "D:\TOOLS\IDA\idat.exe" `
    -ArgumentList "-A", "-S`"$root\tools\ida\decompile_batch.py`"", "-L$log", $db `
    -PassThru

$deadline = (Get-Date).AddMinutes(20)
while ((Get-Date) -lt $deadline) {
    if (Test-Path $report) { break }
    if ($p.HasExited) { break }
    Start-Sleep -Seconds 3
}

if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue }

if (Test-Path $report) {
    "REPORT OK"
    Get-Content $report
} else {
    "NO REPORT"
    if (Test-Path $log) { Get-Content $log -Tail 15 }
}
