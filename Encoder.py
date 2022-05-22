# Credit: https://www.geeksforgeeks.org/image-based-steganography-using-python/

import math

from PIL import Image


# for split frames
from moviepy.editor import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Convert encoding data into 8-bit binary ASCII
def generateData(data):
    newdata = []
    for i in data: # list of binary codes of given data
        newdata.append(format(ord(i), '08b'))
    return newdata
 
# Pixels modified according to encoding data in generateData
def modifyPixel(pixel, data):
    datalist = generateData(data)
    lengthofdata = len(datalist)
    imagedata = iter(pixel)
    for i in range(lengthofdata):
        # Extracts 3 pixels at a time
        pixel = [value for value in imagedata.__next__()[:3] + imagedata.__next__()[:3] + imagedata.__next__()[:3]]
        # Pixel value should be made odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pixel[j]% 2 != 0):
                pixel[j] -= 1
            elif (datalist[i][j] == '1' and pixel[j] % 2 == 0):
                if(pixel[j] != 0):
                    pixel[j] -= 1
                else:
                    pixel[j] += 1
        # Eighth pixel of every set tells whether to stop ot read further. 0 means keep reading; 1 means thec message is over.
        if (i == lengthofdata - 1):
            if (pixel[-1] % 2 == 0):
                if(pixel[-1] != 0):
                    pixel[-1] -= 1
                else:
                    pixel[-1] += 1
        else:
            if (pixel[-1] % 2 != 0):
                pixel[-1] -= 1
        pixel = tuple(pixel)
        yield pixel[0:3]
        yield pixel[3:6]
        yield pixel[6:9]
 
def encoder(newimage, data):
    w = newimage.size[0]
    (x, y) = (0, 0)
 
    for pixel in modifyPixel(newimage.getdata(), data):
 
        # Putting modified pixels in the new image
        newimage.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
 
# Improved Encoding Function
# Instead of performing Steganography on all the frames, the function will now instead perform Steganography on selected range of frames
def encode(start, end, filename, frame_loc):
    total_frame = end - start + 1
    try:
        with open(filename) as fileinput: # Store Data to be Encoded
            filedata = fileinput.read()
    except FileNotFoundError:
        print("\nFile to hide not found! Exiting...")
        quit()
    datapoints = math.ceil(len(filedata) / total_frame) # Data Distribution per Frame
    counter = start
    print("Performing Steganography...")
    for convnum in range(0, len(filedata), datapoints):
        numbering = frame_loc + "\\" + str(counter) + ".png"
        encodetext = filedata[convnum:convnum+datapoints] # Copy Distributed Data into Variable
        try:
            image = Image.open(numbering, 'r') # Parameter has to be r, otherwise ValueError will occur (https://pillow.readthedocs.io/en/stable/reference/Image.html)
        except FileNotFoundError:
            print("\n%d.png not found! Exiting..." % counter)
            quit()
        newimage = image.copy() # New Variable to Store Hiddend Data
        encoder(newimage, encodetext) # Steganography
        new_img_name = numbering # Frame Number
        newimage.save(new_img_name, str(new_img_name.split(".")[1].upper())) # Save as New Frame
        counter += 1
    print("Complete!\n")

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

# Main Encode

from scenedetect import VideoManager
from scenedetect import SceneManager
# For content-aware scene detection:
from scenedetect.detectors import ContentDetector
def find_scenes(video_path, threshold=30.0):
    # Create our video & scene managers, then add the detector.
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(
        ContentDetector(threshold=threshold))

    # Improve processing speed by downscaling before processing.
    video_manager.set_downscale_factor()

    # Start the video manager and perform the scene detection.
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)

    # Each returned scene is a tuple of the (start, end) timecode.
    return scene_manager.get_scene_list()
scenes = find_scenes(file_path)
frame_start = scenes[0][1].get_frames() - 1
frame_end = frame_start + 1
print(f"\n{bcolors.OKGREEN}Found scene change at frame: ", frame_start, " ", frame_end, f"{bcolors.ENDC}")
frame_location = frames_path
filename = input("\nFile to Hide (inc. extension): ")
encode(frame_start, frame_end, filename, frame_location)

# Combine video
import cv2
def combine_audio_video(video_path, og_path):
    """Combines an audio and a video object together"""
    capture = cv2.VideoCapture(og_path) # Stores OG Video into a Capture Window
    fps = capture.get(cv2.CAP_PROP_FPS) # Extracts FPS of OG Video

    video_path_real = video_path + "\\%d.png" # To Get All Frames in Folder

    os.system("ffmpeg-4.3.1-2020-10-01-full_build\\bin\\ffmpeg -framerate %s -i \"%s\" -codec copy output\\combined_video_only.mp4" % (str(int(fps)), video_path_real)) # Combining the Frames into a Video
    

    print("Combining Complete!")

combine_audio_video(frames_path, file_path)