🎬 Reprodutor de Vídeo iOS 6
Um reprodutor de vídeo para Windows com interface nostálgica inspirada no design clássico do iOS 6. Desenvolvido em Python com PyQt, ele traz uma experiência retrô combinada com reprodução fluida de mídias.

🚀 Funcionalidades
📱 Interface retrô estilo iOS 6: Barra de título e controles no estilo clássico.

⏱️ Auto-hide automático: Os controles e a barra superior somem após 3 segundos sem movimento do mouse.

🖱️ Cursor sempre visível: A seta do mouse permanece na tela para fácil navegação.

⏸️ Modo de pausa inteligente: Os controles permanecem visíveis enquanto o vídeo estiver pausado.

📂 Integração com o Windows: Suporte a parâmetros de linha de comando para abrir direto pelo menu "Abrir com".

🛠️ Tecnologias Utilizadas
Python 3

PyQt5

PyInstaller

📦 Como gerar o arquivo .exe
Caso queira empacotar o projeto e gerar um executável próprio para o Windows:

Instale o PyInstaller via terminal:

DOS
pip install pyinstaller
Apague compilações anteriores (se houver):

DOS
rmdir /s /q build dist
Execute o comando de compilação com ícone personalizado:

DOS
pyinstaller --noconsole --onefile --icon=icone.ico --name="Vídeos" player.py
O seu executável pronto estará salvo na pasta dist/Vídeos.exe.

⚙️ Como definir como Reprodutor Padrão no Windows
Para que o Windows abra seus vídeos .mp4 diretamente com este aplicativo:

Mova o arquivo Vídeos.exe para uma pasta definitiva no seu PC (ex: D:\\apps\\reprodutor de video pc).

Clique com o botão direito em qualquer arquivo de vídeo .mp4.

Selecione Abrir com > Escolher outro aplicativo.

Na lista, clique em Escolha um aplicativo no seu PC (ou Procurar outro aplicativo neste PC).

Navegue até a pasta onde deixou o app e selecione o Vídeos.exe.

Selecione a opção Sempre para associar permanentemente os arquivos de vídeo.

📄 Licença
Este projeto é livre para modificações e uso pessoal.

Passo 2: Atualize no GitHub
Salve o arquivo no Bloco de Notas e rode estes comandos no terminal:

DOS
git add README.md
git commit -m "fix: ajusta formatacao do README"
git push origin main


