import csv
from modules.Message import Message
from modules.ProcessFRCSV import ProcessFRCSV
import struct

def openFile(path):
    file = open(path, 'rb')

    return file


# check the type of .DAT file
def checkType(file):
    # file = input .DAT file
    # test_file = openFile("TestData/inspireFLY018.DAT")
    f_header = file.read(256)
    print(f_header)

    # Type P1
    if f_header[16:21].decode('ascii') == b"BUILD".decode('ascii'):
        print("Type P1. It's available.")
        decodeP1(file)
    elif f_header[242, 252].decode('ascii') == b"DJI_LOG_V3".decode('ascii'):
        print("Type P2. It's available.")
    elif f_header[0:4].decode('ascii') == b"LOGH".decode('ascii'):
        print("Type E1.")
    else:
        raise NotDATFileError(file)


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
