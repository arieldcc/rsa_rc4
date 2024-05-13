import binascii

def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def RC4(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()
    S = KSA(key)
    gen = PRGA(S)
    encrypted_data = bytes([next(gen) ^ byte for byte in data])
    return binascii.hexlify(encrypted_data)