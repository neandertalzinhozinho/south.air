@echo off
rem Builds South.air (NDERTAL labs) and assembles dist\South.air.vst3 (same layout as a standard
rem VST3 bundle), then loads the plugin to check it. Copy dist\South.air.vst3 to
rem C:\Program Files\Common Files\VST3 to use it in your music software.
cd /d "%~dp0"
cargo build --release --features motor || exit /b 1
if exist dist\Resonia.vst3 rmdir /s /q dist\Resonia.vst3
if exist dist\South.air.vst3 rmdir /s /q dist\South.air.vst3
rem target explicito em .cargo\config.toml: a saida fica em target\x86_64-pc-windows-msvc\release
set OUT=target\x86_64-pc-windows-msvc\release
%OUT%\southair-app.exe --make-vst3 %OUT%\southair.dll dist || exit /b 1
if exist dist\resonia-app.exe del dist\resonia-app.exe
copy /y %OUT%\southair-app.exe dist\ >nul

rem O dump do motor (southdump.bin) agora e compilado DIRETAMENTE dentro da DLL (include_bytes!)
rem Nao e necessario copiar arquivos .bin soltos; o plugin e 100% autocontido.

echo Done: dist\South.air.vst3
