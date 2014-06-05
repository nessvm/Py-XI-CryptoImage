import socket

from Crypto.Random import random

__author__ = 'Ness'


def diffie_hellman(address, flags=0):
    """
    Starts the diffie hellman process with the server located in the specified
    address
    :param address: (IP, port) tuple
    :return: The key string obtained with Diffie-Hellman
    """
    if not isinstance(address[0], str):
        raise TypeError("Invalid address type, 'str' is required,\
        got {}".format(type(address[0])))

    elif not isinstance(address[1], int):
        raise TypeError("Invalid port type, 'int' is required,\
        got {}".format(type(address[1])))

    else:
        sock = socket.socket()

        try:
            if flags & 0x01:
                local_exponent = int(input('Enter your exponent\n'))
            else:
                local_exponent = random.randint(10, 1000)

            sock.connect(address)
            sock.send('dh'.encode())

            gn_pair = sock.recv(128).decode()
            gn_pair = gn_pair.split()
            g = int(gn_pair[0])
            n = int(gn_pair[1])
            local_k = pow(g, local_exponent) % n
            sock.send(local_k.to_bytes(128, byteorder='little', signed=False))
            remote_k = int.from_bytes(sock.recv(128), byteorder='little', signed=False)
            k = pow(remote_k, local_exponent) % n

        except ConnectionRefusedError:
            print('Connection refused, aborting')
        except ConnectionAbortedError:
            print('Connection aborted on server side')
        except ConnectionError:
            print('Unknown connection error')

        finally:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            return str(k).rjust(8, '0')
