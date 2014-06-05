__author__ = 'Ness'

from socket import *


def send_msg(connection, msg):
    """
    Function for sending an image through a socket
    :param connection:
    @:type connection: socket
    :param msg:
    :type msg: bytes
    :return:
    """

    # Define the image size for confirmation
    msg_size = len(msg)
    raw_msg_size = msg_size.to_bytes(8, "little")
    # Send the image bytes
    connection.sendall(raw_msg_size + msg)


def recv_msg(connection):
    """

    :param connection:
    :type connection: socket
    :return:
    """

    # Receive message length
    raw_msg_size = recvall(connection, 8)
    # Check for errors
    if not raw_msg_size:
        return None
    msg_size = int.from_bytes(raw_msg_size, "little")

    # Receive message data
    msg = recvall(connection, msg_size)
    return msg


def recvall(connection, n):
    """
    Helper function to recv n bytes or return None if EOF is hit
    :param connection:
    :type connection: socket
    :param n:
    :return:
    """
    data = b''
    while len(data) < n:
        packet = connection.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data