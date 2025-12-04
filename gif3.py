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
        gif = Image.open("BusBlinker/clap.gif")
        try:
            num_frames = gif.n_frames
        except Exception:
            sys.exit("provided image is not a gif")
        
        frames = []
        canvas = self.matrix.CreateFrameCanvas()
        print("Preprocessing gif, this may take a moment depending on the size of the gif...")
        for frame_index in range(0, num_frames):
            gif.seek(frame_index)
            # must copy the frame out of the gif, since thumbnail() modifies the image in-place
            frame = gif.copy()
            frame.thumbnail((self.matrix.width, self.matrix.height), Image.LANCZOS)
            
            img = (frame.convert("RGB")).rotate(90, expand=True)
            
            new_width = img.width 
            new_height = img.height + 15
            new_img = Image.new("RGB", (new_width, new_height), color=(0, 0, 0))
            new_img.paste(img, (15, 0))

            frames.append(new_img)

        # Close the gif file to save memory now that we have copied out all of the frames
        gif.close()

        print("Completed Preprocessing, displaying gif")

        try:
            print("Press CTRL-C to stop.")

            # Infinitely loop through the gif
            cur_frame = 0
            while(True):
                canvas.SetImage(frames[cur_frame])
                self.matrix.SwapOnVSync(canvas, framerate_fraction=10)
                if cur_frame == num_frames - 1:
                    cur_frame = 0
                else:
                    cur_frame += 1
        except KeyboardInterrupt:
            sys.exit(0)



# Main function
if __name__ == "__main__":
    simple_square = test()
    if (not simple_square.process()):
        simple_square.print_help()
