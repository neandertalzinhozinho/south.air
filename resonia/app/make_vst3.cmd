@echo off
rem Builds Resonia and assembles dist\Resonia.vst3 (same layout as a standard VST3 bundle),
rem then loads the plugin to check it. Copy dist\Resonia.vst3 to
rem C:\Program Files\Common Files\VST3 to use it in your music software.
cd /d "%~dp0"
cargo build --release --features motor || exit /b 1
if exist dist\Resonia.vst3 rmdir /s /q dist\Resonia.vst3
rem target explicito em .cargo\config.toml: a saida fica em target\x86_64-pc-windows-msvc\release
set OUT=target\x86_64-pc-windows-msvc\release
%OUT%\resonia-app.exe --make-vst3 %OUT%\resonia.dll dist || exit /b 1
copy /y %OUT%\resonia-app.exe dist\ >nul
echo Done: dist\Resonia.vst3
