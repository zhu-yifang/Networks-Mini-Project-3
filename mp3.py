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

    # rdt 2.1
    logger = miniproject3.logging.get_logger("mp3-sender")
    chunk_size = miniproject3.MAX_PACKET - 5
    pause = 0.1
    offsets = range(0, len(data), miniproject3.MAX_PACKET)
    for chunk in [data[i:i + chunk_size] for i in offsets]:
        sequence = '00000'
        if sequence == '00000':
            while True:
                # wait for call 0 from above
                # rdt_send(data)
                sock.send(sequence.encode() + chunk)
                logger.info("Pausing for %f seconds", round(pause, 2))
                time.sleep(pause)
                # Wait for NAC or ACK 0
                ACK = sock.recv(1000).decode("utf-8")
                # if (rdt_rcv(rcvpkt) && isACK(rcvpkt))
                if ACK == '00000':
                    # send the next chunk
                    sequence = '00001'
                    break
                # elif (rdt_rcv(rcvpkt) && isNAK(rcvpkt))
                else:
                    # resend()
                    pass
        # sequence == 00001
        else:
            while True:
                # wait for call 1 from above
                # rdt_send(data)
                sock.send(sequence.encode() + chunk)
                logger.info("Pausing for %f seconds", round(pause, 2))
                time.sleep(pause)
                # Wait for NAC or ACK 1
                ACK = sock.recv(1000).decode("utf-8")
                # if (rdt_rcv(rcvpkt) && isACK(rcvpkt))
                if ACK == '00001':
                    # send the next chunk
                    sequence = '00000'
                    break
                # elif (rdt_rcv(rcvpkt) && isNAK(rcvpkt))
                else:
                    # resend()
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
    # rdt 2.1
    num_bytes = 0
    # set state to 0
    state = '00000'
    while True:
        data = sock.recv(miniproject3.MAX_PACKET)
        if not data:
            break
        # get the sequnce number
        sequence = data[0:5]
        # wait for 0 from below
        if state == '00000':
            while True:
                # has_seq0()
                if sequence == state:
                    # ACK && change state && deliver
                    sock.send(state.encode())  # ACK
                    state = '00001'   # change state to 1
                    break   # deliver
                # has_seq1()
                else:
                    # ACK
                    sock.send(state.encode())
        # wait for 1 from below
        # if state == '00001':
        else:
            while True:
                # has_seq1()
                if sequence == state:
                    # ACK && change state && deliver
                    sock.send(state.encode())  # ACK
                    state = '00000'   # change state to 0
                    break   # deliver
                # has_seq0()
                else:
                    # ACK
                    sock.send(state.encode())
        # deliver            
        logger.info("Received %d bytes", len(data))
        dest.write(data[5:])
        num_bytes += len(data)
        dest.flush()
    return num_bytes
