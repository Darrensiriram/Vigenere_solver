# Global variables
import english_quadgrams as quadgrams
import random
import string

ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
SURVIVAL_RATE = 0.01


def group_info():
    # return [
    #     ('1014917', 'Thijs Verkade', 'DINF-1A'),
    #     ('0999506', 'Darren Siriram', 'DINF-1A'),
    # ]
    class_info = ('1014917', 'Thijs Verkade', 'DINF-1A'), ('0999506', 'Darren Siriram', 'DINF-1A')
    return class_info


def encrypt_vigenere(plaintext, key):
    enc_string = ""

    # Expands the encryption key to make it longer than the inputted string
    expanded_key = key
    expanded_key_length = len(expanded_key)

    while expanded_key_length < len(plaintext):
        # Adds another repetition of the encryption key
        expanded_key = expanded_key + key
        expanded_key_length = len(expanded_key)

    key_position = 0
    for letter in plaintext:
        if letter in ALPHABET:
            # cycles through each letter to find it's numeric position in the alphabet
            position = ALPHABET.find(letter)

            # moves along key and finds the characters value
            key_character = expanded_key[key_position]
            key_character_position = ALPHABET.find(key_character)
            key_position = key_position + 1

            # changes the original of the input string character
            new_position = position + key_character_position
            if new_position > 26:
                new_position = new_position - 26
            new_character = ALPHABET[new_position]

            # Check if letter is upper
            if letter.isupper():
                new_character = new_character.upper()
            else:
                new_character = new_character.lower()

            enc_string = enc_string + new_character
        else:
            enc_string = enc_string + letter
    return enc_string


def decrypt_vigenere(ciphertext, key):
    dec_string = ""

    # Expands the encryption key to make it longer than the inputted string
    expanded_key = key
    expanded_key_length = len(expanded_key)

    while expanded_key_length < len(ciphertext):
        # Adds another repetition of the encryption key
        expanded_key = expanded_key + key
        expanded_key_length = len(expanded_key)
    key_position = 0

    for letter in ciphertext:
        if letter in ALPHABET:
            # cycles through each letter to find it's numeric position in the alphabet
            position = ALPHABET.find(letter)

            # moves along key and finds the characters value
            key_character = expanded_key[key_position]
            key_character_position = ALPHABET.find(key_character)
            key_position = key_position + 1

            # changes the original of the input string character
            new_position = position - key_character_position
            if new_position > 26:
                new_position = new_position - 26
            new_character = ALPHABET[new_position]

            # Check if letter is upper
            if letter.isupper():
                new_character = new_character.upper()
            else:
                new_character = new_character.lower()

            dec_string = dec_string + new_character
        else:
            dec_string = dec_string + letter
    return dec_string


def quadgram_fitness(text):
    new_text = ''
    new_score = 0

    for i in range(len(text)):
        count = 0
        if text[i] in ALPHABET:
            while len(new_text) < 4:
                new_index = i + count
                if new_index in range(len(text)):
                    new_val = text[new_index]
                    if new_val in ALPHABET:
                        new_text += new_val.lower()
                    count += 1
                else:
                    return new_score
            if new_text in quadgrams.quadgram_score:
                new_score = new_score + quadgrams.quadgram_score[new_text]
            else:
                new_score = new_score + 23
            new_text = ''

def get_random_word(y):
    result = ''.join(random.choice(string.ascii_lowercase) for x in range(y))
    return result

def solve_vigenere(ciphertext, key_len):
    key = get_random_word(key_len)
    best_key = key
    result = decrypt_vigenere(ciphertext, key)
    best_result = result
    last_fitness = quadgram_fitness(result)
    best_fitness = last_fitness

    for i in range(1000 * key_len ** 2):
        index_to_change = random.randint(0, len(key) - 1)
        temp_key = key[:index_to_change] + get_random_word(1) + key[index_to_change + 1:]
        temp_result = decrypt_vigenere(ciphertext, temp_key)
        temp_fitness = quadgram_fitness(temp_result)

        if temp_fitness < last_fitness:
            last_fitness = temp_fitness
            key = temp_key
            result = temp_result
            if temp_fitness < best_fitness:
                best_key = key
                best_result = result
                best_fitness = temp_fitness
        else:
            survives = random.uniform(0, 1) < SURVIVAL_RATE
            if survives:
                key = temp_key
                last_fitness = temp_fitness

    return best_key, best_result
