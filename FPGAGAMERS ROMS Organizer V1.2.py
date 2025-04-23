# FPGAMERS ROMS Organizer
# CRIADO POR: João Alvaro (joao.alvaro@gmail.com)
# DATA DE CRIAÇÃO: 22/05/2025
# VERSÃO: 1.2

import os
import shutil
import zipfile
import time

# Iniciar a contagem do tempo
inicio_tempo = time.time()

# Defina o sistema retro, extensões das ROMs e se deseja compactação
console = "GBA"  # Altere para o sistema desejado
extensoes = ".gba,*.bin"  # Separe as extensões por vírgula
compactar = True  # Defina como True para compactar ou False para apenas mover os arquivos
lista_roms = "lista_roms.txt"  # Nome do arquivo de lista

# Obtém o diretório onde o script está sendo executado
origem = os.path.dirname(os.path.abspath(__file__))

# Criar pasta principal do sistema retro e BIOS
console_destino = os.path.join(origem, f"[{console}] ROMS")
bios_destino = os.path.join(origem, f"[{console}] BIOS")

try:
    os.makedirs(console_destino, exist_ok=True)
    os.makedirs(bios_destino, exist_ok=True)
except OSError as e:
    print(f"Erro ao criar pastas: {e}")

# Criar pastas de A-Z e "0-9" dentro da pasta do console e BIOS
for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    try:
        os.makedirs(os.path.join(console_destino, f"[{console}] ROMS {letra}"), exist_ok=True)
        os.makedirs(os.path.join(bios_destino, f"[{console}] BIOS {letra}"), exist_ok=True)
    except OSError:
        pass

try:
    os.makedirs(os.path.join(console_destino, f"[{console}] ROMS 0-9"), exist_ok=True)
    os.makedirs(os.path.join(bios_destino, f"[{console}] BIOS 0-9"), exist_ok=True)
except OSError:
    pass  # Ignorar erro na criação de pasta

# Convertendo as extensões para uma lista
extensoes_lista = [ext.strip() for ext in extensoes.split(",")]

# Limpar ou criar o arquivo de lista de ROMs
with open(lista_roms, "w") as f:
    f.write("Lista de ROMs organizadas:\n")

# Organizar ROMs e mover ou compactar diretamente na pasta correta
for arquivo in os.listdir(origem):
    caminho_origem = os.path.join(origem, arquivo)

    # Se for BIOS, mover para a pasta BIOS na estrutura A-Z
    if arquivo.startswith("[BIOS]"):
        primeiro_caractere = arquivo[len("[BIOS]")].upper()
        destino_bios = os.path.join(bios_destino, f"[{console}] BIOS {primeiro_caractere}" if primeiro_caractere.isalpha() else f"[{console}] BIOS 0-9")

        try:
            shutil.move(caminho_origem, os.path.join(destino_bios, arquivo))
        except Exception as e:
            print(f"Erro ao mover BIOS {arquivo}: {e}")
        continue

    # Se for ROM válida, processar
    if any(arquivo.endswith(ext) for ext in extensoes_lista):
        primeiro_caractere = arquivo[0].upper()

        if primeiro_caractere.isdigit():
            destino_final = os.path.join(console_destino, f"[{console}] ROMS 0-9")
        elif primeiro_caractere in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            destino_final = os.path.join(console_destino, f"[{console}] ROMS {primeiro_caractere}")
        else:
            destino_final = console_destino  # Caso especial

        # Registrar ROM na lista
        with open(lista_roms, "a") as f:
            f.write(f"{arquivo}\n")

        # Se for CHD, apenas mover (sem compactação)
        if arquivo.endswith(".chd"):
            try:
                shutil.move(caminho_origem, os.path.join(destino_final, arquivo))
            except Exception as e:
                print(f"Erro ao mover {arquivo}: {e}")
            continue

        # Se a compactação estiver ativada, criar um arquivo ZIP com método deflate medium
        if compactar:
            try:
                zip_path = os.path.join(destino_final, f"{arquivo[:-4]}.zip")
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(caminho_origem, arquivo)
                os.remove(caminho_origem)  # Remove o arquivo original após compactação
            except Exception as e:
                print(f"Erro ao compactar {arquivo}: {e}")
        else:
            try:
                shutil.move(caminho_origem, os.path.join(destino_final, arquivo))
            except Exception as e:
                print(f"Erro ao mover {arquivo}: {e}")

print(f"Organização concluída para [{console}] ROMS! {'Compactação ativada.' if compactar else 'Arquivos movidos sem compactação.'}")

# Perguntar ao usuário antes de remover ROMs antigas
if compactar:
    resposta = input("Deseja remover as ROMs antigas que já foram compactadas? (S/N): ").strip().lower()
    if resposta == "s":
        for arquivo in os.listdir(origem):
            if any(arquivo.endswith(ext) for ext in extensoes_lista) and not arquivo.endswith(".chd"):
                try:
                    os.remove(os.path.join(origem, arquivo))
                except Exception as e:
                    print(f"Erro ao remover {arquivo}: {e}")
        print("ROMs antigas foram removidas!")
    else:
        print("ROMs antigas mantidas.")

# Medir tempo de execução
tempo_total = time.time() - inicio_tempo
print(f"Tempo total de execução: {tempo_total:.2f} segundos.")