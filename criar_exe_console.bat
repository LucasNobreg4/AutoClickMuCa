@echo off
echo ================================
echo  CRIANDO EXECUTAVEL (COM CONSOLE)
echo ================================

echo.
echo 🔧 Criando executavel com console para debug...
echo.

REM Comando PyInstaller com console habilitado
pyinstaller ^
    --onefile ^
    --console ^
    --name "ImageDetector_Console" ^
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
if exist "dist\ImageDetector_Console.exe" (
    echo ✅ SUCESSO! Executavel criado em: dist\ImageDetector_Console.exe
    echo.
    echo 📁 Arquivos necessários:
    echo    - ImageDetector_Console.exe
    echo    - Todas as imagens (.jpg)  
    echo    - Todos os sons (.mp3)
    echo.
    echo 💡 Esta versão mostra o console com as mensagens de debug
) else (
    echo ❌ ERRO: Falha ao criar o executavel
)

echo.
pause
