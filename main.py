import re

def parse_ciphertext():
    file_path = "ciphertext.txt"
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            words = content.replace('.', '').split()
            word_dict = {word: i for i, word in enumerate(words)}
            plaintext = re.sub(r"[a-zA-Z]", '_', content)
            print("Word Dictionary:")
            for word, i in word_dict.items():
                print(f"{word}: {i}")
            print(f"\nCurrent Plaintext: \n{plaintext}")

    except FileNotFoundError:
        print("File not found. Please check the path and try again.")

if __name__ == "__main__":
    parse_ciphertext()
