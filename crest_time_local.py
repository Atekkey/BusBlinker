#!/usr/bin/env python
import sys
import os
import time
from datetime import datetime
import digit_maps
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from samplebase import SampleBase
    HAS_SAMPLEBASE = True
except ImportError:
    HAS_SAMPLEBASE = False

import numpy as np

def makeTimeMatrix(input):
    rows = 7
    arrays = []
    digit_map = digit_maps.sevenByFive
    for char in input:
        arrays.append(digit_map[char]*2)
        # Add spacing between digits
        arrays.append(np.zeros((rows, 1), dtype=int))
    
    # Combine horizontally
    full_array = np.hstack(arrays)
    padded = np.pad(full_array, ((65-9, 0), (0, 0)), mode='constant')
    padded2 = np.pad(padded, ((0, 0), (0, 3)), mode='constant')

    rotated = np.rot90(padded2, k=1)


    return rotated


def render_matrix_local(matrix, crest_image_path=None, scale=10):
    """
    Render the LED matrix locally using matplotlib.

    Args:
        matrix: numpy array where 0=off, 1=gray, 2=red
        crest_image_path: optional path to crest image to overlay
        scale: pixel size for display
    """
    # Create RGB image from matrix
    height, width = matrix.shape
    rgb_image = np.zeros((height, width, 3), dtype=np.uint8)

    # Map values to colors: 0=black, 1=gray, 2=red
    rgb_image[matrix == 1] = [155, 155, 155]  # Gray
    rgb_image[matrix == 2] = [255, 0, 0]      # Red
    # 0 stays black (default)

    # If crest image provided, overlay it
    if crest_image_path and os.path.exists(crest_image_path):
        img0 = Image.open(crest_image_path).convert("RGB")
        img = img0.rotate(90, expand=True)
        padding_top = 10

        # Convert to numpy and overlay
        img_array = np.array(img)

        # Place the image with padding
        for y in range(min(img_array.shape[0], height)):
            for x in range(min(img_array.shape[1], width - padding_top)):
                if x + padding_top < width:
                    pixel = img_array[y, x]
                    if not (pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0):
                        rgb_image[y, x + padding_top] = pixel

    # Display with matplotlib
    fig, ax = plt.subplots(figsize=(width / 6, height / 6))
    ax.imshow(rgb_image, interpolation='nearest')
    ax.set_title(f'LED Matrix Preview ({width}x{height})')
    ax.axis('off')

    # Add grid lines to show individual LEDs
    ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, height, 1), minor=True)
    ax.grid(which='minor', color='#333333', linestyle='-', linewidth=0.5)

    plt.tight_layout()
    plt.show()


def preview_local(text=None, crest_path="./crest2.png"):
    """
    Preview the matrix display locally without Arduino hardware.

    Args:
        text: The text to display (default: current time)
        crest_path: Path to the crest image (optional)
    """
    if text is None:
        now = datetime.now()
        text = now.strftime("%I:%M")
    print(f"Generating preview for: {text}")
    matrix = makeTimeMatrix(text)
    print(f"Matrix shape: {matrix.shape}")
    render_matrix_local(matrix, crest_path)


print("reach")

if HAS_SAMPLEBASE:
    class test(SampleBase):
        def __init__(self, *args, **kwargs):
            super(test, self).__init__(*args, **kwargs)

        def setMatrixOnCanvas(self, array, canvas):
            for y in range(2, array.shape[0]):
                for x in range(array.shape[1]):
                    if array[y, x] == 1:
                        canvas.SetPixel(x, y, 155, 155, 155) # Gray
                    if array[y, x] == 2:
                        canvas.SetPixel(x, y, 255, 0, 0) # Red
                    else:
                        canvas.SetPixel(x, y, 0, 0, 0)

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
                matrix = makeTimeMatrix(hour_min) 
                self.setMatrixOnCanvas(matrix, canvas)
                canvas.SetImage(new_img)
                canvas = self.matrix.SwapOnVSync(canvas) # Refreshes the canvas
                time.sleep(10)



# Main function
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='LED Matrix Display')
    parser.add_argument('--local', '-l', action='store_true',
                        help='Run in local preview mode (no hardware required)')
    parser.add_argument('--text', '-t', type=str, default=None,
                        help='Text to display (default: current time)')
    parser.add_argument('--crest', '-c', type=str, default='./BusBlinker/crest2.png',
                        help='Path to crest image')

    args, remaining = parser.parse_known_args()

    if args.local or not HAS_SAMPLEBASE:
        if not HAS_SAMPLEBASE:
            print("SampleBase not available, running in local preview mode")
        preview_local(args.text, args.crest)
    else:
        simple_square = test()
        if (not simple_square.process()):
            simple_square.print_help()
