# Credit: https://www.geeksforgeeks.org/image-based-steganography-using-python/
import re
import os

from PIL import Image

# for split frames
from moviepy.editor import *

# Global Variable
global frame_location

# Decode the data in the image
def decode(number):
    data = ''
    numbering = str(number)
    decoder_numbering = frame_location + "\\" + numbering + ".png"
    image = Image.open(decoder_numbering, 'r')
    imagedata = iter(image.getdata())
    while (True):
        pixels = [value for value in imagedata.__next__()[:3] + imagedata.__next__()[:3] + imagedata.__next__()[:3]]
        # string of binary data
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        if re.match("[ -~]", chr(int(binstr,2))) is not None: # only decode printable data
            data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

# Function of split frames 
def get_frames(video_object, base_filename):
    """Returns all frames in the video object"""
    print("Spliting frames from video...")
    directory = "output\\" + base_filename + '_frames\\'
    if not os.path.isdir(directory):
        os.makedirs(directory)
    for index, frame in enumerate(video_object.iter_frames()):
        img = Image.fromarray(frame, 'RGB')
        img.save(f'{directory}{index}.png')

    print("Done!\n")
    return directory

# Runtime
# Split frames
file_path = str(input("\nVideo path: "))
video_object = VideoFileClip(file_path)
file_name = os.path.splitext(os.path.basename(file_path))[0]
frames_path = get_frames(video_object, file_name)

print("Please Enter Start and End Frame where Data is Hidden At")
frame_start = int(input("Start Frame: "))
frame_end = int(input("End Frame: "))
frame_location = frames_path
print("Extracting Data...")
decodedtextfile = open('output\decoded_frame.txt', 'a')
decodedtextfile.write('Decoded Text:\n')
for convnum in range(frame_start, frame_end + 1):
    try:
        decodedtextfile.write(decode(convnum))
        print("Data found in Frame %d" % convnum)
    except StopIteration:
        print("No data found in Frame %d" % convnum)
decodedtextfile.close()
print("\nExtraction Complete!")
