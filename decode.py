# python3
# Subin Jo
# 2022. 11. 02

import csv
import os
from modules.Message import Message
import struct
import hashlib
from Cryptodome.Cipher import AES

# check the meta data and hash value of .DAT file
def checkMeta(path):
    print("path", path)
    meta = os.stat(path)

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha512 = hashlib.sha512()

    with open(path, 'rb') as f:
        buf = f.read()
        md5.update(buf)
        sha1.update(buf)
        sha512.update(buf)

    return meta, md5.hexdigest(), sha1.hexdigest(), sha512.hexdigest()

def decrypt_aes_e2(data):
    key = bytes.fromhex('756e617661696c61626c650000000000')
    iv = b"0123456789abcdef"
    Cipher = AES.new(key, AES.MODE_CBC, iv)
    plain = Cipher.decrypt(data)
    return plain

def check16BytesforE2(f_size, header16):
    print("File Size: ", f_size)
    if f_size == 0:
        print("Empty File")
        return False
    elif f_size % 16 != 0:
        print("Try extractDJI.py first")
        return False
    else:
        plainheader16 = decrypt_aes_e2(header16)
        first = plainheader16.decode('utf-8').rstrip('\x00')
        if first.isdigit():
            return True
        else:
            return False

# check the type of .DAT file
def checkType(in_path, out_path):

    meta, md5, sha1, sha512 = checkMeta(in_path)
    print("Before: ", meta, md5, sha1, sha512)

    with open(in_path, 'rb') as f:
        f_header = f.read(256)
        #print(f_header[0:4])

        if f_header[0:4] == b"LOGH":
            # E1
            print("Type E1.")
            return 0
        elif f_header[242:252] == b"DJI_LOG_V3":
            # P2, E3
            print("Type P2 or E3. It's available.")
            return 0
            #decodeP2(meta, f, out_path)
        elif f_header[16:21] == b"BUILD":
            # Signature of P1. but all types have it except P3, P4
            print("Type P1. It's available.")
            f.seek(0)
            decodeP1(meta, f, out_path)
        elif check16BytesforE2(meta.st_size, f_header[:16]):
            f.seek(0)
            decryptE2(meta, f, out_path)
            checkType(out_path+"output_e2.DAT", out_path)
        else:
            print("nothing")
            #raise NotDATFileError(f)


def decryptE2(meta, in_file, out_path):
    out_path = out_path + "output_e2.DAT"
    print("decryptE2 Start")
    enc_buf = in_file.read()
    dec_buf = decrypt_aes_e2(enc_buf)

    out_f = open(out_path, "wb")
    out_f.write(dec_buf[16:])
    out_f.close()
    print("decryptE2 Complete")


def decodeP1(meta, in_file, out_path):

    out_path = out_path + "\output.csv"
    out_file = open(out_path, 'w')
    writer = csv.DictWriter(out_file, lineterminator='\n', fieldnames=Message.fieldnames)
    writer.writeheader()

    p_subtypes = []
    alternateStructure = False

    try:
        header = in_file.read(128)  # set the right start of payload

        byte = in_file.read(1)  # read the first byte of the payload
        if byte[0] != 0x55:
            alternateStructure = True
        message = None
        message = Message(meta)  # create a new, empty message

        corruptPackets = 0  # keeps track of the number of corrupt packets - data blocks that do not meet the minimum formatting requirements to be a DJI flight data packet
        unknownPackets = 0  # keeps track of the number of unrecognized packets - packets that are of the DJI flight data format but we do not know how to parse the payload

        start_issue = True
        while len(byte) != 0:

            try:
                if byte[0] != 0x55:
                    raise NoNewPacketError(byte, in_file.tell())

                start_issue = True  # reset start issue here
                pktlen = 0xFF & int(in_file.read(1)[0])  # length of the packet
                padding = in_file.read(1)  # padding
                if padding[0] == 0:
                    header = in_file.read(7)
                    current = in_file.tell()
                    in_file.seek(
                        current + pktlen - 10)  # seek to the byte that should be the starting byte of the next packet
                    # print('read from: ' + str(current + pktlen - 10))
                    next_start = in_file.read(1)
                    if len(next_start) <= 0:
                        break
                    if next_start[0] != 0x55:  # something is wrong with the packet length
                        # print('error at byte: ' + str(current + pktlen - 10 + 1))
                        in_file.seek(current)  # reset file pointer to just after header
                        byte = in_file.read(1)
                        raise CorruptPacketError("Packet length error at byte " + str(current - 9))
                    in_file.seek(current)  # go back to where we were if packet length is ok

                    payload = in_file.read(pktlen - 10)
                    thisPacketTickNo = struct.unpack('I', header[3:7])[0]
                    if thisPacketTickNo < 0:
                        # Legacy code from DatCon: (thisPacketTickNo < 0) or
                        # ((alternateStructure) and (thisPacketTickNo > 4500000)) or
                        # ((not alternateStructure) and (thisPacketTickNo > 1500000))
                        byte = padding
                        raise CorruptPacketError(
                            "Corrupted tick number. Tick No: " + str(
                                thisPacketTickNo) + ", alternate structure? " + str(
                                alternateStructure))
                    if pktlen == 0:
                        byte = padding
                        raise CorruptPacketError()
                    if message.tickNo == None:
                        message.setTickNo(thisPacketTickNo)
                    message.writeRow(writer, thisPacketTickNo)

                    if message.addPacket(pktlen, header, payload) == False:
                        unknownPackets += 1

                    byte = in_file.read(1)
                else:
                    byte = padding
            except CorruptPacketError as e:
                corruptPackets += 1
                print(e.value)
            except NoNewPacketError as e:
                if start_issue:  # first time around the loop with this problem
                    print(e.value)
                    start_issue = False  # set to false so we don't flood the screen with error statements
                byte = in_file.read(1)
            except Exception as e:
                print(e)

        writer.writerow(message.getRow())  # write the last row

    finally:
        in_file.close()
        out_file.close()



# custom exception
class NotDATFileError(Exception):
    ''' Raised when a file other than a DJI .DAT file is being processed '''

    def __init__(self, in_f):
        self.value = "Attempted to open non-DAT file: " + in_f

    def __str__(self):
        return repr(self.value)


class CorruptPacketError(Exception):
    def __init__(self, value="The Packet is corrupt."):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NoNewPacketError(Exception):
    def __init__(self, bytestr, offset):
        self.value = 'Expected start of packet (0x55) but found ' + str(bytestr) + ' instead. Located at byte ' + str(
            offset) + ' of input file.'

    def __str__(self):
        return repr(self.value)
