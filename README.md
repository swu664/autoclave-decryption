# autoclave-decryption

A python tool for decrypting an autoclave (autokey) ciphertext with preserved spaces and punctuation, given the initial passphrase(key) length.

**Installation**

Clone the repository.  
- For instructions, see https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository.

**Usage**

1. Copy and paste the ciphertext you would like to decrypt into ciphertext.txt file.
2. Run main.py.
- The terminal should display an indexed list of the words from your ciphertext and your current plaintext.
3. Follow the prompts in the terminal:
- Enter the length of the original key
- Enter word index to guess (or 'q' to quit)
  - Using Visual Studio Code, have your ciphertext.txt file open. 
  - With the word you want to guess in your current plaintext, use the line numbers of Current Plaintext and the ciphertext.txt file to identify the corresponding ciphertext word.
  - Then use control+f or command+f in terminal to find the ciphertext word and it's word index in the word list, Ciphertext Words.
4. At this point, the intention is that you use the number of letters in any encrypted ciphertext word to guess potential words of the same number of letters.
- If your guess is correct, you will notice that Current Plaintext will propogate your guess in a way that the letters make sense, given the preserved spaces and punctuation, i.e., making it easier to guess the rest of your ciphertext.
- If your guess is incorrect, it is likely that the resulting plaintext will consist of random letters. You will have the opportunity to undo that guess, given the prompt "Enter 'r' to reverse the guess (or any key to continue)".
5. If the plaintext that corresponds to the initial key is complete, when you exit using 'q', the inital key will be recovered and displayed.

**Features**
- Decrypts an autoclave (autokey) ciphertext with preserved spaces and punctuation, given the initial passphrase(key) length.
  - Propogates each guess automatically
  - Safely handles decryption at the start and end of the ciphertext
- Recovers inital key, if the plaintext that corresponds to the initial key is complete.
- Allows users to undo the most recent guess
