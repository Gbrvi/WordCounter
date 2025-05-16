import zmq
import os


def split_file(file_path, num_chunks):
    with open(file_path, 'r', encoding='utf-8') as f:
        words = f.read().split()

    total = len(words)
    chunk_size = total // num_chunks
    remainder = total % num_chunks

    os.makedirs("chunks", exist_ok=True)

    start = 0
    for i in range(num_chunks):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunk_words = words[start:end]
        with open(f"chunks/chunk{i+1}.txt", 'w', encoding='utf-8') as chunk_file:
            chunk_file.write(" ".join(chunk_words))
        start = end


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    num_workers = 3
    split_file("file.txt", num_workers)

    total_words = 0

    for i in range(num_workers):
        # Envia o conteúdo do chunk para o worker
        with open(f"chunks/chunk{i+1}.txt", 'r', encoding='utf-8') as chunk_file:
            chunk_data = chunk_file.read()

        # Cada worker numa porta diferente
        socket.connect(f"tcp://localhost:{5555 + i}")
        socket.send_string(chunk_data)

        # Aguarda a contagem de palavras
        word_count = int(socket.recv_string())
        print(f"Chunk {i+1} tem {word_count} palavras.")
        total_words += word_count

        socket.disconnect(f"tcp://localhost:{5555 + i}")

    print(f"\nTotal de palavras no arquivo: {total_words}")


if __name__ == "__main__":
    main()
