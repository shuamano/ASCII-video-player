from PIL import Image
import statistics
import cv2
import time
import sys
import os

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "loglevel;fatal"

#replace with whatever video path you want
video_path = "image_to_text/[ANBU-AonE]_Naruto_01_[ED304340].avi"
cap = cv2.VideoCapture(video_path)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
avg_frame_time = []

#clear the initial output in the terminal
print(chr(27) + "[2J")

for frame_number in range(1, length):
    start = time.time()

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number-1)
    res, frame = cap.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)
    image = pil_image
    ascii_grayscale = list(' .,:;irsXA253hMHGS#9B&@')

    text_image = ""
    previous_line = []
    current_line = []
    ascii_line = []
    flip_flop = 1

    #scaling function
    def scale(width, height):
        scale_factor = max(width, height) / 130  # set the horizontal resolution here (original aspect ratio is maintained)
        new_width = round(width / scale_factor)
        new_height = round(height / scale_factor)
        return new_width, new_height

    resize = scale(image.size[0], image.size[1])
    new_image = image.resize(resize)

    px = new_image.load()
    
    for y in range(1, resize[1]): # iterate through the rows
        previous_line = current_line
        current_line = []
        ascii_line = []
        for x in range(1, resize[0]): # determines ascii char for every pixel in row (iterates through colummns)
            pixel = px[x, y]

            #convert the rgb value of the pixel to a grayscale, then normalize to a range of 70 for the ascii chars
            grayscale = ((0.2989 * pixel[0] + 0.5870 * pixel[1] + 0.1140 * pixel[2])/255)*23
            current_line.append(int(grayscale))

            #print(f"Grayscale: {grayscale}, RGB: {pixel}, ASCII: {ascii_grayscale[int(grayscale)]}")
        
        #on the second row and onward, compare the current and previous row and turn them into one averaged row
        if flip_flop == 1:    
            if y > 1:
                for i in range(1, resize[0]-1):
                    ascii_line.append(statistics.mean([current_line[i], previous_line[i]]))

            for i in ascii_line:
                text_image = text_image + ascii_grayscale[int(i)]
            text_image = text_image + "\n"
            flip_flop = 0
        else:
            flip_flop = 1
            
    lines_count = text_image.count('\n') + 1
    end = time.time()
    avg_frame_time.append((end-start)*1000)

    #move cursor to start pos and print the next frame (steady ouput)
    sys.stdout.write("\033[F" * len(text_image.split("\n")))
    for line in text_image.split("\n"):  
        print(line)
    sys.stdout.write(f"Resolution:{resize}, Frame {frame_number}/{length}, Frametime: {(end-start)*1000}ms, Avg FT: {statistics.mean(avg_frame_time)}")
    sys.stdout.flush()
    
    
