import cv2
import numpy as np
import pyautogui
import pygame.mixer
import time
import os
from PIL import ImageGrab
import mss
from datetime import datetime
from collections import defaultdict

# Configurações das imagens e som
media = [
    {'imagem': 'img_Gemstone.jpg', 'som': 'sound_Gemstone.mp3'},
    {'imagem': 'img_Jewel.jpg', 'som': 'android_end_call_tone.mp3'},
    {'imagem': 'img_bog.jpg', 'som': 'sound_Gemstone.mp3'},
    {'imagem': 'img_cob.jpg', 'som': 'sound_Gemstone.mp3'},
    {'imagem': 'img_soa.jpg', 'som': 'sound_Gemstone.mp3'},
    {'imagem': 'img_Zen.jpg', 'som': ''},  # Sem som para img_Zen
    # {'imagem': 'img_Symbol.jpg', 'som': 'sound_Gemstone.mp3'},
    # Adicione mais imagens aqui se necessário
]

porcentagem_setada = 0.77

# ⚙️ CONFIGURAÇÕES DE CLIQUE AUTOMÁTICO
auto_click_habilitado = True  # True = clica automaticamente, False = apenas detecta
click_delay = 0.1  # Delay antes do clique (segundos)
click_offset_x = 0  # Offset X do clique (pixels) - ajustar se necessário
click_offset_y = 0  # Offset Y do clique (pixels) - ajustar se necessário
tipo_click = 'left'  # 'left', 'right', 'middle', 'double'

# CONFIGURAÇÃO MULTI-MONITOR:
# 0 = Todos os monitores (área virtual completa)
# 1 = Monitor principal
# 2 = Segundo monitor  
# 3 = Terceiro monitor
# 4 = Quarto monitor (se existir)
monitor_alvo = 3  # Altere conforme necessário

# Inicializa o mixer Pygame
pygame.mixer.init()

# Detectar monitores disponíveis
print("🖥️  Detectando monitores disponíveis...")
try:
    with mss.mss() as sct:
        monitores = sct.monitors
        print(f"📊 Total de monitores detectados: {len(monitores)-1}")  # -1 porque o índice 0 é a área virtual
        for i, monitor in enumerate(monitores):
            if i == 0:
                print(f"   Monitor {i}: Área virtual completa - {monitor['width']}x{monitor['height']}")
            else:
                print(f"   Monitor {i}: {monitor['width']}x{monitor['height']} (posição: {monitor['left']}, {monitor['top']})")
        
        if monitor_alvo > len(monitores)-1:
            print(f"⚠️  Monitor {monitor_alvo} não existe! Usando monitor principal (1)")
            monitor_alvo = 1
        
        print(f"🎯 Configurado para capturar: Monitor {monitor_alvo}")
except Exception as e:
    print(f"❌ Erro ao detectar monitores: {e}")
    print("🔄 Usando captura padrão...")

# Inicializa o mixer Pygame
pygame.mixer.init()

# Diretório dos arquivos de imagem e som (usa o diretório do script)
diretorio = os.path.dirname(os.path.abspath(__file__))
print(f"📂 Diretório de trabalho: {diretorio}")

# Caminho completo para as imagens e sons
imagens = [os.path.join(diretorio, m['imagem']) for m in media]
sons = [os.path.join(diretorio, m['som']) if m['som'] and m['som'].strip() else '' for m in media]

# Variável para controlar a reprodução do som (só toca uma vez)
som_reproduzido = False

# 📊 SISTEMA DE HISTÓRICO E ESTATÍSTICAS
historico_deteccoes = []
contador_por_item = defaultdict(int)
total_deteccoes = 0
inicio_sessao = datetime.now()

def adicionar_deteccao(nome_item, confianca):
    """Adiciona uma detecção ao histórico"""
    global total_deteccoes
    
    deteccao = {
        'item': nome_item,
        'horario': datetime.now().strftime("%H:%M:%S"),
        'confianca': round(confianca, 3),
        'timestamp': datetime.now()
    }
    
    historico_deteccoes.append(deteccao)
    contador_por_item[nome_item] += 1
    total_deteccoes += 1
    
    return deteccao

def calcular_posicao_click(result, template_shape, monitor_offset=(0, 0)):
    """Calcula a posição do centro do item detectado para clique"""
    try:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Posição do match (canto superior esquerdo)
        top_left = max_loc
        
        # Calcular centro do template
        center_x = top_left[0] + template_shape[1] // 2
        center_y = top_left[1] + template_shape[0] // 2
        
        # Ajustar para posição real na tela (considerando offset do monitor)
        real_x = center_x + monitor_offset[0] + click_offset_x
        real_y = center_y + monitor_offset[1] + click_offset_y
        
        return (real_x, real_y), (center_x, center_y)
    except:
        return None, None

def executar_click(posicao_real, posicao_relativa, nome_item):
    """Executa o clique na posição detectada"""
    if not auto_click_habilitado:
        return False
        
    try:
        real_x, real_y = posicao_real
        rel_x, rel_y = posicao_relativa
        
        print(f"   🖱️  Clicando em: ({real_x}, {real_y}) [offset: {rel_x}, {rel_y}]")
        
        # Delay antes do clique
        if click_delay > 0:
            time.sleep(click_delay)
        
        # Executar clique baseado no tipo configurado
        if tipo_click == 'left':
            pyautogui.click(real_x, real_y)
        elif tipo_click == 'right':
            pyautogui.rightClick(real_x, real_y)
        elif tipo_click == 'middle':
            pyautogui.middleClick(real_x, real_y)
        elif tipo_click == 'double':
            pyautogui.doubleClick(real_x, real_y)
        
        print(f"   ✅ Clique executado com sucesso!")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao executar clique: {e}")
        return False

def mostrar_estatisticas():
    """Mostra estatísticas completas do histórico"""
    print("\n" + "="*60)
    print("📊 ESTATÍSTICAS DA SESSÃO")
    print("="*60)
    
    tempo_sessao = datetime.now() - inicio_sessao
    horas = int(tempo_sessao.total_seconds() // 3600)
    minutos = int((tempo_sessao.total_seconds() % 3600) // 60)
    
    print(f"🕐 Tempo de sessão: {horas}h {minutos}m")
    print(f"🎯 Total de detecções: {total_deteccoes}")
    
    if total_deteccoes > 0:
        print(f"⚡ Média: {total_deteccoes/(tempo_sessao.total_seconds()/60):.1f} detecções/min")
        
        print("\n📈 RANKING POR ITEM:")
        items_ordenados = sorted(contador_por_item.items(), key=lambda x: x[1], reverse=True)
        for item, count in items_ordenados:
            porcentagem = (count/total_deteccoes)*100
            print(f"   {item:<20} │ {count:>3}x │ {porcentagem:>5.1f}%")
        
        print(f"\n🕒 ÚLTIMAS 5 DETECÇÕES:")
        for deteccao in historico_deteccoes[-5:]:
            print(f"   {deteccao['horario']} │ {deteccao['item']:<20} │ {deteccao['confianca']:.3f}")
    
    print("="*60)

def salvar_historico():
    """Salva o histórico em arquivo"""
    try:
        with open("historico_deteccoes.txt", "w", encoding="utf-8") as f:
            f.write(f"HISTÓRICO DE DETECÇÕES - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"Total de detecções: {total_deteccoes}\n")
            f.write(f"Sessão iniciada em: {inicio_sessao.strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            f.write("DETECÇÕES POR ITEM:\n")
            for item, count in contador_por_item.items():
                f.write(f"{item}: {count}x\n")
            
            f.write(f"\nHISTÓRICO COMPLETO:\n")
            for deteccao in historico_deteccoes:
                f.write(f"{deteccao['horario']} - {deteccao['item']} (confiança: {deteccao['confianca']})\n")
        
        print(f"💾 Histórico salvo em: historico_deteccoes.txt")
    except Exception as e:
        print(f"❌ Erro ao salvar histórico: {e}")

# Configurar pyautogui para trabalhar melhor com múltiplos monitores
pyautogui.FAILSAFE = False

# Cache para templates pré-processadas
templates_cache = []
print("Carregando e processando templates...")

# Pré-carregar e pré-processar todas as templates
for i, imagem in enumerate(imagens):
    try:
        print(f"Tentando carregar: {imagem}")
        
        # Verificar se o arquivo existe
        if not os.path.exists(imagem):
            print(f"❌ Arquivo não encontrado: {imagem}")
            continue
            
        foto_cortada = cv2.imread(imagem, cv2.IMREAD_COLOR)
        if foto_cortada is not None:
            # Pré-calcular algumas escalas comuns
            escalas_rapidas = [1.0, 0.8, 1.2]  # Reduzido para 3 escalas mais comuns
            templates_escalas = []
            
            for escala in escalas_rapidas:
                if escala != 1.0:
                    width = int(foto_cortada.shape[1] * escala)
                    height = int(foto_cortada.shape[0] * escala)
                    template_escalada = cv2.resize(foto_cortada, (width, height))
                else:
                    template_escalada = foto_cortada
                templates_escalas.append(template_escalada)
            
            templates_cache.append({
                'templates': templates_escalas,
                'nome': media[i]['imagem'],
                'som': sons[i]
            })
            print(f"✅ Template carregada: {media[i]['imagem']}")
        else:
            print(f"❌ Erro ao carregar imagem: {imagem}")
            
    except Exception as e:
        print(f"❌ Erro ao processar {imagem}: {e}")

print("Templates carregadas. Iniciando monitoramento...")
print(f"💡 DICA: Para mudar de monitor, altere a variável 'monitor_alvo':")
print(f"   monitor_alvo = 1  # Monitor principal")
print(f"   monitor_alvo = 2  # Segundo monitor") 
print(f"   monitor_alvo = 3  # Terceiro monitor")
print(f"   monitor_alvo = 0  # Todos os monitores")
print(f"\n🖱️  CONFIGURAÇÕES DE CLIQUE:")
print(f"   Auto-clique: {'🟢 HABILITADO' if auto_click_habilitado else '🔴 DESABILITADO'}")
if auto_click_habilitado:
    print(f"   Tipo de clique: {tipo_click}")
    print(f"   Delay: {click_delay}s")
    print(f"   Offset: ({click_offset_x}, {click_offset_y})")
print("\n🎮 COMANDOS DURANTE EXECUÇÃO:")
print("   Ctrl+C: Parar e mostrar estatísticas")
print("   (O histórico será salvo automaticamente)")
print("─" * 50)

# Função otimizada para capturar tela
def capturar_tela_otimizada():
    try:
        # Usar apenas mss que é mais rápido
        with mss.mss() as sct:
            # Usar o monitor configurado com validação
            if monitor_alvo == 0:
                monitor = sct.monitors[0]  # Todos os monitores (área virtual)
            else:
                # Garantir que o monitor existe
                monitor_idx = min(monitor_alvo, len(sct.monitors)-1)
                monitor = sct.monitors[monitor_idx]
            
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    except Exception as e:
        print(f"❌ Erro na captura MSS: {e}")
        try:
            # Fallback para pyautogui
            screenshot = pyautogui.screenshot()
            img = np.array(screenshot)
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        except Exception as e2:
            print(f"❌ Erro no fallback: {e2}")
            return None

# Contador para reduzir prints
contador_monitoramento = 0

# Adicionar tratamento para Ctrl+C
try:
    while True:
        # Captura a tela de forma otimizada
        tela = capturar_tela_otimizada()
        
        # Se houve erro na captura, pula esta iteração
        if tela is None:
            time.sleep(0.5)
            continue
        
        # Percorre as templates pré-carregadas
        for i, template_data in enumerate(templates_cache):
            melhor_resultado = 0
            melhor_result = None
            melhor_template = None
            
            # Testa apenas as escalas pré-calculadas
            for template_escalada in template_data['templates']:
                # Verificação rápida de dimensões
                if template_escalada.shape[0] > tela.shape[0] or template_escalada.shape[1] > tela.shape[1]:
                    continue
                    
                try:
                    result = cv2.matchTemplate(tela, template_escalada, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(result)
                    
                    if max_val > melhor_resultado:
                        melhor_resultado = max_val
                        melhor_result = result
                        melhor_template = template_escalada
                        
                    # Se encontrou um resultado muito bom, para de testar outras escalas
                    if max_val > 0.9:
                        break
                        
                except Exception as e:
                    continue

            if melhor_resultado > porcentagem_setada and not som_reproduzido:
                # Adiciona ao histórico
                deteccao = adicionar_deteccao(template_data['nome'], melhor_resultado)
                
                # Calcular posição para clique (se habilitado)
                posicao_real = None
                posicao_relativa = None
                
                if auto_click_habilitado and melhor_result is not None:
                    # Calcular offset do monitor se necessário
                    monitor_offset = (0, 0)  # Para monitor específico, seria necessário calcular
                    
                    posicao_real, posicao_relativa = calcular_posicao_click(
                        melhor_result, 
                        melhor_template.shape, 
                        monitor_offset
                    )
                
                # Mostra detecção com mais informações
                if auto_click_habilitado and posicao_real:
                    print(f"🎯 DETECTADO #{total_deteccoes}: {deteccao['item']} às {deteccao['horario']} (confiança: {deteccao['confianca']})")
                    
                    # Executar clique
                    click_sucesso = executar_click(posicao_real, posicao_relativa, template_data['nome'])
                    
                    if click_sucesso:
                        print(f"   🎮 Item coletado automaticamente!")
                    else:
                        print(f"   ⚠️  Falha ao coletar item")
                else:
                    print(f"🎯 DETECTADO #{total_deteccoes}: {deteccao['item']} às {deteccao['horario']} (confiança: {deteccao['confianca']})")
                    if auto_click_habilitado:
                        print(f"   ℹ️  Clique desabilitado para esta detecção")
                
                # Reproduz o som correspondente
                try:
                    som_path = template_data['som']
                    # Verifica se há som configurado e se o arquivo existe
                    if som_path and som_path.strip() and os.path.exists(som_path):
                        pygame.mixer.music.load(som_path)
                        pygame.mixer.music.play()
                    elif not som_path or not som_path.strip():
                        print(f"   🔇 Sem som configurado para {template_data['nome']}")
                    else:
                        print(f"   ⚠️  Som não encontrado: {som_path}")
                except Exception as e:
                    print(f"   ❌ Erro ao reproduzir som: {e}")
                
                som_reproduzido = True
                time.sleep(2)
                break

        # Controle de som e timing otimizado
        if som_reproduzido:
            time.sleep(0.5)
            som_reproduzido = False
        else:
            # Reduz a frequência dos prints de monitoramento
            contador_monitoramento += 1
            if contador_monitoramento % 50 == 0:  # Mostra estatísticas a cada 50 iterações
                if total_deteccoes > 0:
                    tempo_decorrido = (datetime.now() - inicio_sessao).total_seconds() / 60
                    print(f"📊 {total_deteccoes} detecções em {tempo_decorrido:.1f}min │ Última: {historico_deteccoes[-1]['item'] if historico_deteccoes else 'Nenhuma'}")
                else:
                    print("🔍 monitorando... (nenhuma detecção ainda)")
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\n🛑 Monitoramento interrompido pelo usuário!")
    mostrar_estatisticas()
    salvar_historico()
    print("\n👋 Sessão finalizada!")

except Exception as e:
    print(f"\n❌ Erro inesperado: {e}")
    mostrar_estatisticas()
    salvar_historico()
