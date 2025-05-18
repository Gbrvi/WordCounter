import zmq
import os
import time


def split_file(file_path, num_chunks):
    """Function to split file into chunk """
    with open(file_path, 'r', encoding='utf-8') as f:
        words = f.read().split()

    total = len(words) # Total words
    chunk_size = total // num_chunks # Divide to X chunk
    remainder = total % num_chunks # It can remain some words

    os.makedirs("chunks", exist_ok=True) # Create "Chunk" folder

    start = 0
    for i in range(num_chunks):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunk_words = words[start:end]
        chunk_path = os.path.join("chunks", f"chunk{i+1}.txt")
        with open(chunk_path, 'w', encoding='utf-8') as chunk_file:
            chunk_file.write(" ".join(chunk_words))
        start = end


def main():
    # Create Socket pattern ROUTER
    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind("tcp://*:6000") # listen to port 6000

    num_workers = 1 # How many works the system will have
    start_split_time = time.perf_counter() # To count how many time it spends to split
    split_file("file.txt", num_workers)
    end_split_time = time.perf_counter()

    poller = zmq.Poller() # Poller to async messages
    poller.register(socket, zmq.POLLIN)

    print("Aguardando workers se conectarem...\n")

    workers_ready = set() # Workers connected
    chunks_sent = 0 
    total_words = 0
    responses = 0 

    start_time = time.perf_counter() # To calculate the time to count the words

    while responses < num_workers: # Wait for all messages 
        events = dict(poller.poll(timeout=1000)) # Check if it has message for each 1 seg
        if socket in events:
            msg = socket.recv_multipart() # Get message
            worker_id = msg[0] # Get Worker_id (ROUTER patterns)

            # Worker is ready and request chunk
            if len(msg) == 2 and msg[1] == b"READY":
                if worker_id not in workers_ready:
                    workers_ready.add(worker_id)
                    print(f"{worker_id.decode()} está pronto")

                    # Send chunk to worker 
                    chunks_sent += 1
                    chunk_path = os.path.join("chunks", f"chunk{chunks_sent}.txt")
                    with open(chunk_path, 'r', encoding='utf-8') as f:
                        chunk_data = f.read()
                    socket.send_multipart([worker_id, chunk_data.encode()])

            # Worker sent response (word counter)
            elif len(msg) == 2:
                response = int(msg[1].decode())
                print(f"{worker_id.decode()} respondeu: {response} palavras")
                total_words += response
                responses += 1

    end_time = time.perf_counter()
    print(f"\nTotal de palavras no arquivo: {total_words}")
    print(f"Tempo pra contar palavras: {end_split_time - start_split_time:.2f}s")
    print(f"Tempo pra separar : {end_time - start_time:.2f}s")


if __name__ == "__main__":
    main()
