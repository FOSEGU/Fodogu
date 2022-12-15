"""
    Original Code from GitHub, Devon Clark, DROP Project
"""

# Devon Clark
# Message Class
import struct
import datetime
from modulesV3.Packet import PacketV3
from modulesV3.GPSPayload import GPSPayloadV3
import simplekml

class MessageV3:
    # *** add the other field names later
    fieldnames = [ 'messageid', 'offsetTime', 'logDateTime', 'time(millisecond)',
    'latitude', 'longitude', 'satnum', 'gpsHealth', 'altitude', 'baroAlt',
    'velN', 'velE', 'velD', 'vel', 'velH',
    ]
    tickNo = None
    tickOffset = 0
    row_out = {}
    packetNum = 0
    packets = []
    addedData = False
    meta = None
    startUNIXTime = None
    gps_fr_dict = {}
    kmlFile = None
    kmlWriter = None
    kml_res = 1   # kml resolution: kml_res = X, where 1:X represents the ratio of original points to output points for the kml. Used to scale down prevent large datasets from not opening in google earth
    point_cnt = kml_res # for counting the points before writing to kml

    def __init__(self, meta, kmlFile=None, kmlScale=1):
        #self.fieldnames = ['messageid'] + GPSPayload.fields + MotorPayload.fields + HPPayload.fields + RCPayload.fields + TabletLocPayload.fields + BatteryPayload.fields + GimbalPayload.fields + FlightStatPayload.fields + AdvBatteryPayload.fields
        self.tickNo = None
        self.row_out = {}
        self.packetNum = 0
        self.packets = []
        self.addedData = False
        self.meta = meta
        self.gps_fr_dict = {}

        self.kmlFile = kmlFile
        self.kmlWriter = None
        if self.kmlFile != None:
            self.kmlWriter = simplekml.Kml()
            self.kml_res = kmlScale
        # *********************************************
        # **** WARNING: THIS IS NOT THE PREFERED METHOD TO OBTAIN THE START TIME
        # ctime is the time the meta data (permissions) were last changed
        # THIS IS NOT THE CREATION TIME
        # We are assuming here that the last time the permissions were
        # touched was when the file was created. This may not be true.
        # If you do not wish to use this, just comment it out. It won't break anything ;)
        # *********************************************
        self.startUNIXTime = int(meta.st_ctime)
        # *********************************************
        # *********************************************

    def setTickNo(self, tickNo):
        self.tickNo = tickNo

    def addPacket(self, pktlen, header, payload):
        # everything we need to do with the packet obj should be done here because we dont retain them
        packet = Packet(pktlen, header, payload)
        tickNoRead = struct.unpack('I', packet.header[3:7])[0]
        if packet.payload != None and tickNoRead >= 0:
            self.addedData = True
            self.setTickNo(tickNoRead)
            self.row_out = dict(self.row_out, **packet.getItems())
            self.packetNum += 1
            if packet.pkttype == GPSPayload._type:      # GPS Packet
                if self.row_out.get('latitude') and self.row_out.get('longitude'):
                    if self.row_out['latitude'] != '' and self.row_out['longitude'] != '':
                        self.gps_fr_dict[self.row_out['time']] = [self.row_out['latitude'], self.row_out['longitude']]
            return True
        return False

    def getRow(self):
        if self.tickNo != None:
            offsetTime = float(self.tickNo - self.tickOffset)/600.0
        else:
            offsetTime = ''
        #logDateTime = datetime.datetime.fromtimestamp(self.startUNIXTime + int(offsetTime)).strftime('%Y-%m-%d %H:%M:%S')
        logDateTime = ''
        return dict(self.row_out, **{'messageid':self.tickNo, 'offsetTime':offsetTime, 'logDateTime':logDateTime})

    def writeKml(self, row):
        if self.kmlWriter != None:
            if row.get('latitude', False) and row.get('longitude', False):
                if self.point_cnt % self.kml_res == 0:
                    self.kmlWriter.newpoint(name=str(row.get('messageid')), coords=[(row.get('longitude'), row.get('latitude'))])
                self.point_cnt += 1

    def writeRow(self, writer, newTickNo):
        if newTickNo != self.tickNo:
            if self.addedData:
                writer.writerow(self.getRow())   # write the current message before starting a new one (only if we have new data)
                self.addedData = False           # reset addedData because just wrote all the most recent info to the csv
            self.writeKml(self.getRow())  # write to KML file.
            self.tickNo = newTickNo

    def outToFile(self, fname):
        if self.gps_fr_dict != {}:
            with open(fname + '-output.txt', 'w') as of:
                for d in self.gps_fr_dict:
                    of.write(str(d) + ': ' + str(self.gps_fr_dict[d]) + '\n')

    def finalizeKml(self):
        if self.kmlWriter != None and self.kmlFile != None:
            self.kmlWriter.save(self.kmlFile)
