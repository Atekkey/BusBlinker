#!/usr/bin/env python
import sys
import os
import time
from datetime import datetime
import digit_maps
from PIL import Image


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from samplebase import SampleBase
import numpy as np

def makeTimeMatrix(input):
    rows = 5
    arrays = []
    digit_map = digit_maps.fiveByThree
    for char in input:
        arrays.append(digit_map[char])
        # Add spacing between digits
        arrays.append(np.zeros((rows, 1), dtype=int))

    # Combine horizontally
    full_array = np.hstack(arrays)
    padded = np.pad(full_array, ((65-7, 0), (0, 0)), mode='constant')
    padded2 = np.pad(padded, ((0, 0), (0, 2)), mode='constant')

    rotated = np.rot90(padded2, k=1)
    

    return rotated

print("reach")

class test(SampleBase):
    def __init__(self, *args, **kwargs):
        super(test, self).__init__(*args, **kwargs)
    
    def setMatrixOnCanvas(self, array, canvas):
        for y in range(30, array.shape[0]):
            for x in range(10, array.shape[1]):
                if array[y, x] == 1:
                    canvas.SetPixel(x, y, 255, 0, 0)  # red
                else:
                    canvas.SetPixel(x, y, 0, 0, 0)    # off

    def run(self):
        img0 = Image.open("./BusBlinker/crest2.png").convert("RGB")
        img = img0.rotate(90, expand=True) 
        padding_top = 10
        new_width = img.width + padding_top
        new_height = img.height 
        new_img = Image.new("RGB", (new_width, new_height), color=(0, 0, 0))
        new_img.paste(img, (padding_top, 0))

        canvas = self.matrix.CreateFrameCanvas()
        
        while True:
            now = datetime.now()
            hour_min = now.strftime("%I:%M")
            sec = now.strftime("%S").zfill(2)
            matrix = makeTimeMatrix(hour_min + ":" +sec)
            self.setMatrixOnCanvas(matrix, canvas)
            canvas.SetImage(new_img)
            canvas = self.matrix.SwapOnVSync(canvas) # Refreshes the canvas
            time.sleep(1)



# Main function
if __name__ == "__main__":
    simple_square = test()
    if (not simple_square.process()):
        simple_square.print_help()
