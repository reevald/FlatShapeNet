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
            ratio_margin = map(length_line, 0, 7 * self.stroke_weight, 0, ratio_margin)
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
        gradien = 0 if y1 == y2 else (y2 - y1) / (x2 - x1)
        for x_obs in range(x_min, x_max):
            noise_1d = map(noise(x_off), 0, 1, -margin_off_noise, margin_off_noise)
            y = gradien * (x_obs - x1) + y1 + noise_1d
            vertex(x_obs, y)
            x_off += self.inc_time_noise
        endShape()


# Initialize class
size_canvas = {
            "width": 224, 
            "height": 224
            }
shape_ku = ShapesGenerator(size_cnv=size_canvas,
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

# Testing
def draw():
    background(51)
    shape_ku.stroke_weight = 8
    shape_ku.line_noise(100, 20, 100, 50, (155, 140, 0))
    stroke(255, 0, 0)
    line(150, 20, 150, 50)
    noLoop()
    
