"""
Script para converter imagem em ícone (.ico)
Requer: pip install Pillow
"""
from PIL import Image
import sys

def criar_icone_exemplo():
    """Cria um ícone básico de exemplo"""
    try:
        # Criar uma imagem simples com texto
        img = Image.new('RGBA', (256, 256), (0, 100, 200, 255))  # Fundo azul
        
        # Adicionar um círculo simples
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Círculo branco no centro
        draw.ellipse([64, 64, 192, 192], fill=(255, 255, 255, 255))
        # Círculo menor azul escuro
        draw.ellipse([96, 96, 160, 160], fill=(0, 50, 100, 255))
        
        # Salvar como .ico com múltiplos tamanhos
        img.save('detector_icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
        print("✅ Ícone de exemplo criado: detector_icon.ico")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar ícone: {e}")
        return False

def converter_imagem_para_icone(arquivo_entrada, arquivo_saida="custom_icon.ico"):
    """Converte uma imagem para formato .ico"""
    try:
        # Abrir imagem
        img = Image.open(arquivo_entrada)
        
        # Converter para RGBA se necessário
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Redimensionar para quadrado se necessário
        width, height = img.size
        if width != height:
            size = min(width, height)
            # Cortar para ficar quadrado (crop do centro)
            left = (width - size) // 2
            top = (height - size) // 2
            img = img.crop((left, top, left + size, top + size))
        
        # Salvar como .ico com múltiplos tamanhos
        img.save(arquivo_saida, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
        print(f"✅ Ícone criado: {arquivo_saida}")
        return True
    except Exception as e:
        print(f"❌ Erro ao converter: {e}")
        return False

if __name__ == "__main__":
    print("🎨 CRIADOR DE ÍCONES PARA EXECUTÁVEL")
    print("=" * 40)
    
    # Verificar se foi passado um arquivo
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
        print(f"📁 Convertendo: {arquivo}")
        converter_imagem_para_icone(arquivo)
    else:
        print("💡 Opções:")
        print("1. Criar ícone de exemplo")
        print("2. Converter imagem existente")
        
        escolha = input("\nEscolha (1 ou 2): ").strip()
        
        if escolha == "1":
            criar_icone_exemplo()
        elif escolha == "2":
            arquivo = input("Digite o nome da imagem (ex: minha_imagem.jpg): ").strip()
            if arquivo:
                converter_imagem_para_icone(arquivo)
        else:
            print("❌ Opção inválida")
    
    input("\n⏸️  Pressione Enter para fechar...")
