#!/usr/bin/env python
import sys
import os
import time
from datetime import datetime
import digit_maps
from PIL import Image

from busData import myMain, fetchTemp
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from samplebase import SampleBase
import numpy as np

global temp
temp = None

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


def makeRegMatrix(fetch_weather):
    arrCanv = np.zeros((64, 32), dtype=int)
    global temp
    off = 1
    print("0a")
    N, S = myMain()
    print("0b")
    
    # NORTH
    try:
        draw_string(arrCanv, "N", off + 1, 0, color=1)
        if N != None:
            min, sec = N["time_left"][0], N["time_left"][1]
            if min > 59:
                s = str(min // 60) + "_H"
            elif min > 9:
                s = str(min) + "_M"
            else:
                s = str(min) + ":" + str(sec).zfill(2)
    except Exception as e:
        print("Error drawing N:", e)
    finally:
        draw_string(arrCanv, s, off + 1, 8, color=3)
    
    # SOUTH
    try:
        draw_string(arrCanv, "S", off + 10*1, 0, color=1)
        if S != None:
            min, sec = S["time_left"][0], S["time_left"][1]
            if min > 59:
                s = str(min // 60) + "_H"
            elif min > 9:
                s = str(min) + "_M"
            else:
                s = str(min) + ":" + str(sec).zfill(2)
    except Exception as e:
        print("Error drawing S:", e)
    finally:
        draw_string(arrCanv, s, off + 10*1, 8, color=3)
    
    # WEATHER
    if fetch_weather:
        try:
            temp = str(fetchTemp())
        except Exception as e:
            print("Error fetching weather:", e)
    if temp != None:
        draw_string(arrCanv, temp+"^F", off + 10*2, 5, color=9)
    
    # TIME INFO
    now = datetime.now()
    date = now.strftime("%m/%d")
    day_of_week = now.strftime("%a")
    hour_min = now.strftime("%I:%M")
    draw_string(arrCanv, day_of_week.upper().strip(), off + 10*3, 7, color=6) # FRI
    draw_string(arrCanv, date, off + 10*4, 0, color=5) # 12/05
    draw_string(arrCanv, hour_min, off + 10*5, 2, color=5) # 01:04
    
    end = np.rot90(arrCanv, k=1)
    print("0end")
    return end


class test(SampleBase):
    def __init__(self, *args, **kwargs):
        super(test, self).__init__(*args, **kwargs)
    
    def setMatrixOnCanvas(self, array, canvas):
        for y in range(2, array.shape[0]):
            for x in range(array.shape[1]):
                if array[y, x] == 1:
                    a = 20
                    canvas.SetPixel(x, y, 153+a, 54+a, 199+a) # purp 
                elif array[y, x] == 2:
                    canvas.SetPixel(x, y, 0, 255, 0) # G 
                elif array[y, x] == 3:
                    a = 0
                    canvas.SetPixel(x, y, 255 + a, 255 + a, 255 + a) # W
                elif array[y, x] == 4:
                    canvas.SetPixel(x, y, 127, 164, 199) # LB
                elif array[y, x] == 5:
                    canvas.SetPixel(x, y, 98, 174, 179) # LB2 
                elif array[y, x] == 6:
                    canvas.SetPixel(x, y, 178, 232, 116) # lg
                elif array[y, x] == 7:
                    a = 40
                    canvas.SetPixel(x, y, 5+a, 86+a, 165+a) # uiuc B
                elif array[y, x] == 8:
                    canvas.SetPixel(x, y, 255, 95, 5) # uiuc OR
                elif array[y, x] == 9:
                    a = 70
                    canvas.SetPixel(x, y, 168 + a, 56 + a, 69 + a) # Old Rose
                elif array[y, x] == 10:
                    a = 0
                    canvas.SetPixel(x, y, 171+a, 171+a, 171+a) # Grey
                else:
                    canvas.SetPixel(x, y, 0, 0, 0)  

    def run(self):
        canvas = self.matrix.CreateFrameCanvas()
        i = 0
        while True:
            i += 1
            i = i % (60 * 60) # every 60 min refetch weather
            fetch_weather = i == 1
            try:
                print("0")
                mat = makeRegMatrix(fetch_weather) 
                print("1")
                self.setMatrixOnCanvas(mat, canvas)
                print("2")
                canvas = self.matrix.SwapOnVSync(canvas) # Refreshes the canvas
            except Exception as e:
                print("Error in main loop:", e)
            time.sleep(1)



# Main function
if __name__ == "__main__":
    simple_square = test()
    if (not simple_square.process()):
        simple_square.print_help()
