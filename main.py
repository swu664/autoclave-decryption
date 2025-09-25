import re

def display_plaintext(ciphertext_words, ciphertext_letters):
    letter_index = 0
    plaintext = ""
    for word_index in ciphertext_words:
        plaintext += " "
        for char in ciphertext_words.get(word_index):
            if char.isalpha():
                if ciphertext_letters[letter_index][1] == 0:
                    plaintext += "_"
                else:
                    plaintext += ciphertext_letters[letter_index][0]
                letter_index +=1
            elif char == "<":
                plaintext += "\n"
                break
            else:
                plaintext += char
    return plaintext

def parse_ciphertext():
    file_path = "ciphertext.txt"
    try:
        with open(file_path, 'r') as f:
            content = f.read()

            #create mapping of indices to ciphertext words
            words = content.replace("\n","<nl> ").split()
            ciphertext_words = {i: word for i, word in enumerate(words)}
            print("Ciphertext Words:")
            for i, word in ciphertext_words.items():
                print(f"{i}: {word}")
            
            #create mapping of indices to ciphertext letters
            letters = re.findall(r'[a-zA-Z]', content)
            ciphertext_letters = {i: [letter, 0] for i, letter in enumerate(letters)}

            print(f"\n{content}")
            print(f"\nCurrent Plaintext: \n{display_plaintext(ciphertext_words, ciphertext_letters)}")

    except FileNotFoundError:
        print("File not found. Please check the path and try again.")

    return content, ciphertext_words, ciphertext_letters

LETTER_VALUE_DICT = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6,
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
            c_val = LETTER_VALUE_DICT[c.lower()]
            k_val = LETTER_VALUE_DICT[k.lower()]
            p_val = (c_val - k_val) % 26
            p_char = chr(p_val + ord('a'))
            plaintext.append(p_char)
        else:
            plaintext.append(c)

    return plaintext

if __name__ == "__main__":
    parse_ciphertext()