__author__ = 'Ness'

import mmap
import os
import threading
import sys

from socketserver import *
from modules.bmp import BMP
from modules.data_stream import recv_msg
from Crypto.Random import random
from Crypto.Hash import SHA
from Crypto.Cipher import DES
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature


def main():
    # Creating server
    host = input("Enter local server address: ")
    port = 12345
    server = ThreadingTCPServer(
        (host, port),
        ValidatorRequestHandler
    )
    server.serve_forever()


class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    pass


class ValidatorRequestHandler(StreamRequestHandler):
    def handle(self):
        print('Processing request from {}'.format(self.client_address[0]))
        type = self.connection.recv(2)
        req = type.decode()

        if req == 'dh':
            print('Processing Diffie-Hellman')
            g = random.randint(100, 9999999)
            n = random.randint(10000000, 99999999)

            gn_pair = str(g) + ' ' + str(n)
            self.connection.send(gn_pair.encode())  # Send byte codification of g and n
            remote_k = int.from_bytes(self.connection.recv(128), byteorder='little', signed=False)

            # Prompt for local 'e' value and generate local key from g^e mod n
            local_exponent = random.randint(100, 10000)
            local_k = pow(g, local_exponent) % n  # Generating the key

            # Sending the local generated key in 128 unsigned byte length
            self.connection.send(local_k.to_bytes(128, byteorder='little', signed=False))

            # Finally generate the shared private key
            k = str(pow(remote_k, local_exponent) % n).rjust(8, '0')
            print('Done, private shared key: {}\n=======================\n'.format(k))

            file = os.open("tmp\\" + self.client_address[0], os.O_CREAT | os.O_TRUNC | os.O_RDWR)
            os.write(file, b'\x00'*8)

            memory_file = mmap.mmap(file, 8)
            memory_file.flush()
            memory_file.write(k.encode())

        elif req == 'ci':
            print('Receiving image')

            key_path = '..\\..\\key\\ness_public.pem' #+ input("Enter the sender's public key path")
            key_file = open(key_path, 'rb')
            key = RSA.importKey(key_file.read())
            signer = Signature.new(key)
            hash = SHA.new()

            # Receiving the rest of the messages
            # First the image
            raw_image = recv_msg(self.connection)
            # Then the signature
            signature = recv_msg(self.connection)
            # Finally the padding
            raw_padding = self.connection.recv(1)
            padding = int.from_bytes(raw_padding, 'little')

            # Writing the ciphered image to a file
            file = open('cipher.bmp', 'wb')
            file.write(raw_image)
            file.close()

            image = BMP('cipher.bmp')
            ciphertext = image.pixels

            fd = os.open("tmp\\" + self.client_address[0], os.O_RDONLY, mode=0o555)
            des_key = os.read(fd, 8)
            decipher = DES.new(des_key, DES.MODE_CBC, b'12345678')

            if padding == 0:
                plaintext = decipher.decrypt(bytes(ciphertext))
            else:
                plaintext = decipher.decrypt(bytes(ciphertext))[:-padding]
            image.pixels = plaintext

            hash = SHA.new(plaintext)
            signer = Signature.new(key)

            if signer.verify(hash, signature):
                print('Image signature validated, writing\n====================\n')
                BMP.create_image(image, 'plain.bmp')
            else:
                print('Image signature invalid\n==============================\n')
                BMP.create_image(image, 'plain.bmp')

        self.finish()


if __name__ == '__main__':
    main()