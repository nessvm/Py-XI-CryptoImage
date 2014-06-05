import socket

from cryptographic import diffie_hellman
from modules.bmp import BMP
from modules.data_stream import send_msg
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES
from Crypto.Signature import PKCS1_v1_5 as Signature
from Crypto.Hash import SHA

__author__ = 'Ness'


def main():
    # Argument validations
    # Arguments must include flags:
    server_address = '127.0.0.1'#input("Enter server address: ")
    image_path = '..\\..\\img\\' + 'Paisaje.bmp'#input("Enter image name: ")
    local_key_path = '..\\..\\key\\' + 'ness_private.pem'#input("Enter your private key name: ")

    # Image instance
    image = BMP(image_path)

    # Diffie-Hellman process for generating a DES key
    des_key = diffie_hellman((server_address, 12345))

    # Key, cipher, hash and signer creation
    key_file = open(local_key_path, 'r')
    local_key = RSA.importKey(key_file.read())
    key_file.close()

    des_iv = b'12345678'
    des_cipher = DES.new(des_key, DES.MODE_CBC, des_iv)
    signer = Signature.new(local_key)
    plaintext = image.pixels
    hash = SHA.new(bytes(plaintext))

    if len(plaintext) % 8 != 0:
        padding = 8 - (len(plaintext) % 8)
        plaintext += b'x' * padding
    else:
        padding = 0

    ciphertext = des_cipher.encrypt(bytes(plaintext))

    image.pixels = ciphertext
    BMP.create_image(image, "cipher.bmp")

    image_bytes = image.get_bytes()
    signature = signer.sign(hash)

    ct_size = len(image_bytes)
    print(len(image_bytes))
    sig_size = len(signature)

    # Creating the connection with the server and sending
    connection = socket.socket()
    connection.connect((server_address, 12345))
    connection.send('ci'.encode())
    send_msg(connection, image_bytes)
    send_msg(connection, signature)
    connection.send(padding.to_bytes(1, 'little'))


if __name__ == '__main__':
    main()