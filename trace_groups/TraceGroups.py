import numpy as np
import gc 
import cv2 as cv

class TTraceGroup:
    def __init__(self, _id, truth, traces, thickness=10):
        self._id = _id
        self.traces = traces
        self.truth = truth
        self.thickness = thickness

        self.xmax = max([trace.coordinates.xmax for trace in self.traces])
        self.xmin = min([trace.coordinates.xmin for trace in self.traces])

        self.ymax = max([trace.coordinates.ymax for trace in self.traces])
        self.ymin = min([trace.coordinates.ymin for trace in self.traces])

        self.delta_x = self.xmax - self.xmin + 40
        self.delta_y = self.ymax - self.ymin + 40
        
    def create_image(self):
        img = np.ones(shape=(self.delta_y, self.delta_x, 3))
        img = np.full_like(img, 255)

        x_coords, y_coords = [], []
        for trace in self.traces:
            x_coords.append(np.array(trace.coordinates.x_coordinates) - self.xmin + 20)
            y_coords.append(np.array(trace.coordinates.y_coordinates) - self.ymin + 20)

        for xs, ys in zip(x_coords, y_coords):
            for i in range(2, len(xs)):
                pt1 = (xs[i-1], ys[i-1])
                pt2 = (xs[i], ys[i])
                cv.line(img, pt1, pt2, (0, 0, 0), thickness=self.thickness, lineType=cv.FILLED)

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