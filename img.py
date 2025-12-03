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
        img = Image.open("./BusBlinker/crest2.png").convert("RGB")
        img2 = img.rotate(90, expand=True) 
        canvas = self.matrix.CreateFrameCanvas()
        while True:
            canvas.SetImage(img2)
            canvas = self.matrix.SwapOnVSync(canvas) # Refreshes the canvas
            time.sleep(1)



# Main function
if __name__ == "__main__":
    simple_square = test()
    if (not simple_square.process()):
        simple_square.print_help()
