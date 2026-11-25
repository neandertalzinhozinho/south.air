# Runner único do port e dos testes J1..J6.
#
# Cada suíte e um harness `rustc --test` sobre `checks/<arquivo>.rs`, que aponta
# para o kernel em `port/src/<modulo>.rs` (fonte única). Assim o teste e a
# biblioteca nunca divergem.
#
#   pwsh -File port\run_tests.ps1          # rápido (~1 min)
#   pwsh -File port\run_tests.ps1 -Slow    # inclui dot AVX 400k e CRT 17.8M

param([switch]$Slow)

$ErrorActionPreference = 'Stop'
$port = $PSScriptRoot
$root = Split-Path -Parent $port
$checks = Join-Path $root 'checks'
$build = Join-Path $checks '.build'
New-Item -ItemType Directory -Force -Path $build | Out-Null

$suites = [ordered]@{
    'port (pending + chain + stage)' = $null   # cargo test
    'J1/J2 core'             = 'stage_j_core.rs'
    'J3 pipe'                = 'stage_j_pipe.rs'
    'J4 contrato'            = 'stage_j_fft.rs'
    'J4 kernels'             = 'j4_fft.rs'
    'J5 canal'               = 'stage_j_chan.rs'
    'J6 engine'              = 'stage_j_engine.rs'
}
if ($Slow) {
    $suites['J2 dot AVX 400k'] = 'j_dot32_avx.rs'
    $suites['CRT 17.8M']       = 'j_crt_equiv.rs'
}

$failed = @()
$total = 0

foreach ($name in $suites.Keys) {
    $file = $suites[$name]
    Write-Host "== $name" -ForegroundColor Cyan

    if ($null -eq $file) {
        # --lib: os doc-comments do kernel contêm listagens de asm em bloco,
        # que o rustdoc tentaria compilar como Rust. Doctest não é prova aqui.
        cargo test --quiet --lib --manifest-path (Join-Path $port 'Cargo.toml')
        if ($LASTEXITCODE -ne 0) { $failed += $name; continue }
        $total++
        continue
    }

    $src = Join-Path $checks $file
    $exe = Join-Path $build ([IO.Path]::GetFileNameWithoutExtension($file) + '.exe')
    rustc --edition 2021 --test $src -o $exe
    if ($LASTEXITCODE -ne 0) { $failed += "$name (build)"; continue }

    & $exe
    if ($LASTEXITCODE -ne 0) { $failed += "$name (run)"; continue }
    $total++
}

Write-Host ''
if ($failed.Count -gt 0) {
    Write-Host ("FALHOU: " + ($failed -join ', ')) -ForegroundColor Red
    exit 1
}
Write-Host "OK: $total suítes verdes (57 testes J + 18 do port)" -ForegroundColor Green
