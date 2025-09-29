import re, string

def display_plaintext(ciphertext_words, plaintext_letters):
    letter_index = 0
    plaintext = ""
    for word_index in ciphertext_words:
        plaintext += " "
        for char in ciphertext_words.get(word_index):
            if char in string.ascii_letters:
                plaintext += plaintext_letters[letter_index]
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
            ciphertext_letters = re.findall(r'[a-zA-Z]', content)

            plaintext_letters = ["_"] * len(ciphertext_letters)

            print(f"\n{content}")
            print(f"\nCurrent Plaintext: \n{display_plaintext(ciphertext_words, plaintext_letters)}")

    except FileNotFoundError:
        print("File not found. Please check the path and try again.")

    return content, ciphertext_words, ciphertext_letters, plaintext_letters

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
        if k == "_":
            return "Incomplete plaintext – Unable to recover inital key."
        if c.isalpha():
            c_val = LETTER_VALUE_DICT[c.lower()]
            k_val = LETTER_VALUE_DICT[k.lower()]
            p_val = (c_val - k_val) % 26
            p_char = chr(p_val + ord('a'))
            plaintext.append(p_char)
        else:
            plaintext.append(c)

    return "".join(plaintext)

def clean(text):
    text = re.sub(r'<nl>', "", text)
    text = re.findall(r'[a-zA-Z+]', text)
    return "".join(text).lower()

def update_backwards(word_index, key_guess, original_key_length):
    #find start position
    letter_index = 0
    for i in range(word_index):
        letter_index += len(clean(ciphertext_words[i]))
    
    num_updates = (letter_index // original_key_length) + 1

    current_key = key_guess
    next_key = current_key
    current_ciphertext = ciphertext_words[word_index]
    next_ciphertext = current_ciphertext
    at_beginning = False

    for j in range(num_updates):
        temp = 0
        current_ciphertext = next_ciphertext
        next_ciphertext = ""
        current_key = next_key
        intermediate_key = ""
        intermediate_ciphertext = ""
        for i, c in enumerate(current_key):
            #update current ciphertext_letters
            plaintext_letters[letter_index + temp] = c

            #retrieve next ciphertext segment to decode
            if letter_index - original_key_length + temp >= 0:
                at_beginning = False
                next_ciphertext += ciphertext_letters[letter_index - original_key_length + temp]
                intermediate_key += c
                intermediate_ciphertext += current_ciphertext[i]
            else:
                at_beginning = True
            temp += 1
            if i == len(current_key) - 1 and intermediate_key and intermediate_ciphertext:
                current_key = intermediate_key
                current_ciphertext = intermediate_ciphertext
        if at_beginning:
            break
        next_key = clean(decrypt_vigenere(clean(current_ciphertext), current_key))
        letter_index -= original_key_length
    
    if letter_index < 0:
        for i, c in enumerate(next_key):
            plaintext_letters[i] = c

def update_forwards(word_index, key_guess, original_key_length):
    #find start position
    letter_index = 0
    for i in range(word_index):
        letter_index += len(clean(ciphertext_words[i]))
    
    num_updates = ((len(ciphertext_letters) - letter_index) // original_key_length) + 1

    current_key = key_guess
    next_key = current_key
    current_ciphertext = ciphertext_words[word_index]
    next_ciphertext = current_ciphertext
    at_end = False

    for j in range(num_updates):
        temp = 0
        current_ciphertext = next_ciphertext
        next_ciphertext = ""
        current_key = next_key
        intermediate_key = ""
        intermediate_ciphertext = ""
        for i, c in enumerate(current_key):
            #update plaintext_letters
            plaintext_letters[letter_index + temp] = c
            
            #retrieve next ciphertext segment to decode
            if letter_index + temp + original_key_length < len(ciphertext_letters):
                at_end = False
                next_ciphertext += ciphertext_letters[letter_index + original_key_length + temp]
                intermediate_key += c
                intermediate_ciphertext += current_ciphertext[i]
            else:
                at_end = True
            temp += 1
            if i == len(current_key) - 1 and intermediate_key and intermediate_ciphertext:
                current_key = intermediate_key
                current_ciphertext = intermediate_ciphertext
                next_key = clean(decrypt_vigenere(clean(next_ciphertext), current_key))
                letter_index += original_key_length  
        if at_end:
            break

    last_index = len(plaintext_letters) - 1
    end_index = len(next_key) - (letter_index + len(next_key) - last_index)
    if letter_index + len(next_key) > last_index:
        end_key = next_key[0:end_index + 1]
        for i, c in enumerate(end_key):
            plaintext_letters[last_index - end_index + i] = c

if __name__ == "__main__":
    content, ciphertext_words, ciphertext_letters, plaintext_letters = parse_ciphertext()

    length_of_original_key = int(input("\nEnter the length of the original key: "))

    while True:
        user_input = input("\nEnter word index to guess (or 'q' to quit): ")

        if user_input.lower() == 'q':
            print("Exiting decryption attempt.")
            break

        word_index = int(user_input)
        print(f"Ciphertext word [{word_index}]: {ciphertext_words[word_index]}")
        key = input("Enter your plaintext guess: ")

        if len(key) != len(clean(ciphertext_words.get(word_index, ''))):
            raise ValueError("Key length must match ciphertext length.")
        
        previous_state = plaintext_letters.copy()

        update_backwards(word_index, key, length_of_original_key)
        update_forwards(word_index, key, length_of_original_key)

        print(f"\n{content}")
        print(f"\n{display_plaintext(ciphertext_words, plaintext_letters)}")

        reverse_guess = input("\nEnter 'r' to reverse the guess (or any key to continue): ")
        if reverse_guess.lower() == 'r':
            plaintext_letters = previous_state
            print(f"\n{display_plaintext(ciphertext_words, plaintext_letters)}")
        else:
            continue

    print(f"Initial key: {decrypt_vigenere(''.join(ciphertext_letters[0:length_of_original_key]), ''.join(plaintext_letters[0:length_of_original_key]))}")