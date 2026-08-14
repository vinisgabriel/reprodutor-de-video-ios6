# Reprodutor de Vídeo iOS 6

Uma aplicação em Python que simula a interface clássica e nostálgica do reprodutor de mídia do iOS 6 para Windows, utilizando PyQt.

O aplicativo oferece reprodução fluida de mídias com controles customizados, auto-hide inteligente e integração completa com o sistema operacional para abertura direta de arquivos.

---

## 🚀 Funcionalidades

- **Interface Retrô iOS 6:** Estilização visual fiel aos elementos de UI e controles clássicos do iOS 6.
- **Controles com Auto-Hide:** Barras de navegação e controles somem automaticamente após 3 segundos de inatividade do mouse.
- **Modo de Pausa Inteligente:** Mantém a interface visível permanentemente enquanto o vídeo estiver pausado.
- **Cursor Dinâmico:** Garantia de visibilidade contínua do cursor do mouse durante a navegação sobre o vídeo.
- **Suporte a Linha de Comando (sys.argv):** Aceita o caminho de arquivos de vídeo como parâmetro para integração com o menu "Abrir com" do Windows.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **PyQt5** (Construção da interface gráfica, eventos e player de mídia)
- **PyInstaller** (Empacotamento do script Python em executável nativo do Windows)

---

## 📦 Como Gerar o Executável (.exe)

### Pré-requisitos

Certifique-se de ter o PyInstaller instalado:

`pip install pyinstaller`

### Compilação

Para compilar o projeto gerando um executável único e com ícone personalizado, execute:

`pyinstaller --noconsole --onefile --icon=icone.ico --name="Vídeos" player.py`

O arquivo final será gerado dentro da pasta `dist/Vídeos.exe`.

---

## ⚙️ Configuração no Windows ("Abrir com")

Para definir a aplicação como reprodutor padrão para arquivos de vídeo (.mp4):

1. Mova o arquivo `Vídeos.exe` para a pasta de sua preferência (ex: `D:\apps\reprodutor de video pc\`).
2. Clique com o botão direito em qualquer arquivo `.mp4` > **Abrir com** > **Escolher outro aplicativo**.
3. Selecione **Escolher um aplicativo no seu PC**, navegue até a pasta e escolha o `Vídeos.exe`.
4. Marque a opção **Sempre** para vincular a extensão permanentemente.