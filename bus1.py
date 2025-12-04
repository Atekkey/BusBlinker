#!/usr/bin/env python
import sys
import os
import time
from datetime import datetime
import digit_maps
from PIL import Image

from busData import myMain


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from samplebase import SampleBase
import numpy as np

def makeTimeMatrix(input):
    rows = 7
    arrays = []
    digit_map = digit_maps.sevenByFive
    for char in input:
        arrays.append(digit_map[char])
        # Add spacing between digits
        arrays.append(np.zeros((rows, 1), dtype=int))
    
    # Combine horizontally
    full_array = np.hstack(arrays)
    padded = np.pad(full_array, ((65-9, 0), (0, 0)), mode='constant')
    padded2 = np.pad(padded, ((0, 0), (0, 3)), mode='constant')

    rotated = np.rot90(padded2, k=1)
    
    return rotated

def draw_char(canvas, char_array, top_left_row, top_left_col, color = 1):
    rows, cols = char_array.shape
    canvas[top_left_row:top_left_row+rows, top_left_col:top_left_col+cols] = char_array * color

def draw_string(canvas, text, start_row, start_col, spacing=1, color = 1):
    col = start_col
    sevenByFive = digit_maps.sevenByFive
    for char in text:
        if char in sevenByFive:
            char_array = sevenByFive[char]
            draw_char(canvas, char_array, start_row, col, color)
            col += char_array.shape[1] + spacing 


def makeRegMatrix():
    arrCanv = np.zeros((64, 32), dtype=int)
    off = 1
    busInfo = myMain()
    for bus in busInfo:
        if 'N' in bus["headsign"]:
            s = str(bus["time_left"][0])[-1] + ":" + str(bus["time_left"][1]).zfill(2)
            draw_string(arrCanv, s, off + 1, 7, color=1)
        if 'S' in bus["headsign"]:
            s = str(bus["time_left"][0])[-1] + ":" + str(bus["time_left"][1]).zfill(2)
            draw_string(arrCanv, s, off + 10*1, 7, color=1)
        if 'E' in bus["headsign"]:
            s = str(bus["time_left"][0])[-1] + ":" + str(bus["time_left"][1]).zfill(2)
            draw_string(arrCanv, s, off + 10*2, 7, color=1)
    draw_string(arrCanv, "N", off + 1, 0, color=1)
    draw_string(arrCanv, "S", off + 10*1, 0, color=1)
    draw_string(arrCanv, "E", off + 10*2, 0, color=2)
    end = np.rot90(arrCanv, k=1)
    return end

print("reach")

class test(SampleBase):
    def __init__(self, *args, **kwargs):
        super(test, self).__init__(*args, **kwargs)
    
    def setMatrixOnCanvas(self, array, canvas):
        for y in range(2, array.shape[0]):
            for x in range(array.shape[1]):
                if array[y, x] == 1:
                    canvas.SetPixel(x, y, 153, 54, 199) # purp 
                elif array[y, x] == 2:
                    canvas.SetPixel(x, y, 0, 255, 0) # G 
                else:
                    canvas.SetPixel(x, y, 0, 0, 0)  
    
    def run(self):
        
        canvas = self.matrix.CreateFrameCanvas()
        
        while True:
            mat = makeRegMatrix() 
            self.setMatrixOnCanvas(mat, canvas)
            
            canvas = self.matrix.SwapOnVSync(canvas) # Refreshes the canvas
            time.sleep(1)



# Main function
if __name__ == "__main__":
    simple_square = test()
    if (not simple_square.process()):
        simple_square.print_help()
