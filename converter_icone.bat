@echo off
title Conversor de Icone - Image Detector
color 0B

echo.
echo ████████████████████████████████████
echo      CONVERSOR DE ICONE (.ICO)
echo ████████████████████████████████████
echo.

echo 🎨 Este script converte qualquer imagem em icone
echo.

REM Verificar se Pillow está instalado
python -c "import PIL" 2>nul
if errorlevel 1 (
    echo ❌ Pillow nao encontrado. Instalando...
    pip install Pillow
    if errorlevel 1 (
        echo ❌ Erro ao instalar Pillow
        pause
        exit /b 1
    )
    echo ✅ Pillow instalado com sucesso!
)

echo 💡 OPCOES:
echo    1. Converter imagem especifica
echo    2. Criar icone de exemplo
echo    3. Listar imagens disponiveis
echo.

set /p escolha="Escolha (1-3): "

if "%escolha%"=="1" (
    echo.
    echo 📂 Imagens encontradas:
    for %%f in (*.jpg *.png *.bmp *.gif) do echo    • %%f
    echo.
    set /p arquivo="Digite o nome da imagem: "
    if exist "!arquivo!" (
        python criar_icone.py "!arquivo!"
    ) else (
        echo ❌ Arquivo nao encontrado: !arquivo!
    )
) else if "%escolha%"=="2" (
    echo.
    echo 🎨 Criando icone de exemplo...
    python criar_icone.py
) else if "%escolha%"=="3" (
    echo.
    echo 📂 IMAGENS DISPONIVEIS:
    for %%f in (*.jpg *.png *.bmp *.gif) do echo    📷 %%f
    echo.
    echo 🎯 ICONES EXISTENTES:
    for %%f in (*.ico) do echo    🎨 %%f
) else (
    echo ❌ Opcao invalida
)

echo.
echo 💡 PROXIMO PASSO: Execute build_exe.py para rebuildar com novo icone
echo.
pause
