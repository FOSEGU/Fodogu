# python3
# writer : Mingyu Seong
# 2022 12 05
import zlib, struct, os

###################################
INPUT_FILENAME = "mini2_dji.DAT"
OUTPUT_PATH = "./output/"
###################################

def isDJIDat(buf):
    if(buf[0] == 0x78 and buf[1] == 0x9c):
        return True
    else:
        return False

def getStrings(buf, offset):
    bStringData = ""
    while True:
        if buf[offset] == 0:
            break
        else:
            bStringData += chr(buf[offset])
            offset += 1
    return bStringData

def mkdirFromFilename(outputBase, filename):
    a = filename.split("/")
    a.pop()
    fileDirPath = "/".join(a)
    os.makedirs(outputBase+fileDirPath, exist_ok=True)

def extractDJI_main(INPUT_FILENAME, OUTPUT_PATH, strResult):
    with open(INPUT_FILENAME, "rb") as f:
        data = f.read()

    if(isDJIDat(data)):
        dedata = zlib.decompress(data)
        #f = open('test.dat', "wb")
        #f.write(dedata)
        #f.close
        remain = len(dedata)
        while(remain > 0):
            try:
                uncompressedFileLength = struct.unpack("<I",dedata[1:5])[0]
                #print(uncompressedFileLength)
                filename = getStrings(dedata, 7)
                print(filename)
                mkdirFromFilename(OUTPUT_PATH, filename)
                payload = dedata[283:uncompressedFileLength+283]

                f = open(OUTPUT_PATH+filename, "wb")
                f.write(payload)
                f.close

                dedata = dedata[uncompressedFileLength+283:]
                remain = len(dedata)
                #print(len(remain))
            except Exception as e:
                print(e)
                raise
        strResult += "Done.\n"
        print("Done.")

    else:
        strResult += "This is not DJI DAT.\n"
        print("This is not DJI DAT.")
        exit()

    return strResult

if __name__ == '__main__':
    extractDJI_main(INPUT_FILENAME, OUTPUT_PATH)
