"""
Where solution code to MP3 should be written.  No other files should
be modified.
"""

import socket
import io
import time
import typing
import struct
import miniproject3
import miniproject3.logging


def send(sock: socket.socket, data: bytes):
    """
    Implementation of the sending logic for sending data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.
        data -- A bytes object, containing the data to send over the network.
    """

    # Naive implementation where we chunk the data to be sent into
    # packets as large as the network will allow, and then send them
    # over the network, pausing half a second between sends to let the
    # network "rest" :)
    logger = miniproject3.logging.get_logger("mp3-sender")
    chunk_size = miniproject3.MAX_PACKET - 5
    pause = .1
    offsets = range(0, len(data), miniproject3.MAX_PACKET)
    for chunk in [data[i:i + chunk_size] for i in offsets]:
        sock.send(b'00000' + chunk)
        logger.info("Pausing for %f seconds", round(pause, 2))
        time.sleep(pause)


def recv(sock: socket.socket, dest: io.BufferedIOBase) -> int:
    """
    Implementation of the receiving logic for receiving data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.

    Return:
        The number of bytes written to the destination.
    """
    logger = miniproject3.logging.get_logger("mp3-receiver")
    # Naive solution, where we continually read data off the socket
    # until we don't receive any more data, and then return.
    # You can do better than this!
    num_bytes = 0
    while True:
        data = sock.recv(miniproject3.MAX_PACKET)
        if not data:
            break
        logger.info("Received %d bytes", len(data))
        dest.write(data)
        num_bytes += len(data)
        dest.flush()
    return num_bytes
