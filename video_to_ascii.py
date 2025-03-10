from PIL import Image
import statistics
import cv2
import os
import time

# replace with whatever video path you want
video_path = "image_to_text/【東方】Bad Apple!! ＰＶ【影絵】.mp4"
cap = cv2.VideoCapture(video_path)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

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

    # scaling function
    def scale(width, height):
        scale_factor = max(width, height) / 130  # set the resolution here
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

            # convert the rgb value of the pixel to a grayscale, then normalize to a range of 23 for the ascii chars
            grayscale = ((0.2989 * pixel[0] + 0.5870 * pixel[1] + 0.1140 * pixel[2])/255)*23
            current_line.append(int(grayscale))

            #print(f"Grayscale: {grayscale}, RGB: {pixel}, ASCII: {ascii_grayscale[int(grayscale)]}")
        
        # on the second row and onward, compare the current and previous row and turn them into one averaged row
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

    # clear the terminal and print the next frame (steady ouput)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(text_image)
    print(f"Resolution:{resize}, Frame {frame_number}/{length}, Frametime: {(end-start)*1000}ms")
