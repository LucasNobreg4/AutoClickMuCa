#!/usr/bin/env python3
"""
Script para criar executável do detector de imagens
"""
import os
import subprocess
import sys
import shutil
from pathlib import Path

def limpar_builds_anteriores():
    """Remove arquivos de builds anteriores"""
    print("🧹 Limpando builds anteriores...")
    
    # Pastas a limpar
    pastas_para_limpar = ["build", "dist", "__pycache__"]
    
    for pasta in pastas_para_limpar:
        pasta_path = Path(pasta)
        if pasta_path.exists():
            try:
                shutil.rmtree(pasta_path)
                print(f"   ✅ Removido: {pasta}/")
            except Exception as e:
                print(f"   ⚠️  Não foi possível remover {pasta}/: {e}")
    
    # Arquivos .spec (gerados pelo PyInstaller)
    for spec_file in Path(".").glob("*.spec"):
        try:
            spec_file.unlink()
            print(f"   ✅ Removido: {spec_file.name}")
        except Exception as e:
            print(f"   ⚠️  Não foi possível remover {spec_file.name}: {e}")
    
    print("   🔄 Limpeza concluída!\n")

def detectar_icone():
    """Detecta se existe um arquivo de ícone na pasta"""
    icones_possiveis = ["detector_icon.ico", "icon.ico", "app_icon.ico", "custom_icon.ico"]
    
    for icone in icones_possiveis:
        if Path(icone).exists():
            return icone
    
    # Procurar qualquer arquivo .ico
    icones_encontrados = list(Path(".").glob("*.ico"))
    if icones_encontrados:
        return str(icones_encontrados[0])
    
    return None

def criar_executavel():
    print("=" * 50)
    print("    CRIANDO EXECUTÁVEL DO IMAGE DETECTOR")
    print("=" * 50)
    
    # Perguntar se quer limpar builds anteriores
    resposta = input("🗑️  Limpar builds anteriores? (s/n) [recomendado]: ").strip().lower()
    if resposta in ['s', 'sim', 'y', 'yes', '']:
        limpar_builds_anteriores()
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Configurações do build
    script_name = "Marijuana.py"
    exe_name = "ImageDetector"
    
    # Verificar se o script existe
    if not Path(script_name).exists():
        print(f"❌ Erro: {script_name} não encontrado!")
        return False
    
    print(f"\n🔧 Criando executável a partir de {script_name}...")
    
    # Detectar ícone
    icone_path = detectar_icone()
    if icone_path:
        print(f"🎨 Ícone encontrado: {icone_path}")
    else:
        print("ℹ️  Nenhum ícone encontrado (será usado ícone padrão)")
        resposta_icone = input("   Quer criar um ícone de exemplo? (s/n): ").strip().lower()
        if resposta_icone in ['s', 'sim', 'y', 'yes']:
            try:
                from PIL import Image, ImageDraw
                # Criar ícone simples
                img = Image.new('RGBA', (256, 256), (0, 120, 215, 255))  # Azul Windows
                draw = ImageDraw.Draw(img)
                # Desenhar um símbolo simples
                draw.ellipse([64, 64, 192, 192], fill=(255, 255, 255, 255))
                draw.ellipse([96, 96, 160, 160], fill=(0, 120, 215, 255))
                img.save('detector_icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128)])
                print("   ✅ Ícone de exemplo criado: detector_icon.ico")
                icone_path = "detector_icon.ico"
            except ImportError:
                print("   ⚠️  Pillow não instalado. Install com: pip install Pillow")
            except Exception as e:
                print(f"   ❌ Erro ao criar ícone: {e}")
    
    # Comando PyInstaller
    comando = [
        "pyinstaller",
        "--onefile",                    # Arquivo único
        "--console",                    # Com console (para ver mensagens)
        f"--name={exe_name}",          # Nome do executável
        "--add-data=*.jpg;.",          # Incluir imagens
        "--add-data=*.mp3;.",          # Incluir sons
        "--hidden-import=cv2",         # Imports necessários
        "--hidden-import=numpy",
        "--hidden-import=pygame",
        "--hidden-import=mss",
        "--hidden-import=PIL",
        "--hidden-import=pyautogui",
        "--hidden-import=collections",
        "--hidden-import=datetime",
        script_name
    ]
    
    # Adicionar ícone se encontrado
    if icone_path:
        comando.insert(-1, f"--icon={icone_path}")
        print(f"   🎨 Usando ícone: {icone_path}")
    
    try:
        # Executar PyInstaller
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            exe_path = Path("dist") / f"{exe_name}.exe"
            if exe_path.exists():
                print(f"\n✅ SUCESSO! Executável criado:")
                print(f"   📁 Localização: {exe_path.absolute()}")
                print(f"   📊 Tamanho: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
                
                # Verificar se existe versão anterior na pasta atual
                exe_local = Path(f"{exe_name}.exe")
                if exe_local.exists():
                    resposta_substituir = input(f"\n⚠️  {exe_name}.exe já existe nesta pasta. Substituir? (s/n): ")
                    if resposta_substituir.lower() in ['s', 'sim', 'y', 'yes']:
                        try:
                            shutil.copy2(exe_path, exe_local)
                            print(f"   ✅ Executável atualizado: {exe_local.absolute()}")
                        except Exception as e:
                            print(f"   ❌ Erro ao copiar: {e}")
                    else:
                        print(f"   💡 Nova versão disponível em: {exe_path.absolute()}")
                else:
                    # Copiar automaticamente se não existir
                    try:
                        shutil.copy2(exe_path, exe_local)
                        print(f"   📋 Copiado para pasta atual: {exe_local.absolute()}")
                    except Exception as e:
                        print(f"   ⚠️  Não foi possível copiar para pasta atual: {e}")
                
                print(f"\n📋 INSTRUÇÕES DE USO:")
                print(f"   1. Copie o executável para onde quiser")
                print(f"   2. Coloque as imagens (.jpg) na mesma pasta")
                print(f"   3. Coloque os sons (.mp3) na mesma pasta")
                print(f"   4. Execute o {exe_name}.exe")
                
                print(f"\n🎯 ARQUIVOS NECESSÁRIOS:")
                for arquivo in Path(".").glob("*.jpg"):
                    print(f"   📷 {arquivo.name}")
                for arquivo in Path(".").glob("*.mp3"):
                    print(f"   🔊 {arquivo.name}")
                
                return True
            else:
                print("❌ Erro: Executável não foi criado")
                return False
        else:
            print("❌ Erro durante a criação:")
            print(resultado.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def criar_executavel_sem_console():
    """Cria versão sem console (mais limpa)"""
    print("\n" + "=" * 50)
    print("    CRIANDO VERSÃO SEM CONSOLE")
    print("=" * 50)
    
    # Detectar ícone também para versão silenciosa
    icone_path = detectar_icone()
    
    comando = [
        "pyinstaller",
        "--onefile",
        "--noconsole",                 # SEM console
        "--name=ImageDetector_Silent", # Nome diferente
        "--add-data=*.jpg;.",
        "--add-data=*.mp3;.",
        "--hidden-import=cv2",
        "--hidden-import=numpy",
        "--hidden-import=pygame",
        "--hidden-import=mss",
        "--hidden-import=PIL",
        "--hidden-import=pyautogui",
        "Marijuana.py"
    ]
    
    # Adicionar ícone se encontrado
    if icone_path:
        comando.insert(-1, f"--icon={icone_path}")
        print(f"🎨 Usando ícone: {icone_path}")
    
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
        if resultado.returncode == 0:
            print("✅ Versão silenciosa criada: ImageDetector_Silent.exe")
        else:
            print("❌ Erro na versão silenciosa")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    # Criar versão com console
    sucesso = criar_executavel()
    
    if sucesso:
        resposta = input("\n❓ Criar também versão sem console? (s/n): ")
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            criar_executavel_sem_console()
    
    input("\n⏸️  Pressione Enter para fechar...")
