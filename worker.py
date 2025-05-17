import zmq
import sys


def start_worker(name):
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.identity = name.encode()
    print("Conectando ao master...")
    socket.connect("tcp://localhost:6000")

    
    print(f"{name} ativo no master")

    print("Conectado. Enviando READY...")

    # Informa ao master que está pronto
    socket.send_multipart([b"READY"])
    print("READY enviado. Aguardando chunk...")

    while True:
        parts = socket.recv_multipart()

        if len(parts) == 1:
            content = parts[0].decode()
            print("Chunk recebido.")
            word_count = len(content.split())
            socket.send_multipart([str(word_count).encode()])
            break  # Termina após processar um chunk


if __name__ == "__main__":
    name = sys.argv[1]
    start_worker(name)
    print(f"{name} conectado ao master")
