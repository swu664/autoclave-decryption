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

letter_value_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6,
                     "h": 7, "i": 8, "j": 9, "k": 10, "l": 11, "m": 12,
                     "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18,
                     "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24,
                     "z": 25}

def decrypt_vigenere(ciphertext, key):
    if len(key) != len(ciphertext):
        raise ValueError("Key length must match ciphertext length.")
    
    plaintext = []

    for c, k in zip(ciphertext, key):
        if c.isalpha():
            c_val = letter_value_dict[c.lower()]
            k_val = letter_value_dict[k.lower()]
            p_val = (c_val - k_val) % 26
            p_char = chr(p_val + ord('a'))
            plaintext.append(p_char)
        else:
            plaintext.append(c)

    return plaintext

if __name__ == "__main__":
    parse_ciphertext()