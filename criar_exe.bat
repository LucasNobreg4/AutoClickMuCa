@echo off
echo ================================
echo    CRIANDO EXECUTAVEL DO SCRIPT
echo ================================

echo.
echo 🔧 Criando executavel com PyInstaller...
echo.

REM Comando PyInstaller com configurações otimizadas
pyinstaller ^
    --onefile ^
    --noconsole ^
    --name "ImageDetector" ^
    --icon=icon.ico ^
    --add-data "*.jpg;." ^
    --add-data "*.mp3;." ^
    --hidden-import=cv2 ^
    --hidden-import=numpy ^
    --hidden-import=pygame ^
    --hidden-import=mss ^
    --hidden-import=PIL ^
    --hidden-import=pyautogui ^
    Marijuana.py

echo.
if exist "dist\ImageDetector.exe" (
    echo ✅ SUCESSO! Executavel criado em: dist\ImageDetector.exe
    echo.
    echo 📁 Arquivos necessários:
    echo    - ImageDetector.exe
    echo    - Todas as imagens (.jpg)
    echo    - Todos os sons (.mp3)
    echo.
    echo 💡 DICA: Coloque o .exe na mesma pasta das imagens e sons!
) else (
    echo ❌ ERRO: Falha ao criar o executavel
)

echo.
pause
