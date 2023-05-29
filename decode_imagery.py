#Input: Satnogs DB type files - 2023-05-21 09:26:37|A49EA68AB262E0A49EA68AB2626303F05701A40C000000086D0B0B0B0..... etc.

from PIL import Image
import io
import array
import math
import cv2

f = open("original.txt",'r')

f_lines = f.read().split("\n")

f.close()

f_frames = []


for i in range(len(f_lines)):
    line = f_lines[i]
    f_frames.append(line[20:])


#parsing

im = Image.new("RGB",(480,360))

def chunk2xy(chunk_num):
    x_image = (chunk_num*80) % 480
    y_image = math.floor((chunk_num*80)/480)
    
    
    return x_image,y_image

def write_pixel(imager,chunk_num):
    
    for i in range(80):
        #print(imager[i])
        try:
            x,y = chunk2xy(chunk_num)
            im.putpixel((x+i,y),(imager[i],imager[i],imager[i]))
        except Exception as e:
            print(e)
            #print(len(imager))
            pass


def parse(frame):
    """
struct{
uint16_t packetId; //0xA4 0x0C
uint16_t sequenceId; //ignore
uint8_t isPreview; //one indicates 48x36 pixel preview, zero indicates 480x360 full resolution image
uint16_t elementId; //image chunk number. 0-21 for previews, 0-2159 for full
uint8_t pixels[80]; //pixel data
}

"""
    
    frame_bytes = bytearray.fromhex(frame)[18:]
    packetID = int.from_bytes(frame_bytes[0:2], "big")
    
    if len(frame_bytes) > 30 and packetID == 41996:
        #print("GOOD FRAME!")
        
        isPreview = frame_bytes[5]
        elementID = int.from_bytes(frame_bytes[5:7], "big")
        imagery = frame_bytes[7:] #imagery data
        write_pixel(imagery,elementID)
        #print(packetID)
        #print("WRITE FRAME!",elementID,chunk2xy(elementID))
        
        
    


for i in range(len(f_frames)):
    frame = f_frames[i]
    parse(frame)

im.save("output.png")
srcBGR = cv2.imread("output.png")
rgb= cv2.cvtColor(srcBGR, cv2.COLOR_BayerGR2RGB)
cv2.imwrite('output_rgb.png', rgb)

