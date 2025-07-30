#!/usr/bin/env python3
"""
Configurador de Auto-Clique para Image Detector
Permite ajustar facilmente as configurações de clique automático
"""
import re
from pathlib import Path

def ler_configuracoes_atuais():
    """Lê as configurações atuais do arquivo Python"""
    script_path = Path("Marijuana.py")
    if not script_path.exists():
        print("❌ Arquivo Marijuana.py não encontrado!")
        return None
    
    with open(script_path, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Extrair configurações usando regex
    configs = {}
    
    patterns = {
        'auto_click_habilitado': r'auto_click_habilitado\s*=\s*(True|False)',
        'click_delay': r'click_delay\s*=\s*([\d.]+)',
        'click_offset_x': r'click_offset_x\s*=\s*([-\d]+)',
        'click_offset_y': r'click_offset_y\s*=\s*([-\d]+)',
        'tipo_click': r"tipo_click\s*=\s*['\"]([^'\"]+)['\"]"
    }
    
    for nome, pattern in patterns.items():
        match = re.search(pattern, conteudo)
        if match:
            valor = match.group(1)
            if nome == 'auto_click_habilitado':
                configs[nome] = valor == 'True'
            elif nome in ['click_delay']:
                configs[nome] = float(valor)
            elif nome in ['click_offset_x', 'click_offset_y']:
                configs[nome] = int(valor)
            else:
                configs[nome] = valor
    
    return configs, conteudo

def salvar_configuracoes(conteudo, novas_configs):
    """Salva as novas configurações no arquivo"""
    
    replacements = {
        'auto_click_habilitado': f"auto_click_habilitado = {novas_configs['auto_click_habilitado']}",
        'click_delay': f"click_delay = {novas_configs['click_delay']}",
        'click_offset_x': f"click_offset_x = {novas_configs['click_offset_x']}",
        'click_offset_y': f"click_offset_y = {novas_configs['click_offset_y']}",
        'tipo_click': f"tipo_click = '{novas_configs['tipo_click']}'"
    }
    
    patterns = {
        'auto_click_habilitado': r'auto_click_habilitado\s*=\s*(True|False)',
        'click_delay': r'click_delay\s*=\s*[\d.]+',
        'click_offset_x': r'click_offset_x\s*=\s*[-\d]+',
        'click_offset_y': r'click_offset_y\s*=\s*[-\d]+',
        'tipo_click': r"tipo_click\s*=\s*['\"][^'\"]+['\"]"
    }
    
    novo_conteudo = conteudo
    for nome, replacement in replacements.items():
        pattern = patterns[nome]
        novo_conteudo = re.sub(pattern, replacement, novo_conteudo)
    
    # Salvar arquivo
    with open("Marijuana.py", 'w', encoding='utf-8') as f:
        f.write(novo_conteudo)
    
    print("✅ Configurações salvas com sucesso!")

def configurar_auto_click():
    """Interface principal de configuração"""
    print("🖱️  CONFIGURADOR DE AUTO-CLIQUE")
    print("=" * 40)
    
    # Ler configurações atuais
    resultado = ler_configuracoes_atuais()
    if not resultado:
        return
    
    configs, conteudo = resultado
    
    print("\n📋 CONFIGURAÇÕES ATUAIS:")
    print(f"   Auto-clique: {'🟢 HABILITADO' if configs.get('auto_click_habilitado', False) else '🔴 DESABILITADO'}")
    print(f"   Tipo: {configs.get('tipo_click', 'left')}")
    print(f"   Delay: {configs.get('click_delay', 0.1)}s")
    print(f"   Offset X: {configs.get('click_offset_x', 0)}")
    print(f"   Offset Y: {configs.get('click_offset_y', 0)}")
    
    print(f"\n⚙️  OPÇÕES DE CONFIGURAÇÃO:")
    print(f"   1. Habilitar/Desabilitar auto-clique")
    print(f"   2. Alterar tipo de clique")
    print(f"   3. Ajustar delay")
    print(f"   4. Ajustar offset de posição")
    print(f"   5. Configuração rápida (recomendada)")
    print(f"   0. Sair")
    
    while True:
        escolha = input(f"\nEscolha uma opção (0-5): ").strip()
        
        if escolha == "0":
            break
        elif escolha == "1":
            novo_valor = not configs.get('auto_click_habilitado', False)
            configs['auto_click_habilitado'] = novo_valor
            print(f"   ✅ Auto-clique: {'HABILITADO' if novo_valor else 'DESABILITADO'}")
            
        elif escolha == "2":
            print(f"\n   Tipos de clique disponíveis:")
            print(f"   • left (esquerdo - padrão)")
            print(f"   • right (direito)")
            print(f"   • middle (meio)")
            print(f"   • double (duplo)")
            
            novo_tipo = input(f"   Digite o tipo: ").strip().lower()
            if novo_tipo in ['left', 'right', 'middle', 'double']:
                configs['tipo_click'] = novo_tipo
                print(f"   ✅ Tipo alterado para: {novo_tipo}")
            else:
                print(f"   ❌ Tipo inválido!")
                
        elif escolha == "3":
            try:
                novo_delay = float(input(f"   Digite o delay em segundos (ex: 0.1): "))
                if 0 <= novo_delay <= 5:
                    configs['click_delay'] = novo_delay
                    print(f"   ✅ Delay alterado para: {novo_delay}s")
                else:
                    print(f"   ❌ Delay deve ser entre 0 e 5 segundos!")
            except ValueError:
                print(f"   ❌ Valor inválido!")
                
        elif escolha == "4":
            try:
                novo_x = int(input(f"   Offset X (atual: {configs.get('click_offset_x', 0)}): "))
                novo_y = int(input(f"   Offset Y (atual: {configs.get('click_offset_y', 0)}): "))
                
                configs['click_offset_x'] = novo_x
                configs['click_offset_y'] = novo_y
                print(f"   ✅ Offset alterado para: ({novo_x}, {novo_y})")
            except ValueError:
                print(f"   ❌ Valores inválidos!")
                
        elif escolha == "5":
            print(f"\n🚀 CONFIGURAÇÃO RÁPIDA:")
            print(f"   Configuração recomendada para coleta automática")
            
            configs['auto_click_habilitado'] = True
            configs['tipo_click'] = 'left'
            configs['click_delay'] = 0.1
            configs['click_offset_x'] = 0
            configs['click_offset_y'] = 0
            
            print(f"   ✅ Configuração aplicada!")
            print(f"   • Auto-clique: HABILITADO")
            print(f"   • Tipo: clique esquerdo")
            print(f"   • Delay: 0.1s")
            print(f"   • Offset: (0, 0)")
            
        else:
            print(f"   ❌ Opção inválida!")
            continue
        
        # Perguntar se quer salvar
        salvar = input(f"\n💾 Salvar alterações? (s/n): ").strip().lower()
        if salvar in ['s', 'sim', 'y', 'yes']:
            salvar_configuracoes(conteudo, configs)
            print(f"\n🎯 PRÓXIMO PASSO: Execute o detector para testar!")
            break
        else:
            print(f"   ⚠️  Alterações não salvas")

if __name__ == "__main__":
    configurar_auto_click()
    input(f"\n⏸️  Pressione Enter para fechar...")
