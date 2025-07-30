#!/usr/bin/env python3
"""
Script para limpar arquivos de build do PyInstaller
"""
import shutil
from pathlib import Path

def limpar_tudo():
    """Remove todos os arquivos temporários e builds"""
    print("🧹 LIMPEZA COMPLETA DE BUILDS")
    print("=" * 40)
    
    # Pastas a remover
    pastas = ["build", "dist", "__pycache__"]
    
    # Arquivos a remover
    extensoes = ["*.spec", "*.pyc", "*.pyo"]
    
    removidos = 0
    
    # Remover pastas
    for pasta in pastas:
        pasta_path = Path(pasta)
        if pasta_path.exists():
            try:
                shutil.rmtree(pasta_path)
                print(f"✅ Pasta removida: {pasta}/")
                removidos += 1
            except Exception as e:
                print(f"❌ Erro ao remover {pasta}/: {e}")
        else:
            print(f"⏩ Pasta não existe: {pasta}/")
    
    # Remover arquivos por extensão
    for extensao in extensoes:
        for arquivo in Path(".").glob(extensao):
            try:
                arquivo.unlink()
                print(f"✅ Arquivo removido: {arquivo.name}")
                removidos += 1
            except Exception as e:
                print(f"❌ Erro ao remover {arquivo.name}: {e}")
    
    # Remover executáveis antigos (opcional)
    executaveis = list(Path(".").glob("*.exe"))
    if executaveis:
        print(f"\n📋 Encontrados {len(executaveis)} executáveis:")
        for exe in executaveis:
            print(f"   • {exe.name}")
        
        resposta = input("\n❓ Remover executáveis também? (s/n): ")
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            for exe in executaveis:
                try:
                    exe.unlink()
                    print(f"✅ Executável removido: {exe.name}")
                    removidos += 1
                except Exception as e:
                    print(f"❌ Erro ao remover {exe.name}: {e}")
    
    print(f"\n🎯 RESULTADO:")
    if removidos > 0:
        print(f"   ✅ {removidos} itens removidos com sucesso!")
        print(f"   💽 Espaço liberado!")
    else:
        print(f"   ℹ️  Nada para remover")
    
    print(f"\n💡 AGORA VOCÊ PODE:")
    print(f"   • Executar build_exe.py para criar novo executável")
    print(f"   • Editar Marijuana.py e rebuildar")

if __name__ == "__main__":
    limpar_tudo()
    input("\n⏸️  Pressione Enter para fechar...")
