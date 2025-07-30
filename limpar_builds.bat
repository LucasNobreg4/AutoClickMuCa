@echo off
title Limpeza de Builds - Image Detector
color 0C

echo.
echo ████████████████████████████████████
echo      LIMPEZA DE BUILDS ANTERIOR  
echo ████████████████████████████████████
echo.

echo 🧹 Removendo arquivos temporarios...
echo.

REM Remover pastas
if exist "build" (
    rmdir /s /q "build" 2>nul
    echo ✅ Pasta 'build' removida
) else (
    echo ⏩ Pasta 'build' nao existe
)

if exist "dist" (
    rmdir /s /q "dist" 2>nul
    echo ✅ Pasta 'dist' removida  
) else (
    echo ⏩ Pasta 'dist' nao existe
)

if exist "__pycache__" (
    rmdir /s /q "__pycache__" 2>nul
    echo ✅ Pasta '__pycache__' removida
) else (
    echo ⏩ Pasta '__pycache__' nao existe
)

REM Remover arquivos .spec
for %%f in (*.spec) do (
    del "%%f" 2>nul
    echo ✅ Arquivo %%f removido
)

echo.
echo 🎯 LIMPEZA CONCLUIDA!
echo.
echo 💡 PROXIMOS PASSOS:
echo    • Execute build_exe.py para criar novo executavel
echo    • Ou edite Marijuana.py e execute o build novamente
echo.
pause
