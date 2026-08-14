import sys
import os
import winreg

def registrar_player():
    # Detecta onde a pasta está rodando no momento
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    python_exe = sys.executable
    script_player = os.path.join(pasta_atual, "player.py")

    # Comando executado pelo Windows ao clicar em um vídeo
    comando = f'"{python_exe}" "{script_player}" "%1"'
    
    nome_programa = "iOS6VideoPlayer"
    descricao = "iOS 6 Video Player (Python)"

    try:
        # 1. Registrar no ProgIDs
        prog_key_path = f"Software\\Classes\\{nome_programa}"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, prog_key_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, descricao)

        # Command key
        cmd_key_path = f"{prog_key_path}\\shell\\open\\command"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_key_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, comando)

        # 2. Adicionar à lista de "OpenWithList" para extensão .mp4
        assoc_key_path = f"Software\\Classes\\.mp4\\OpenWithProgids"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, assoc_key_path) as key:
            winreg.SetValueEx(key, nome_programa, 0, winreg.REG_NONE, b'')

        print("=== SUCESSO! ===")
        print("O player foi registrado no Windows.")
        print("Agora clique com botão direito em qualquer vídeo .mp4 -> 'Abrir com' -> 'Escolher outro aplicativo' e selecione o iOS 6 Video Player!")

    except Exception as e:
        print(f"Erro ao registrar no Windows: {e}")

if __name__ == "__main__":
    registrar_player()