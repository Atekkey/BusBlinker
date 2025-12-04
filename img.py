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


class test(SampleBase):
    def __init__(self, *args, **kwargs):
        super(test, self).__init__(*args, **kwargs)
    

    def run(self):
        img0 = Image.open("./crest.png").convert("RGB")
        img = img0.rotate(90, expand=True) 
        padding_top = 10
        new_width = img.width + padding_top
        new_height = img.height 
        new_img = Image.new("RGB", (new_width, new_height), color=(0, 0, 0))
        new_img.paste(img, (padding_top, 0))
        
        canvas = self.matrix.CreateFrameCanvas()
        while True:
            canvas.SetImage(new_img)
            canvas = self.matrix.SwapOnVSync(canvas) # Refreshes the canvas
            time.sleep(1)



# Main function
if __name__ == "__main__":
    simple_square = test()
    if (not simple_square.process()):
        simple_square.print_help()
