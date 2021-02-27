from random import randint
import numpy as np
import gc 
import cv2 as cv
from math import pi, tan, exp

class TTraceGroup:
    def __init__(self, _id, truth, traces, max_width, width):
        self._id = _id
        self.traces = traces
        self.truth = truth
        self.max_width = max_width
        self.width = width

        self.xmax = max([trace.coordinates.xmax for trace in self.traces])
        self.xmin = min([trace.coordinates.xmin for trace in self.traces])

        self.ymax = max([trace.coordinates.ymax for trace in self.traces])
        self.ymin = min([trace.coordinates.ymin for trace in self.traces])

        self.delta_x = self.xmax - self.xmin
        self.delta_y = self.ymax - self.ymin

    def get_size(self):
        return self.delta_x, self.delta_y
        
    def create_image(self):
        # get the new width and height
        w = round((self.delta_x / self.max_width) * self.width)
        scale = self.delta_x / self.delta_y
        h = round(w / scale)

        img = np.ones(shape=(h, w, 3)) * 255

        x_coords, y_coords = [], []
        for trace in self.traces:
            x_coords.append((np.array(trace.coordinates.x_coordinates) - self.xmin) / self.delta_x * w)
            y_coords.append((np.array(trace.coordinates.y_coordinates) - self.ymin) / self.delta_y * h)

        def get_color(x):
            alpha = 0.7 
            value = 1 / (1 + exp(-alpha * x))
            thickness = value * 3 
            color = value * 5 

            return round(thickness), round(color)

        for xs, ys in zip(x_coords, y_coords):
            duration = len(xs)
            for i in range(2, duration):
                pt1 = (round(xs[i-1]), round(ys[i-1]))
                pt2 = (round(xs[i]), round(ys[i]))
                if ((i / duration) <= 0.05) or ((i / duration) >= 0.95):
                    img = cv.line(img, pt1, pt2, (5, 5, 5), thickness=1, lineType=cv.LINE_8)
                else:
                    delta_x = abs(xs[i-1]- xs[i])
                    delta_y = abs(ys[i-1]- ys[i])
                    dy_dx = delta_y / delta_x if delta_x != 0 else 10e10
                    thickness, color = get_color(dy_dx)
                    img = cv.line(img, pt1, pt2, (color, color, color), thickness=thickness, lineType=cv.LINE_8)

        return img, self.truth

    def show_image(self):
        cv.namedWindow("image")
        print(self.truth)
        print("Press any key to close the image window")
        
        img, _ = self.create_image()
        cv.imshow("image", img)
        cv.waitKey()
        cv.destroyAllWindows()

        del img
        gc.collect()

    def save_image(self, img_name):
        img = self.create_image()
        width, heigth = img.shape[1], img.shape[0]
        width *= 0.4
        heigth *= 0.4
        img = cv.resize(img, (int(width), int(heigth)), interpolation=cv.INTER_AREA)
        cv.imwrite(img_name, img)