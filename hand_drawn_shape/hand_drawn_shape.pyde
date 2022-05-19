# Copyright 2022 Mochammad Galang Rivaldo

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# Import libraries
import os


# Folder preparation
labels = [
         "circle",
         "kite",
         "rectangle",
         "rhombus",
         "parallelogram",
         "square",
         "trapezoid",
         "triangle"
]
base_dir = os.path.join(os.getcwd(), "dataset")
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "val")
test_dir = os.path.join(base_dir, "test")

try:
    os.mkdir(base_dir)
    for parent_dir in [train_dir, val_dir, test_dir]:
        os.mkdir(parent_dir)
        for child_dir in [os.path.join(parent_dir, lb) for lb in labels]:
            os.mkdir(child_dir)
    print("Create directory successfully!")
except OSError as err:
    print("Unable create directory, {}".format(err))


# Blueprint shapes
class ShapesGenerator():
    def __init__(self, size_cnv, inc_time_noise, stroke_weight, list_color, weights_color):
        self.size_cnv = size_cnv
        self.list_color = list_color
        self.weights_color = weights_color
        self.inc_time_noise = inc_time_noise
        self.stroke_weight = stroke_weight

    def line_noise(self, x1, y1, x2, y2, line_color):
        """Return line with Perlin Noise (like hand-drawn line)"""
        length_line = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        ratio_margin = 1.5 # 1.5 * stroke_weight
        standar_length = 7 * self.stroke_weight
        if length_line < standar_length:
            ratio_margin = map(length_line, 0, standar_length, 0, ratio_margin)
        margin_off_noise = self.stroke_weight * ratio_margin
        stroke(line_color[0], line_color[1], line_color[2])
        strokeWeight(self.stroke_weight)
        noFill()
        beginShape()
        if x1 == x2:
            y_min = y1 if y1 < y2 else y2
            y_max = y1 if y1 > y2 else y2
            # Time for perlin noise from random number (prevent same noise)
            y_off = random(100)
            for y_obs in range(y_min, y_max):
                # Noise return value in range [0, 1]
                noise_1d = map(noise(y_off), 0, 1, -margin_off_noise, margin_off_noise)
                x = x1 + noise_1d
                vertex(x, y_obs)
                y_off += self.inc_time_noise
            endShape()
            return

        x_min = x1 if x1 < x2 else x2
        x_max = x1 if x1 > x2 else x2
        x_off = random(100)
        gradien = 0 if y1 == y2 else float(y2 - y1) / float(x2 - x1)
        for x_obs in range(x_min, x_max):
            noise_1d = map(noise(x_off), 0, 1, -margin_off_noise, margin_off_noise)
            y = gradien * (x_obs - x1) + y1 + noise_1d
            vertex(x_obs, y)
            x_off += self.inc_time_noise
        endShape()

    def rotate_epi(self, deg):
        x_epi = float(self.size_cnv["width"]) / 2.0
        y_epi = float(self.size_cnv["height"]) / 2.0
        translate(
                  x_epi - (x_epi * cos(radians(deg)) - y_epi * sin(radians(deg))),
                  y_epi - (y_epi * cos(radians(deg)) + x_epi * sin(radians(deg)))
                  )
        rotate(radians(deg))

    def render_shape(self, list_point):
        strokeWeight(self.stroke_weight)
        strokeCap(ROUND)
        for i, p in enumerate(list_point):
            j = 0 if i == len(list_point) - 1 else i + 1
            self.line_noise(
                            x1=list_point[i][0],
                            y1=list_point[i][1],
                            x2=list_point[j][0],
                            y2=list_point[j][1],
                            line_color=self.list_color[:4][i]
                            )

    def rectangle_gen(self, height_shape, width_shape, rotate_deg):
        """Create rectangle with 4 points and center canvas position"""
        y_top_shape = floor(float(self.size_cnv["height"] - height_shape) / 2.0)
        y_bot_shape = self.size_cnv["height"] - y_top_shape
        x_left_shape = floor(float(self.size_cnv["width"] - width_shape) / 2.0)
        x_right_shape = self.size_cnv["width"] - x_left_shape
        points = [
                  (x_left_shape, y_top_shape),
                  (x_right_shape, y_top_shape),
                  (x_right_shape, y_bot_shape),
                  (x_left_shape, y_bot_shape)
                  ]
        self.rotate_epi(rotate_deg)
        self.render_shape(points)

# Initialize class
size_canvas = {
            "width": 224, 
            "height": 224
            }
shape_ = ShapesGenerator(size_cnv=size_canvas,
                         inc_time_noise=0.025,
                         stroke_weight=4,
                         list_color=[
                                     (0, 0, 0), # Black
                                     (255, 0, 0), # Red
                                     (160, 32, 255), # Purple
                                     (0, 32, 255), # Blue
                                     (0, 192, 0), # Green
                                     (255, 160, 16) # Orange
                                     ],
                         weights_color=[
                                        0.167, 0.167, 0.167, 0.167,
                                        0.167, 0.167, 0.167, 0.167
                         ])


def setup():
    size(size_canvas["width"], size_canvas["height"])
    noLoop()


# Testing
def draw():
    background(51)
    shape_.rectangle_gen(150, 150, -3)
    
