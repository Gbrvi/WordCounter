import subprocess
import time

def start_peers(num_peers):
    processes = []
    activate_script = r"C:\Users\maria\OneDrive\Documentos\Distribuidos\WordCounter\venv\Scripts\Activate.ps1"

    for i in range(1, num_peers + 1):
        print(f"Iniciando peer{i}...")

        # Comando PowerShell: ativa o venv e executa o peer.py com id e total_peers
        comando = f'& {{ . "{activate_script}"; python peer.py {i} {num_peers} }}'

        # Usar PowerShell separado para cada peer
        p = subprocess.Popen([
            'powershell', 
            '-NoExit',  # Mantenha a janela aberta para ver logs (remova em produção)
            '-Command', 
            comando
        ])

        processes.append(p)
        time.sleep(0.2)  # Pequeno atraso para evitar colisão de portas

    return processes

if __name__ == "__main__":
    NUM_PEERS = 10  # Altere conforme necessário
    procs = start_peers(NUM_PEERS)

    # Se quiser esperar todos terminarem:
    for p in procs:
        p.wait()