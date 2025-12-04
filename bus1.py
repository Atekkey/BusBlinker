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
MAP = {"M":"MON", "T":"TUE", "W":"WED", "H":"THU", "F":"FRI", "S":"SAT", "U":"SUN"}

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
            draw_string(arrCanv, s, off + 1, 7, color=3)
        if 'S' in bus["headsign"]:
            s = str(bus["time_left"][0])[-1] + ":" + str(bus["time_left"][1]).zfill(2)
            draw_string(arrCanv, s, off + 10*1, 7, color=3)
        if 'E' in bus["headsign"]:
            s = str(bus["time_left"][0])[-1] + ":" + str(bus["time_left"][1]).zfill(2)
            draw_string(arrCanv, s, off + 10*2, 7, color=3)
    draw_string(arrCanv, "N", off + 1, 0, color=1)
    draw_string(arrCanv, "S", off + 10*1, 0, color=1)
    draw_string(arrCanv, "E", off + 10*2, 0, color=2)

    now = datetime.now()
    date = now.strftime("%m/%d")
    day_of_week = now.strftime("%a").upper()
    # print("\n", day_of_week, "\n")
    # day_of_week = MAP[day_of_week.upper()].upper()
    draw_string(arrCanv, day_of_week, off + 10*3, 0, color=1)
    draw_string(arrCanv, date, off + 10*4, 4, color=5)
    hour_min = now.strftime("%I:%M")
    draw_string(arrCanv, hour_min, off + 10*5, 4, color=4)
    
    end = np.rot90(arrCanv, k=1)
    return end


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
                elif array[y, x] == 3:
                    canvas.SetPixel(x, y, 255, 255, 255) # W
                elif array[y, x] == 4:
                    canvas.SetPixel(x, y, 127, 164, 199) # LB
                elif array[y, x] == 5:
                    canvas.SetPixel(x, y, 98, 174, 179) # LB2
                else:
                    canvas.SetPixel(x, y, 0, 0, 0)  
    
    def run(self):
        
        canvas = self.matrix.CreateFrameCanvas()
        
        while True:
            mat = makeRegMatrix() 
            self.setMatrixOnCanvas(mat, canvas)
            
            canvas = self.matrix.SwapOnVSync(canvas) # Refreshes the canvas
            time.sleep(0.9)



# Main function
if __name__ == "__main__":
    simple_square = test()
    if (not simple_square.process()):
        simple_square.print_help()
