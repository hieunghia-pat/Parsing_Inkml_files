import numpy as np
import gc 
import cv2 as cv

class TTraceGroup:
    def __init__(self, _id, truth, traces, size, thickness=2):
        self._id = _id
        self.traces = traces
        self.truth = truth
        self.thickness = thickness
        self.size = size

        self.xmax = max([trace.coordinates.xmax for trace in self.traces])
        self.xmin = min([trace.coordinates.xmin for trace in self.traces])

        self.ymax = max([trace.coordinates.ymax for trace in self.traces])
        self.ymin = min([trace.coordinates.ymin for trace in self.traces])

        self.delta_x = self.xmax - self.xmin
        self.delta_y = self.ymax - self.ymin
        
    def create_image(self):
        w = self.size[0]
        scale = self.delta_x / self.delta_y
        h = w / scale

        img = np.ones(shape=(int(h), int(w), 3))
        img = np.full_like(img, 255)

        x_coords, y_coords = [], []
        for trace in self.traces:
            x_coords.append((np.array(trace.coordinates.x_coordinates) - self.xmin) / self.delta_x * w)
            y_coords.append((np.array(trace.coordinates.y_coordinates) - self.ymin) /self.delta_y * h)

        for xs, ys in zip(x_coords, y_coords):
            for i in range(2, len(xs)):
                pt1 = (int(xs[i-1]), int(ys[i-1]))
                pt2 = (int(xs[i]), int(ys[i]))
                cv.line(img, pt1, pt2, (0, 0, 0), thickness=2, lineType=cv.FILLED)

        return img

    def show_image(self):
        cv.namedWindow("image")
        print(self.truth)
        print("Press any key to close the image window")
        img = self.create_image()
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