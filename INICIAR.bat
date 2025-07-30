@echo off
title Image Detector - Configuracao Rapida
color 0A

echo.
echo ████████████████████████████████████████
echo     IMAGE DETECTOR - SETUP RAPIDO
echo ████████████████████████████████████████
echo.

echo 📂 Verificando arquivos necessarios...
echo.

REM Verificar se o executável existe
if exist "ImageDetector.exe" (
    echo ✅ ImageDetector.exe encontrado
) else (
    echo ❌ ImageDetector.exe NAO encontrado!
    echo    Copie o executavel para esta pasta
    goto erro
)

REM Contar imagens
set /a count_img=0
for %%f in (*.jpg) do set /a count_img+=1

echo ✅ Encontradas %count_img% imagens (.jpg)

REM Contar sons  
set /a count_mp3=0
for %%f in (*.mp3) do set /a count_mp3+=1

echo ✅ Encontrados %count_mp3% arquivos de som (.mp3)

echo.
if %count_img% GTR 0 if %count_mp3% GTR 0 (
    echo 🎯 TUDO PRONTO! Pressione qualquer tecla para iniciar o detector...
    pause >nul
    echo.
    echo 🚀 Iniciando Image Detector...
    echo 💡 Pressione Ctrl+C para parar e ver estatisticas
    echo.
    ImageDetector.exe
) else (
    echo ❌ ERRO: Arquivos faltando!
    echo.
    echo 📋 CHECKLIST:
    echo    [ ] ImageDetector.exe
    echo    [ ] Pelo menos 1 imagem (.jpg)  
    echo    [ ] Pelo menos 1 som (.mp3)
    echo.
    echo 💡 Copie todos os arquivos necessarios para esta pasta
)

goto fim

:erro
echo.
echo 📖 INSTRUCOES:
echo    1. Copie ImageDetector.exe para esta pasta
echo    2. Copie todas as imagens (.jpg) para esta pasta  
echo    3. Copie todos os sons (.mp3) para esta pasta
echo    4. Execute este script novamente
echo.

:fim
echo.
pause
