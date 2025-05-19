import zmq
import sys
import time
import threading

PORT_BASE = 7000  # Each peer communicates through this base port + id


def load_chunk(file_path, peer_id, total_peers):
    with open(file_path, 'r', encoding='utf-8') as f:
        words = f.read().split()

    total = len(words)
    chunk_size = total // total_peers
    remainder = total % total_peers

    start = (chunk_size * (peer_id - 1)) + min(peer_id - 1, remainder)
    end = start + chunk_size + (1 if peer_id <= remainder else 0)

    return words[start:end]


def publish_thread(context, peer_id, my_count):
    pub = context.socket(zmq.PUB)
    pub.bind(f"tcp://*:{PORT_BASE + peer_id}")
    time.sleep(1)  # Give time for SUBs to connect
    print(f"[{peer_id}] Publishing my count: {my_count}")
    pub.send_string(f"{peer_id} {my_count}")
    pub.close()


def subscribe_thread(context, peer_id, total_peers, results):
    sub = context.socket(zmq.SUB)
    sub.setsockopt_string(zmq.SUBSCRIBE, '')

    # Connect to other peers (except itself)
    for i in range(1, total_peers + 1):
        if i == peer_id:
            continue
        sub.connect(f"tcp://localhost:{PORT_BASE + i}")

    print(f"[{peer_id}] Waiting for counts from other peers...")
    while len(results) < total_peers:
        msg = sub.recv_string()
        sender_id, count = msg.split()
        sender_id = int(sender_id)
        count = int(count)

        if sender_id not in results:
            results[sender_id] = count

    sub.close()


def main():
    peer_id = int(sys.argv[1])
    total_peers = int(sys.argv[2])

    chunk_words = load_chunk("file.txt", peer_id, total_peers)
    my_count = len(chunk_words)

    context = zmq.Context()
    results = {peer_id: my_count}

    t_pub = threading.Thread(target=publish_thread, args=(context, peer_id, my_count))
    t_sub = threading.Thread(target=subscribe_thread, args=(context, peer_id, total_peers, results))

    t_pub.start()
    t_sub.start()

    t_pub.join()
    t_sub.join()

    total_word_count = sum(results.values())
    print(f"Final total word count: {total_word_count}")


if __name__ == "__main__":
    main()
