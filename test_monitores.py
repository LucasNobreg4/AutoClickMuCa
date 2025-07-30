import mss
import cv2
import numpy as np
import time

print("🖥️  TESTE DE MONITORES")
print("=" * 40)

try:
    with mss.mss() as sct:
        monitores = sct.monitors
        print(f"📊 Monitores detectados: {len(monitores)-1}")
        
        for i, monitor in enumerate(monitores):
            if i == 0:
                print(f"\n🌐 Monitor {i}: Área Virtual Completa")
                print(f"   Resolução: {monitor['width']}x{monitor['height']}")
            else:
                print(f"\n🖥️  Monitor {i}:")
                print(f"   Resolução: {monitor['width']}x{monitor['height']}")
                print(f"   Posição: ({monitor['left']}, {monitor['top']})")
                
                # Captura uma pequena amostra de cada monitor
                print(f"   Capturando amostra do Monitor {i}...")
                screenshot = sct.grab(monitor)
                img = np.array(screenshot)
                img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                
                # Salva uma pequena amostra para identificação
                sample_path = f"monitor_{i}_sample.jpg"
                cv2.imwrite(sample_path, img_bgr)
                print(f"   ✅ Amostra salva: {sample_path}")
        
        print("\n" + "─" * 40)
        print("💡 COMO USAR:")
        print("1. Verifique as amostras salvas (monitor_X_sample.jpg)")
        print("2. Identifique qual monitor tem seu jogo/aplicação")
        print("3. No script principal, altere: monitor_alvo = X")
        print("4. Execute o script principal novamente")
        
except Exception as e:
    print(f"❌ Erro: {e}")

input("\nPressione Enter para fechar...")
