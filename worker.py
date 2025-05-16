<<<<<<< HEAD
import zmq
import sys


def start_worker(port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    print(f"Worker ativo na porta {port}")

    while True:
        message = socket.recv_string()
        word_count = len(message.split())
        socket.send_string(str(word_count))


if __name__ == "__main__":
    # Ex: python worker.py 5555
    port = int(sys.argv[1])
    start_worker(port)
=======
import zmq
import sys


def start_worker(port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    print(f"Worker ativo na porta {port}")

    while True:
        message = socket.recv_string()
        word_count = len(message.split())
        socket.send_string(str(word_count))


if __name__ == "__main__":
    # Ex: python worker.py 5555
    port = int(sys.argv[1])
    start_worker(port)
>>>>>>> 176e7a8018b40a5415ff4ae0904fe18f2f188609
