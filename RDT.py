from datetime import datetime, timedelta
import Network
import argparse
from time import sleep
import hashlib


class RDTException(Exception):
    pass


class Packet:
    # the number of bytes used to store packet length
    seq_num_S_length = 10
    length_S_length = 10
    # length of md5 checksum in hex
    checksum_length = 32

    def __init__(self, seq_num, msg_S):
        self.seq_num = seq_num
        self.msg_S = msg_S

    @classmethod
    def from_byte_S(cls, byte_S):
        if Packet.corrupt(byte_S):
            raise RuntimeError('Cannot initialize Packet: byte_S is corrupt')
        # extract the fields
        seq_num = int(byte_S[Packet.length_S_length: Packet.length_S_length + Packet.seq_num_S_length])
        msg_S = byte_S[Packet.length_S_length + Packet.seq_num_S_length + Packet.checksum_length:]
        return cls(seq_num, msg_S)

    def get_byte_S(self):
        # convert sequence number of a byte field of seq_num_S_length bytes
        seq_num_S = str(self.seq_num).zfill(self.seq_num_S_length)
        # convert length to a byte field of length_S_length bytes
        length_S = str(self.length_S_length + len(seq_num_S) + self.checksum_length + len(self.msg_S)).zfill(
            self.length_S_length)
        # compute the checksum
        checksum = hashlib.md5((length_S + seq_num_S + self.msg_S).encode('utf-8'))
        checksum_S = checksum.hexdigest()
        # compile into a string
        return length_S + seq_num_S + checksum_S + self.msg_S

    @staticmethod
    def corrupt(byte_S):
        # extract the fields
        length_S = byte_S[0:Packet.length_S_length]
        seq_num_S = byte_S[Packet.length_S_length: Packet.length_S_length + Packet.seq_num_S_length]
        checksum_S = byte_S[
                     Packet.length_S_length + Packet.seq_num_S_length: Packet.length_S_length + Packet.seq_num_S_length + Packet.checksum_length]
        msg_S = byte_S[Packet.length_S_length + Packet.seq_num_S_length + Packet.checksum_length:]

        # compute the checksum locally
        checksum = hashlib.md5(str(length_S + seq_num_S + msg_S).encode('utf-8'))
        computed_checksum_S = checksum.hexdigest()
        # and check if the same
        return checksum_S != computed_checksum_S


class RDT:
    # receive timeout
    timeout = timedelta(seconds=1)
    # latest sequence number used in a packet
    seq_num = 1
    # buffer of bytes read from network
    byte_buffer = ''

    def __init__(self, role_S, server_S, port):
        # use the passed in port and port+1 to set up unidirectional links between
        # RDT send and receive functions
        # cross the ports on the client and server to match net_snd to net_rcv
        if role_S == 'server':
            self.net_snd = Network.NetworkLayer(role_S, server_S, port)
            self.net_rcv = Network.NetworkLayer(role_S, server_S, port + 1)
        else:
            self.net_rcv = Network.NetworkLayer(role_S, server_S, port)
            self.net_snd = Network.NetworkLayer(role_S, server_S, port + 1)

    def disconnect(self):
        self.net_snd.disconnect()
        del self.net_snd
        self.net_rcv.disconnect()
        del self.net_rcv

    def rdt_1_0_send(self, msg_S):
        p = Packet(self.seq_num, msg_S)
        self.seq_num += 1
        # !!! make sure to use net_snd link to udt_send and udt_receive in the RDT send function
        self.net_snd.udt_send(p.get_byte_S())

    def rdt_1_0_receive(self):
        start = datetime.now()
        while True:
            if datetime.now() - start > self.timeout:
                raise RDTException("timeout")
            # !!! make sure to use net_rcv link to udt_send and udt_receive the in RDT receive function
            byte_S = self.net_rcv.udt_receive()
            self.byte_buffer += byte_S
            # check if we have received enough bytes
            if len(self.byte_buffer) < Packet.length_S_length:
                # return ret_S  # not enough bytes to read packet length
                continue
            # extract length of packet
            length = int(self.byte_buffer[:Packet.length_S_length])
            if len(self.byte_buffer) < length:
                # return ret_S  # not enough bytes to read the whole packet
                continue
            # create packet from buffer content
            p = Packet.from_byte_S(self.byte_buffer[0:length])
            # remove the packet bytes from the buffer
            self.byte_buffer = self.byte_buffer[length:]
            # return packet message to the upper layer
            return p.msg_S

    # Implement These:
    # think about async

    # rdt 1.0 + corruption and duplicate
    def rdt_2_1_send(self, msg_S):
        sndpkt = Packet(self.seq_num, msg_S)
        self.seq_num += 1

        while True:
            self.net_snd.udt_send(sndpkt.get_byte_S())  # sending packet
            # new state: Wait for ACK or NAK 0
            self.byte_buffer = ''
            rcvpkt = ''
            # waiting for response from receiver, no timeout
            while rcvpkt == '':
                rcvpkt = self.net_rcv.udt_receive()  # response equals whatever the receiver responds

            length = int(rcvpkt[:Packet.length_S_length])  # length of packet
            self.byte_buffer = rcvpkt  # setting buffer

            if Packet.corrupt(self.byte_buffer[:length]):  # checking for corruption
                # ACK/NAK packet corrupted, need to resend packet
                continue
            # packet is not corrupt
            else:
                response = Packet.from_byte_S(self.byte_buffer[:length])
                if response.seq_num < self.seq_num:
                    # receiver behind sender
                    # ACK
                    ack = Packet(response.seq_num, '1')
                    self.net_snd.udt_send(ack.get_byte_S())
                if response.msg_S == '1':  # ACK
                    # successfully sent a packet
                    self.seq_num += 1
                    break
                elif response.msg_S == '0':  # NAK
                    # NAK received, need to resend packet
                    continue

    def rdt_2_1_receive(self):
        ret_S = None
        byte_S = self.net_rcv.udt_receive()
        self.byte_buffer += byte_S
        loop_guard = self.seq_num
        # keep extracting packets - if reordered, could get more than one
        while loop_guard == self.seq_num:
            # check if we have received enough bytes
            if len(self.byte_buffer) < Packet.length_S_length:
                break  # not enough bytes to read packet length

            # extract length of packet
            length = int(self.byte_buffer[:Packet.length_S_length])
            if len(self.byte_buffer) < length:
                break  # not enough bytes to read the whole packet

            if Packet.corrupt(self.byte_buffer):
                # packet corrupted send NAK
                nak = Packet(self.seq_num, '0')  # send NAK
                self.net_snd.udt_send(nak.get_byte_S())
            else:  # packet not corrupted
                # create packet from buffer content and add to return string
                rcvpkt = Packet.from_byte_S(self.byte_buffer[:length])
                if rcvpkt.msg_S != '1' and rcvpkt.msg_S != '0':  # if this packet is not an ACK or NAK
                    if rcvpkt.seq_num < self.seq_num:
                        # Duplicate, ACK
                        ack = Packet(rcvpkt.seq_num, '1')
                        self.net_snd.udt_send(ack.get_byte_S())
                    elif rcvpkt.seq_num == self.seq_num:
                        # ACK
                        ack = Packet(self.seq_num, '1')
                        self.net_snd.udt_send(ack.get_byte_S())
                        self.seq_num += 1

                    ret_S = rcvpkt.msg_S if (ret_S is None) else ret_S + rcvpkt.msg_S  # build message
                # remove the packet bytes from the buffer
            self.byte_buffer = self.byte_buffer[length:]
        # if this was the last packet, will return on the next iteration
        return ret_S

    def rdt_3_0_send(self, msg_S):
        # rdt 2.1 + loss
        wait = timedelta(5)
        sndpkt = Packet(self.seq_num, msg_S)
        self.seq_num += 1

        while True:
            self.net_snd.udt_send(sndpkt.get_byte_S())  # sending packet
            self.byte_buffer = ''
            rcvpkt = ''
            # swapped out time.time() w/ datetime.now()
            timeoutstart = datetime.now()
            timeoutend = datetime.now()
            while rcvpkt == '' and timeoutend - timeoutstart < wait:  # waiting for response from receiver, timeout = 5
                rcvpkt = self.net_rcv.udt_receive()  # response equals whatever the receiver responds
                timeoutend = datetime.now()
            if rcvpkt == '':
                continue  # timeout, resend packet

            length = int(rcvpkt[:Packet.length_S_length])  # length of packet
            self.byte_buffer = rcvpkt  # setting buffer

            if Packet.corrupt(self.byte_buffer[:length]):  # checking for corruption
                # ACK/NAK packet corrupted, need to resend packet
                continue
            else:  # packet is not corrupt
                response = Packet.from_byte_S(self.byte_buffer[:length])
                if response.seq_num < self.seq_num:
                    # receiver behind sender
                    # ACK
                    ack = Packet(response.seq_num, '1')
                    self.net_snd.udt_send(ack.get_byte_S())
                if response.msg_S == '1':  # ACK
                    # successfully sent a packet
                    self.seq_num += 1
                    break
                elif response.msg_S == '0':  # NAK
                    # NAK received, need to resend packet
                    continue

    def rdt_3_0_receive(self):
        # rdt 2.1 + loss
        ret_S = None
        byte_S = self.net_rcv.udt_receive()
        self.byte_buffer += byte_S
        loop_guard = self.seq_num
        # keep extracting packets - if reordered, could get more than one
        while loop_guard == self.seq_num:
            # check if we have received enough bytes
            if len(self.byte_buffer) < Packet.length_S_length:
                break  # not enough bytes to read packet length

            # extract length of packet
            length = int(self.byte_buffer[:Packet.length_S_length])
            if len(self.byte_buffer) < length:
                break  # not enough bytes to read the whole packet

            if Packet.corrupt(self.byte_buffer):
                # packet corrupted send NAK
                nak = Packet(self.seq_num, '0')  # send NAK
                self.net_snd.udt_send(nak.get_byte_S())
            else:  # packet not corrupted
                # create packet from buffer content and add to return string
                rcvpkt = Packet.from_byte_S(self.byte_buffer[:length])
                if rcvpkt.msg_S != '1' and rcvpkt.msg_S != '0':  # if this packet is not an ACK or NAK
                    if rcvpkt.seq_num < self.seq_num:
                        # Duplicate, ACK
                        ack = Packet(rcvpkt.seq_num, '1')
                        self.net_snd.udt_send(ack.get_byte_S())
                    elif rcvpkt.seq_num == self.seq_num:
                        # ACK
                        ack = Packet(self.seq_num, '1')
                        self.net_snd.udt_send(ack.get_byte_S())
                        self.seq_num += 1

                    ret_S = rcvpkt.msg_S if (ret_S is None) else ret_S + rcvpkt.msg_S  # build message
                # remove the packet bytes from the buffer
            self.byte_buffer = self.byte_buffer[length:]
        # if this was the last packet, will return on the next iteration
        return ret_S


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RDT implementation.')
    parser.add_argument('role', help='Role is either client or server.', choices=['client', 'server'])
    parser.add_argument('server', help='Server.')
    parser.add_argument('port', help='Port.', type=int)
    args = parser.parse_args()

    rdt = RDT(args.role, args.server, args.port)
    if args.role == 'client':
        rdt.rdt_1_0_send('MSG_FROM_CLIENT')
        sleep(2)
        print(rdt.rdt_1_0_receive())
        rdt.disconnect()
    else:
        sleep(1)
        print(rdt.rdt_1_0_receive())
        rdt.rdt_1_0_send('MSG_FROM_SERVER')
        rdt.disconnect()
