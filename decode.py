import csv
import os
from modules.Message import Message
from modules.ProcessFRCSV import ProcessFRCSV
import struct
import hashlib


# check the meta data and hash value of .DAT file
def checkMeta(path):
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


# check the type of .DAT file
def checkType(path):
    # test_file = open("TestData/inspireFLY018.DAT", 'rb')

    with open(path, 'rb') as f:
        f_header = f.read(256)
        print(f_header)

        if f_header[16:21].decode('ascii') == b"BUILD".decode('ascii'):
            print("Type P1. It's available.")
            decodeP1(f)
        elif f_header[242:252].decode('ascii') == b"DJI_LOG_V3".decode('ascii'):
            print("Type P2. It's available.")
        elif f_header[0:4].decode('ascii') == b"LOGH".decode('ascii'):
            print("Type E1.")
        else:
            raise NotDATFileError(f)


def decodeP1(fn):
    return 0

def decodeP2(fn):
    return 0


def writeOutput(path, message):
    output_file = open(path, 'w')
    writer = csv.DictWriter(output_file, lineterminator='\n', fieldnames=Message.fieldnames)
    writer.writeheader()

    writer.writerow(message.getRow())


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
        self.value = 'Expected start of packet (0x55) but found ' + str(bytestr) + ' instead. Located at byte ' + str(offset) + ' of input file.'
    def __str__(self):
        return repr(self.value)
