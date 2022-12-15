# Devon Clark
# Packet Class
import struct
from modulesV3.GPSPayload import GPSPayloadV3


class PacketV3:
    pktlen = 0
    header = 0
    pkttype = None
    label = None
    tickNo = 0
    payload = None

    def __init__(self, pktlen, header, payload):
        self.pktlen = pktlen
        self.header = header
        self.pkttype = struct.unpack("<H",self.header[1:3])[0]
        self.tickNo = struct.unpack('<I', self.header[3:7])[0]

        self.payload = self.processPayload(payload)

    def processPayload(self, payload):
        if self.pkttype == GPSPayload._type:      # GPS Packet
            self.label = 'GPS'
            #print(str(self.tickNo) + ' - GPS pkt len: ' + str(self.pktlen))
            payload = self.decode(payload)
            pld_obj = GPSPayload(payload)
            if len(pld_obj.data) > 0:
                return pld_obj
        return None

    def getItems(self):
        try:
            return self.payload.data
        except:
            return {}


    def decode(self, payload):
        xorKey = int(self.tickNo % 256)
        decodedPld = []
        for byte in payload:
            decodedPld.append(byte ^ xorKey)    # byte and xorKey must be ints
        return bytes(decodedPld)
