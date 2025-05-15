import os

class File():
    """Function Class to manage file """
    def _split_file(self, file_path, num_chunk=3):
        """Split in X chucks files"""
        with open(file_path, 'r') as f:
            words = f.read().split(" ")

        total_words = len(words) # Count all the words
        chunk_size = total_words // num_chunk # Split it on X num_chunk
        remains_words = total_words % num_chunk #If remains some words

        self._join_words(total_words, num_chunk, chunk_size, words, remains_words)


    def _join_words(self, num_chunk, chunk_size, words, remains_words):
        """Join the words into num_chunks"""
        inicio = 0
        for i in range(num_chunk):
            fim = inicio + chunk_size + (1 if i < remains_words else 0)

            word_in_chunk = words[inicio:fim]

            file_name = f"chunk{i+1}.txt"

            with open(file_name, 'w', encoding='utf-8') as f_chunk:
                f_chunk.write(" ".join(word_in_chunk))

            inicio = fim
if __name__ == "__main__":
    file = File()
    file._split_file("file.txt")




