import re
import requests
from collections import Counter

def fetch_english_words():
    """
    Fetch English words from an online word list.
    
    Returns:
        set: A set containing English words.
    """
    url = "https://raw.githubusercontent.com/eneko/data-repository/master/data/words.txt"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return set(response.text.upper().splitlines())
        else:
            print("Failed to fetch English words from the online word list.")
            return set()
    except requests.RequestException as e:
        print(f"An error occurred while fetching English words: {e}")
        return set()

def decrypt(ciphertext, shift):
    """
    Decrypt the ciphertext using the Caesar cipher with the given shift.
    
    Args:
        ciphertext (str): The ciphertext to decrypt.
        shift (int): The shift value for the Caesar cipher.
    
    Returns:
        str: The decrypted plaintext.
    """
    decrypted_text = ""
    for char in ciphertext:
        if char.isalpha():
            shifted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            decrypted_text += shifted_char
        else:
            decrypted_text += char
    return decrypted_text

def filter_plaintexts(plaintexts, english_words):
    """
    Filter plaintexts to include only those containing English words.
    
    Args:
        plaintexts (list): List of plaintexts.
        english_words (set): Set of English words.
    
    Returns:
        list: List of plaintexts containing only English words.
    """
    return [plaintext for plaintext in plaintexts if all(word.upper() in english_words for word in re.findall(r'\b\w+\b', plaintext))]

def frequency_analysis(plaintexts):
    """
    Perform frequency analysis on the plaintexts and return the most frequent one.
    
    Args:
        plaintexts (list): List of plaintexts.
    
    Returns:
        tuple: A tuple containing the most frequent plaintext and its frequency count.
    """
    frequency_counter = Counter(plaintexts)
    return frequency_counter.most_common(1)[0]

def decrypt_and_analyze(ciphertext):
    """
    Decrypt the ciphertext for all shifts, filter plaintexts, and perform frequency analysis.
    
    Args:
        ciphertext (str): The ciphertext to decrypt.
    
    Returns:
        tuple: A tuple containing the most likely plaintext and its frequency count.
            Returns None if no meaningful English words are found in the decrypted plaintexts.
    """
    english_words = fetch_english_words()
    if not english_words:
        print("No English words found. Aborting decryption.")
        return None
    
    plaintexts = [decrypt(ciphertext, shift) for shift in range(26)]
    filtered_plaintexts = filter_plaintexts(plaintexts, english_words)
    if filtered_plaintexts:
        return frequency_analysis(filtered_plaintexts)
    else:
        print("No meaningful English words found in the decrypted plaintexts.")
        return None

def main():
    ciphertext = input("Enter the ciphertext: ").upper()
    result = decrypt_and_analyze(ciphertext)
    if result:
        plaintext, frequency = result
        print("Decrypted plaintext with the highest frequency score:", plaintext)
        print("Frequency score:", frequency)
    else:
        pass  # Do nothing if no meaningful English words are found

if __name__ == "__main__":
    main()
