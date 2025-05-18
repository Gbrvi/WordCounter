import subprocess
import time

def start_workers(num_workers):
    processes = []
    activate_script = r"C:\Users\gvalm\Documents\Projetos\WordCounter\myenv\Scripts\Activate.ps1"
    
    for i in range(1, num_workers + 1):
        name = f"worker{i}"
        print(f"Iniciando {name}... \n")

        # Comando PowerShell que ativa o env e roda o worker
        comando = f'& {{ . "{activate_script}"; python worker.py {name} }}'        
        p = subprocess.Popen([
            'powershell', 
            '-NoExit',  # ou remova para testes
            '-Command', 
            comando
            ])

        processes.append(p)
        time.sleep(1)

    return processes

if __name__ == "__main__":
    NUM_WORKERS = 10 # Altere conforme necessário
    procs = start_workers(NUM_WORKERS)

    # Opcional: esperar todos terminarem (útil para teste)
    for p in procs:
        p.wait()