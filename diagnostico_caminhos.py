#!/usr/bin/env python3
"""
Script de diagnóstico para identificar problemas de caminho
"""
import os
from pathlib import Path

def diagnosticar_caminhos():
    print("🔍 DIAGNÓSTICO DE CAMINHOS")
    print("=" * 40)
    
    # 1. Verificar diretório atual
    diretorio_atual = os.getcwd()
    print(f"📂 Diretório atual: {diretorio_atual}")
    
    # 2. Verificar diretório do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📄 Diretório do script: {script_dir}")
    
    # 3. Verificar se são diferentes
    if diretorio_atual != script_dir:
        print(f"⚠️  ATENÇÃO: Diretórios diferentes!")
        print(f"   Isso pode causar problemas de 'file not found'")
    else:
        print(f"✅ Diretórios coincidem")
    
    print(f"\n📁 ARQUIVOS NO DIRETÓRIO ATUAL:")
    try:
        arquivos = os.listdir(diretorio_atual)
        for arquivo in sorted(arquivos):
            if arquivo.endswith(('.jpg', '.mp3', '.py')):
                print(f"   ✅ {arquivo}")
    except Exception as e:
        print(f"   ❌ Erro ao listar: {e}")
    
    print(f"\n📁 ARQUIVOS NO DIRETÓRIO DO SCRIPT:")
    try:
        arquivos_script = os.listdir(script_dir)
        for arquivo in sorted(arquivos_script):
            if arquivo.endswith(('.jpg', '.mp3', '.py')):
                print(f"   ✅ {arquivo}")
    except Exception as e:
        print(f"   ❌ Erro ao listar: {e}")
    
    # 4. Testar caminhos específicos
    print(f"\n🧪 TESTE DE CAMINHOS:")
    
    # Configuração atual do script
    media_teste = [
        {'imagem': 'img_Gemstone.jpg', 'som': 'sound_Gemstone.mp3'},
        {'imagem': 'img_Jewel.jpg', 'som': 'android_end_call_tone.mp3'},
        {'imagem': 'img_bog.jpg', 'som': 'sound_Gemstone.mp3'},
        {'imagem': 'img_cob.jpg', 'som': 'sound_Gemstone.mp3'},
        {'imagem': 'img_soa.jpg', 'som': 'sound_Gemstone.mp3'},
    ]
    
    # Método 1: Diretório atual
    print(f"\n   Método 1 - Diretório atual:")
    for item in media_teste:
        caminho_img = os.path.join(diretorio_atual, item['imagem'])
        caminho_som = os.path.join(diretorio_atual, item['som'])
        
        existe_img = os.path.exists(caminho_img)
        existe_som = os.path.exists(caminho_som)
        
        print(f"     {'✅' if existe_img else '❌'} {item['imagem']}")
        print(f"     {'✅' if existe_som else '❌'} {item['som']}")
    
    # Método 2: Diretório do script
    print(f"\n   Método 2 - Diretório do script:")
    for item in media_teste:
        caminho_img = os.path.join(script_dir, item['imagem'])
        caminho_som = os.path.join(script_dir, item['som'])
        
        existe_img = os.path.exists(caminho_img)
        existe_som = os.path.exists(caminho_som)
        
        print(f"     {'✅' if existe_img else '❌'} {item['imagem']}")
        print(f"     {'✅' if existe_som else '❌'} {item['som']}")
    
    # 5. Recomendar solução
    print(f"\n💡 RECOMENDAÇÕES:")
    if diretorio_atual != script_dir:
        print(f"   1. Execute o script a partir da pasta onde estão as imagens")
        print(f"   2. Ou mova todas as imagens/sons para: {diretorio_atual}")
        print(f"   3. Ou use: cd \"{script_dir}\" antes de executar")
    else:
        print(f"   ✅ Configuração correta!")
        
        # Verificar se faltam arquivos
        faltando = []
        for item in media_teste:
            if not os.path.exists(os.path.join(script_dir, item['imagem'])):
                faltando.append(item['imagem'])
            if not os.path.exists(os.path.join(script_dir, item['som'])):
                faltando.append(item['som'])
        
        if faltando:
            print(f"   ⚠️  Arquivos faltando: {', '.join(faltando)}")
        else:
            print(f"   ✅ Todos os arquivos necessários encontrados!")

if __name__ == "__main__":
    diagnosticar_caminhos()
    input(f"\n⏸️  Pressione Enter para fechar...")
