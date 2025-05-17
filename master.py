import zmq
import os
import time


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
    socket = context.socket(zmq.ROUTER)
    socket.bind("tcp://*:6000")

    num_workers = 5
    split_file("C:\Users\gvalm\Desktop\file.txt", num_workers)

    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    print("Aguardando workers se conectarem...\n")

    workers_ready = set()
    chunks_sent = 0
    total_words = 0
    responses = 0

    start_time = time.perf_counter()

    while responses < num_workers:
        events = dict(poller.poll())
        if socket in events:
            msg = socket.recv_multipart()

            worker_id = msg[0]

            # Worker se identificou e está pronto
            if len(msg) == 2 and msg[1] == b"READY":
                workers_ready.add(worker_id)
                print(f"{worker_id.decode()} está pronto")

                # Enviar chunk se ainda não enviou
                if chunks_sent < num_workers:
                    with open(f"chunks/chunk{chunks_sent + 1}.txt", 'r', encoding='utf-8') as f:
                        chunk_data = f.read()
                    socket.send_multipart([worker_id, chunk_data.encode()])
                    chunks_sent += 1

            # Worker enviou resultado
            elif len(msg) == 2:
                response = int(msg[1].decode())
                print(f"{worker_id.decode()} respondeu: {response} palavras")
                total_words += response
                responses += 1

    end_time = time.perf_counter()
    print(f"\nTotal de palavras no arquivo: {total_words}")
    print(f"Tempo total: {end_time - start_time:.2f}s")


if __name__ == "__main__":
    main()
