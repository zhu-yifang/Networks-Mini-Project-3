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

    # rdt 2.0
    logger = miniproject3.logging.get_logger("mp3-sender")
    chunk_size = miniproject3.MAX_PACKET - 5
    pause = .1
    offsets = range(0, len(data), miniproject3.MAX_PACKET)
    for chunk in [data[i:i + chunk_size] for i in offsets]:
        while True:
            # wait for call from above
            sock.send(b'00000' + chunk)
            logger.info("Pausing for %f seconds", round(pause, 2))
            time.sleep(pause)
            # Wait for NAC or ACK
            ACK = sock.recv(1000).decode("utf-8")
            # if (rdt_rcv(rcvpkt) && isACK(rcvpkt))
            print(ACK)
            if ACK == '00000':
                # send the next chunk
                break
            # elif (rdt_rcv(rcvpkt) && isNAK(rcvpkt))
            else:
                # resend
                pass
        



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
    # rdt 2.0
    num_bytes = 0
    # Wait for call from below
    while True:
        data = sock.recv(miniproject3.MAX_PACKET)
        if not data:
            break
        logger.info("Received %d bytes", len(data))
        dest.write(data)
        num_bytes += len(data)
        # send ACK
        sock.send(b'00000')
        dest.flush()
    return num_bytes
