from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os

key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

cipher_encrypt = PKCS1_OAEP.new(RSA.import_key(public_key))
cipher_decrypt = PKCS1_OAEP.new(RSA.import_key(private_key))

def encrypt_file(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    chunk_size = 190  # Ukuran chunk, kurang dari 256 bytes karena padding
    encrypted_data = bytearray()
    
    for i in range(0, len(file_data), chunk_size):
        chunk = file_data[i:i+chunk_size]
        encrypted_chunk = cipher_encrypt.encrypt(chunk)
        encrypted_data.extend(encrypted_chunk)
    
    return encrypted_data

def decrypt_file(file_path):
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    
    chunk_size = 256  # Ukuran chunk hasil enkripsi RSA 2048 bits
    decrypted_data = bytearray()
    
    for i in range(0, len(encrypted_data), chunk_size):
        chunk = encrypted_data[i:i+chunk_size]
        decrypted_chunk = cipher_decrypt.decrypt(chunk)
        decrypted_data.extend(decrypted_chunk)
    
    return decrypted_data
