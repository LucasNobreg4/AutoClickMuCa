# 🎯 IMAGE DETECTOR - INSTRUÇÕES DE USO

## 📦 ARQUIVOS CRIADOS:

✅ **ImageDetector.exe** (73.4 MB)
   - Versão com console (mostra mensagens e estatísticas)
   - Recomendada para uso normal

✅ **ImageDetector_Silent.exe**
   - Versão sem console (roda em segundo plano)
   - Para uso discreto

## 📂 ESTRUTURA DE PASTAS NECESSÁRIA:

```
Sua_Pasta/
├── ImageDetector.exe          (executável principal)
├── img_Gemstone.jpg          (imagens a detectar)
├── img_Jewel.jpg
├── img_bog.jpg
├── img_cob.jpg
├── img_soa.jpg
├── sound_Gemstone.mp3        (sons a tocar)
├── android_end_call_tone.mp3
└── historico_deteccoes.txt   (criado automaticamente)
```

## 🚀 COMO USAR:

### INSTALAÇÃO:
1. Crie uma pasta em qualquer lugar (ex: "C:\MeuDetector\")
2. Copie o **ImageDetector.exe** para essa pasta
3. Copie todas as **imagens (.jpg)** para a mesma pasta
4. Copie todos os **sons (.mp3)** para a mesma pasta

### EXECUÇÃO:
1. Execute o **ImageDetector.exe** (duplo clique)
2. O programa detectará automaticamente seus monitores
3. Começará a monitorar imediatamente
4. Quando detectar uma imagem, tocará o som correspondente

### PARANDO:
- Pressione **Ctrl+C** no console para parar
- O programa mostrará estatísticas completas
- Salvará o histórico em "historico_deteccoes.txt"

## ⚙️ CONFIGURAÇÕES:

Para alterar configurações, você precisa editar o arquivo Python original:

- **monitor_alvo**: Qual monitor capturar (1, 2, 3 ou 0 para todos)
- **porcentagem_setada**: Sensibilidade da detecção (0.77 = 77%)
- **escalas_rapidas**: Tamanhos testados [1.0, 0.8, 1.2]

### 🎨 PERSONALIZAR ÍCONE:

Para usar um ícone personalizado no executável:

1. **Converter imagem para ícone:**
   ```bash
   python criar_icone.py
   # Escolha opção 2 e informe sua imagem
   ```

2. **Ou usar ícone pronto:**
   - Coloque o arquivo `.ico` na pasta do projeto
   - Nomes reconhecidos: `detector_icon.ico`, `icon.ico`, `app_icon.ico`

### 🖱️ CONFIGURAR AUTO-CLIQUE:

Para configurar o clique automático:

1. **Configurador automático:**
   ```bash
   python configurar_clique.py
   # Interface simples para ajustar todas as opções
   ```

2. **Configuração manual no código:**
   ```python
   auto_click_habilitado = True    # True/False
   tipo_click = 'left'            # 'left', 'right', 'middle', 'double'
   click_delay = 0.1              # Segundos
   click_offset_x = 0             # Pixels
   click_offset_y = 0             # Pixels
   ```

3. **Testar configuração:**
   - Execute o detector normalmente
   - Quando detectar item, verá: "🎮 Item coletado automaticamente!"

## 📊 FUNCIONALIDADES:

✅ **Detecção em tempo real** de múltiplas imagens
✅ **Suporte a múltiplos monitores** (até 3 detectados)
✅ **Histórico completo** de detecções com horários
✅ **Estatísticas automáticas** (total, ranking, média)
✅ **Sons personalizados** para cada tipo de imagem
✅ **Otimização de performance** (detecção rápida)
✅ **Salvamento automático** do histórico
✅ **🖱️ CLIQUE AUTOMÁTICO** - Nova funcionalidade!
   - Detecta item na tela
   - Calcula posição do centro
   - Clica automaticamente para coletar
   - Configurável (habilitar/desabilitar, tipo, delay, offset)

## 🔧 REQUISITOS:

- ✅ Windows 10/11
- ✅ Não precisa Python instalado
- ✅ Não precisa bibliotecas adicionais
- ✅ Funciona offline

## ❓ SOLUÇÃO DE PROBLEMAS:

**Erro "não encontra imagens":**
- Verifique se as imagens .jpg estão na mesma pasta do .exe

**Erro "não encontra sons":**
- Verifique se os arquivos .mp3 estão na mesma pasta do .exe

**Não detecta no monitor correto:**
- Execute primeira vez para ver quais monitores foram detectados
- Anote qual monitor você quer usar
- Pare o programa (Ctrl+C)
- Edite o código Python e refaça o executável

**Detecção muito sensível/pouco sensível:**
- Ajuste porcentagem_setada no código (menor = mais sensível)

**Quer ícone personalizado:**
- Execute: `python criar_icone.py`
- Converta sua imagem favorita para .ico
- Rebuilde o executável com: `python build_exe.py`

**Executável muito grande:**
- Normal (70+ MB devido às bibliotecas OpenCV, PyGame, etc.)
- Para reduzir: remova imports não usados do código

**Auto-clique não funciona:**
- Verifique se `auto_click_habilitado = True`
- Ajuste offset se clicando na posição errada
- Use `configurar_clique.py` para facilitar

**Clicando na posição errada:**
- Ajuste `click_offset_x` e `click_offset_y`
- Valores positivos movem para direita/baixo
- Valores negativos movem para esquerda/cima

## 🛠️ FERRAMENTAS INCLUÍDAS:

- **build_exe.py**: Criar/atualizar executável
- **criar_icone.py**: Converter imagens para ícones
- **configurar_clique.py**: Configurar auto-clique facilmente
- **limpar_builds.py**: Limpar arquivos temporários
- **test_monitores.py**: Testar configuração de monitores

## 📱 CONTATO:

Para dúvidas ou melhorias, consulte o código Python original.

---
*Executável criado em: 28/07/2025*
*Versão: PyInstaller 6.14.2*
