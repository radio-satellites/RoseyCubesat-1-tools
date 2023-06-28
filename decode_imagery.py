# Input: Satnogs DB type files - 2023-05-21 09:26:37|A49EA68AB262E0A49EA68AB2626303F05701A40C000000086D0B0B0B0..... etc.
import argparse
import datetime
import math
import os.path

from dateutil import parser as dateparser
import cv2
from PIL import Image


def chunk2xy(chunk_num):
    x_image = (chunk_num * 80) % 480
    y_image = math.floor((chunk_num * 80) / 480)

    return x_image, y_image


def write_pixel(imager, chunk_num):
    x, y = chunk2xy(chunk_num)
    for i in range(80):
        # print(imager[i])
        try:
            im.putpixel((x + i, y), (imager[i], imager[i], imager[i]))
        except Exception as e:
            print(e)
            # print(len(imager))
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
        # print("GOOD FRAME!")

        isPreview = frame_bytes[5]
        elementID = int.from_bytes(frame_bytes[5:7], "big")
        imagery = frame_bytes[7:]  # imagery data
        # print(f"{isPreview}\t{elementID}\t{imagery}")
        write_pixel(imagery, elementID)
        try:
            ids_frames.remove(elementID)
        except:
            # print(f"Exception at {isPreview}\t{elementID}")
            pass

        # print(packetID)
        # print("WRITE FRAME!",elementID,chunk2xy(elementID))


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--start_date", "-s", action="store")
    argparser.add_argument("--end_date", "-e", action="store")
    argparser.add_argument("--source_file", "-f", required=True, action="store")
    args = argparser.parse_args()

    start_datetime = (
        dateparser.parse(args.start_date) if args.start_date else datetime.datetime.min
    )
    end_datetime = (
        dateparser.parse(args.end_date) if args.end_date else datetime.datetime.max
    )

    print(f"Start date: {start_datetime}\tEnd date: {end_datetime}")

    if not os.path.exists(args.source_file):
        raise ValueError("Source file does not exist.")

    with open(args.source_file, "r") as f:
        f_lines = f.read().split("\n")

    f_frames = []

    ids_frames = list(range(2160))

    for line in f_lines:
        line_parts = line.split("|")
        if len(line_parts) == 2:
            frame_date = dateparser.parse(line_parts[0])
            # print(f"{start_datetime} < {frame_date} < {end_datetime}")
            if start_datetime < frame_date < end_datetime:
                f_frames.append(line_parts[1])

    print(f"Original frame count: {len(f_lines)}")
    print(f"Filtered frame count: {len(f_frames)}")

    # parsing

    im = Image.new("RGB", (480, 360))

    for i in range(len(f_frames)):
        frame = f_frames[i]
        parse(frame)

    im.save("output_raw.png")
    srcBGR = cv2.imread("output_raw.png", 0)
    rgb = cv2.cvtColor(srcBGR, cv2.COLOR_BayerGR2RGB)
    bw = cv2.cvtColor(srcBGR, cv2.COLOR_BayerGR2GRAY)
    cv2.imwrite("output_rgb.png", rgb)
    cv2.imwrite("output_bw.png", bw)

    # post process - fill in blanks

    im_blank = Image.open("output_raw.png")
    pixels = list(im_blank.getdata())
    for z in range(len(ids_frames)):
        bad_id = ids_frames[z]
        x, y = chunk2xy(bad_id)
        for i in range(80):
            try:
                im_blank.putpixel(
                    (x + i, y),
                    (
                        pixels[(y - 1) * 480 + x + i][0],
                        pixels[(y - 1) * 480 + x + i][0],
                        pixels[(y - 1) * 480 + x + i][0],
                    ),
                )
            except:
                print("Can't correct error")

    im_blank.save("output_smooth_raw.png")

    # post process color

    srcBGR = cv2.imread("output_smooth_raw.png", 0)
    rgb = cv2.cvtColor(srcBGR, cv2.COLOR_BayerGR2RGB)
    bw = cv2.cvtColor(srcBGR, cv2.COLOR_BayerGR2GRAY)
    cv2.imwrite("output_smooth_rgb.png", rgb)
    cv2.imwrite("output_smooth_bw.png", bw)
