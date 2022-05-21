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
labels = ["circle",
          "kite",
          "rectangle",
          "rhombus",
          "parallelogram",
          "square",
          "trapezoid",
          "triangle"]

# Default constants value
constants = {"PATH_DEST": os.getcwd(),
             "NUM_TRAIN": 3,
             "NUM_VAL": 3,
             "NUM_TEST": 10}
# Inject value by env variables
for key_constant in constants:
    try:
        if os.environ[key_constant]:
            # Validate number value
            value = os.environ[key_constant]
            constants[key_constant] = abs(int(value)) if key_constant.split("_")[0] == "NUM" else value
    except KeyError:
        print("{} enviroment variable is not set".format(key_constant))

base_dir = os.path.join(constants["PATH_DEST"], "dataset")
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
    def __init__(self, size_cnv, inc_time_noise, stroke_weight, list_color):
        self.size_cnv = size_cnv
        self.list_color = list_color
        self.inc_time_noise = inc_time_noise
        self.stroke_weight = stroke_weight
        self.ratio_margin_noise = 1.5 # 1.5 from stroke weight

    def line_noise(self, x1, y1, x2, y2, line_color, is_buff_x_horz):
        """Return line with Perlin Noise (like hand-drawn line)"""
        length_line = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        standar_length = 7 * self.stroke_weight
        ratio_margin = self.ratio_margin_noise
        if length_line < standar_length:
            ratio_margin = map(length_line, 0, standar_length, 0, ratio_margin)
        margin_off_noise = self.stroke_weight * ratio_margin
        stroke(line_color[0], line_color[1], line_color[2])
        strokeWeight(self.stroke_weight)
        noFill()
        beginShape()
        if abs(x1 - x2) < 5:
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
            if abs(is_buff_x_horz):
                x_obs = x_obs + noise_1d if is_buff_x_horz == 1 else x_obs - noise_1d
            vertex(x_obs, y)
            x_off += self.inc_time_noise
        endShape()

    def rotate_epi(self, deg):
        x_epi = float(self.size_cnv["width"]) / 2.0
        y_epi = float(self.size_cnv["height"]) / 2.0
        translate(x_epi - (x_epi * cos(radians(deg)) - y_epi * sin(radians(deg))),
                  y_epi - (y_epi * cos(radians(deg)) + x_epi * sin(radians(deg))))
        rotate(radians(deg))

    def render_shape(self, list_point, list_buff_x_horz):
        strokeWeight(self.stroke_weight)
        strokeCap(ROUND)
        for i in range(len(list_point)):
            j = 0 if i == len(list_point) - 1 else i + 1
            idx_color = int(random(len(self.list_color)))
            self.line_noise(x1=list_point[i][0],
                            y1=list_point[i][1],
                            x2=list_point[j][0],
                            y2=list_point[j][1],
                            line_color=self.list_color[idx_color],
                            is_buff_x_horz=list_buff_x_horz[i])

    def circle_gen(self, height_shape, width_shape, rotate_deg):
        """Return ellipse almost like circle with noise"""
        # Ref: https://saylordotorg.github.io/text_intermediate-algebra/s11-03-ellipses.html
        a = float(width_shape) / 2.0
        b = float(height_shape) / 2.0
        c = sqrt(a ** 2 + b ** 2)
        h = float(self.size_cnv["width"]) / 2.0
        k = float(self.size_cnv["height"]) / 2.0
        l = sqrt(h ** 2 + k ** 2)
        x_off = random(100)
        stack_vertex = []
        buff_noise = map(c, 0, l, 1, 2.5)
        margin_off_noise = self.stroke_weight * self.ratio_margin_noise * buff_noise
        for x_obs in range(floor(h - a) + 1, floor(h + a) + 1):
            s = sqrt(1 - (float(x_obs - h) / a) ** 2) * b
            noise_1d = map(noise(x_off), 0, 1, -margin_off_noise, margin_off_noise)
            stack_vertex.append((x_obs, floor(k + s + noise_1d)))
            stack_vertex.insert(0, (x_obs, floor(k - s + noise_1d)))
            x_off += self.inc_time_noise
        line_color = self.list_color[int(random(len(self.list_color)))]
        pushMatrix()
        self.rotate_epi(rotate_deg)
        stroke(line_color[0], line_color[1], line_color[2])
        strokeWeight(self.stroke_weight)
        noFill()
        beginShape()
        for coord in stack_vertex:
            vertex(coord[0], coord[1])
        endShape()
        popMatrix()

    def kite_gen(self, height_shape, width_shape, rotate_deg):
        """Return kite with diagonal horizontal = height_shape,
        diagonal vertical = width_shape and perlin noise 1D
        """
        # Ordinate (y) on diagonal vertical
        top_diag_vert = floor(float(self.size_cnv["height"] - height_shape) / 2.0)
        bot_diag_vert = self.size_cnv["height"] - top_diag_vert
        # Space for: top_diag_vert != intercept_diag != mid_diag_vert
        # Ratio a / b with a < b and ax + bx = length of diag_vert for real x
        ratio_diag_vert = random(2.0 / 16.0, 5.0 / 16.0)
        y_intercept_diag = top_diag_vert + floor(ratio_diag_vert * height_shape)
        x_epi_shape = floor(float(self.size_cnv["width"] / 2.0))
        # Axis (x) on diagonal horizontal
        left_diag_horz = floor(float(self.size_cnv["width"] - width_shape) / 2.0)
        right_diag_horz = self.size_cnv["width"] - left_diag_horz
        points = [(left_diag_horz, y_intercept_diag),
                  (x_epi_shape, top_diag_vert),
                  (right_diag_horz, y_intercept_diag),
                  (x_epi_shape, bot_diag_vert)]
        pushMatrix()
        self.rotate_epi(rotate_deg)
        self.render_shape(points, list_buff_x_horz=[0, 0, 1, -1])
        popMatrix()

    def rectangle_gen(self, height_shape, width_shape, rotate_deg):
        """Return rectangle with 4 points and center canvas position"""
        y_top_shape = floor(float(self.size_cnv["height"] - height_shape) / 2.0)
        y_bot_shape = self.size_cnv["height"] - y_top_shape
        x_left_shape = floor(float(self.size_cnv["width"] - width_shape) / 2.0)
        x_right_shape = self.size_cnv["width"] - x_left_shape
        points = [(x_left_shape, y_top_shape),
                  (x_right_shape, y_top_shape),
                  (x_right_shape, y_bot_shape),
                  (x_left_shape, y_bot_shape)]
        pushMatrix()
        self.rotate_epi(rotate_deg)
        self.render_shape(points, list_buff_x_horz=[0, 0, 0, 0])
        popMatrix()
        
    def rhombus_gen(self, height_shape, width_shape, rotate_deg):
        """Return rhombus with diagonal horizontal = height_shape,
        diagonal vertical = width_shape and perlin noise 1D
        """
        # Ordinate (y) on diagonal vertical
        top_diag_vert = floor(float(self.size_cnv["height"] - height_shape) / 2.0)
        bot_diag_vert = self.size_cnv["height"] - top_diag_vert
        # Intercept diagonal
        x_intercept_diag = floor(float(self.size_cnv["width"] / 2.0))
        y_intercept_diag = floor(float(self.size_cnv["height"] / 2.0))
        # Axis (x) on diagonal horizontal
        left_diag_horz = floor(float(self.size_cnv["width"] - width_shape) / 2.0)
        right_diag_horz = self.size_cnv["width"] - left_diag_horz
        points = [(left_diag_horz, y_intercept_diag),
                  (x_intercept_diag, top_diag_vert),
                  (right_diag_horz, y_intercept_diag),
                  (x_intercept_diag, bot_diag_vert)]
        pushMatrix()
        self.rotate_epi(rotate_deg)
        self.render_shape(points, list_buff_x_horz=[1, -1, 1, -1])
        popMatrix()

    def parallelogram_gen(self, height_shape, width_shape, rotate_deg, ratio_base, flip_horz):
        """Return parallelogram with ratio base (top-bot sides)"""
        # Standar of ratio base in range[0.25, 0.75]
        min_base = floor(ratio_base * width_shape)
        x_left_shape = floor(float(self.size_cnv["width"] - width_shape) / 2.0)
        x_right_shape = self.size_cnv["width"] - x_left_shape
        y_top_shape = floor(float(self.size_cnv["height"] - height_shape) / 2.0)
        y_bot_shape = self.size_cnv["height"] - y_top_shape
        points = [(x_right_shape - min_base, y_top_shape),
                  (x_right_shape, y_top_shape),
                  (x_left_shape + min_base, y_bot_shape),
                  (x_left_shape, y_bot_shape)]
        list_buff_x_horz = [0, 1, 0, 1]
        if flip_horz:
            points = [(x_left_shape, y_top_shape),
                      (x_left_shape + min_base, y_top_shape),
                      (x_right_shape, y_bot_shape),
                      (x_right_shape - min_base, y_bot_shape)]
            list_buff_x_horz = [0, -1, 0, -1]
        pushMatrix()
        self.rotate_epi(rotate_deg)
        self.render_shape(points, list_buff_x_horz)
        popMatrix()

    def square_gen(self, length_shape, rotate_deg):
        """Return square with 4 points and center canvas position"""
        self.rectangle_gen(length_shape, length_shape, rotate_deg)

    def trapezoid_gen(self, height_shape, width_shape, rotate_deg, ratio_parallel, flip_vert):
        """Return trapezoid with one pair of parallel sides (determine by ratio)
        Support isosceles, right-angle, and any trapezoid
        """
        # Standar of ratio parallel in range[0.25, 0.75]
        min_parallel = floor(ratio_parallel * width_shape)
        x_left_shape = floor(float(self.size_cnv["width"] - width_shape) / 2.0)
        x_right_shape = self.size_cnv["width"] - x_left_shape
        y_top_shape = floor(float(self.size_cnv["height"] - height_shape) / 2.0)
        y_bot_shape = self.size_cnv["height"] - y_top_shape
        space_unshape = floor(random(x_left_shape, x_right_shape - min_parallel))
        points = [(space_unshape, y_top_shape),
                  (space_unshape + min_parallel, y_top_shape),
                  (x_right_shape, y_bot_shape),
                  (x_left_shape, y_bot_shape)]
        list_buff_x_horz = [0, -1, 0, 1]
        if flip_vert:
            points = [(x_left_shape, y_top_shape),
                      (x_right_shape, y_top_shape),
                      (space_unshape + min_parallel, y_bot_shape),
                      (space_unshape, y_bot_shape)]
            list_buff_x_horz = [0, 1, 0, -1]
        pushMatrix()
        self.rotate_epi(rotate_deg)
        self.render_shape(points, list_buff_x_horz)
        popMatrix()

    def triangle_gen(self, height_shape, width_shape, rotate_deg, flip_vert):
        """Return triangle with base equals to width_shape
        Support equilateral, isosceles, right-angle, and any triangle
        """
        x_left_shape = floor(float(self.size_cnv["width"] - width_shape) / 2.0)
        x_right_shape = self.size_cnv["width"] - x_left_shape
        y_top_shape = floor(float(self.size_cnv["height"] - height_shape) / 2.0)
        y_bot_shape = self.size_cnv["height"] - y_top_shape
        space_unshape = floor(random(x_left_shape, x_right_shape))
        points = [(space_unshape, y_top_shape),
                  (x_right_shape, y_bot_shape),
                  (x_left_shape, y_bot_shape)]
        list_buff_x_horz = [-1, 0, 1]
        if flip_vert:
            points = [(x_left_shape, y_top_shape),
                      (x_right_shape, y_top_shape),
                      (space_unshape, y_bot_shape)]
            list_buff_x_horz = [0, 1, -1]
        pushMatrix()
        self.rotate_epi(rotate_deg)
        self.render_shape(points, list_buff_x_horz)
        popMatrix()


# Initialize class
size_canvas = {"width": 224, 
               "height": 224}
shape_ = ShapesGenerator(size_cnv=size_canvas,
                         inc_time_noise=0.025,
                         stroke_weight=4,
                         list_color=[(0, 0, 0), # Black
                                     (255, 0, 0), # Red
                                     (160, 32, 255), # Purple
                                     (0, 32, 255), # Blue
                                     (0, 192, 0), # Green
                                     (255, 160, 16)]) # Orange


def setup():
    size(size_canvas["width"], size_canvas["height"])

img_counter = 0
# Order: start => train => val => test => stop
toggle_bool = True
base_class_dir = train_dir
def draw():
    global base_class_dir
    global img_counter
    global toggle_bool
    if img_counter == constants["NUM_TRAIN"]:
        base_class_dir = val_dir
    if img_counter == constants["NUM_TRAIN"] + constants["NUM_VAL"]:
        base_class_dir = test_dir
    if img_counter == constants["NUM_TRAIN"] + constants["NUM_VAL"] + constants["NUM_TEST"] - 1:
        noLoop()
    shape_.stroke_weight = int(random(4, 10))
    # Rectangle
    background(255)
    min_length = int(random(50, 150))
    max_length = int(random(min_length + 30, 200))
    shape_.rectangle_gen(height_shape=max_length if toggle_bool else min_length,
                         width_shape=min_length if toggle_bool else max_length,
                         rotate_deg=int(random(-5, 5)))
    save(os.path.join(base_class_dir, "rectangle", "rectangle-{}.jpg".format(img_counter)))
    # Circle
    background(255)
    max_length = int(random(min_length, min_length + 50))
    shape_.circle_gen(height_shape=max_length if toggle_bool else min_length,
                      width_shape=min_length if toggle_bool else max_length,
                      rotate_deg=int(random(-180, 180)))
    save(os.path.join(base_class_dir, "circle", "circle-{}.jpg".format(img_counter)))
    # Kite
    background(255)
    max_length = int(random(min_length + 30, 200))
    shape_.kite_gen(height_shape=max_length,
                    width_shape=min_length,
                    rotate_deg=int(random(-30, 30)))
    save(os.path.join(base_class_dir, "kite", "kite-{}.jpg".format(img_counter)))
    # Rhombus
    background(255)
    shape_.rhombus_gen(height_shape=max_length,
                       width_shape=min_length,
                       rotate_deg=int(random(-20, 20)))
    save(os.path.join(base_class_dir, "rhombus", "rhombus-{}.jpg".format(img_counter)))
    # Parallelogram
    background(255)
    min_length = int(random(50, 200))
    max_length = int(random(min_length, 200))
    shape_.parallelogram_gen(height_shape=min_length,
                             width_shape=max_length,
                             rotate_deg=int(random(-10, 10)),
                             ratio_base=random(0.4, 0.7),
                             flip_horz=toggle_bool)
    save(os.path.join(base_class_dir, "parallelogram", "parallelogram-{}.jpg".format(img_counter)))
    # Square
    background(255)
    shape_.square_gen(length_shape=int(random(50, 200)),
                      rotate_deg=int(random(-5, 5)))
    save(os.path.join(base_class_dir, "square", "square-{}.jpg".format(img_counter)))
    # Trapezoid
    background(255)
    shape_.trapezoid_gen(height_shape=min_length,
                         width_shape=max_length,
                         rotate_deg=int(random(-10, 10)),
                         ratio_parallel=random(0.35, 0.55),
                         flip_vert=toggle_bool)
    save(os.path.join(base_class_dir, "trapezoid", "trapezoid-{}.jpg".format(img_counter)))
    # Triangle
    background(255)
    min_length = int(random(50, 150))
    max_length = int(random(min_length, 180))
    shape_.triangle_gen(height_shape=max_length if toggle_bool else min_length,
                        width_shape=min_length if toggle_bool else max_length,
                        rotate_deg=int(random(-30, 30)),
                        flip_vert=toggle_bool)
    save(os.path.join(base_class_dir, "triangle", "triangle-{}.jpg".format(img_counter)))
    img_counter += 1
    toggle_bool = not toggle_bool
