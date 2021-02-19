import numpy as np 
import cv2 as cv

class TTrace:
    def __init__(self, _id, coordinates):
        self.id = _id
        self.coordinates = coordinates
        self.coordinates.parsing_coordinates()

    def show_image(self):
        img = np.ones(shape=(self.coordinates.delta_y, self.coordinates.delta_x, 3))
        img = np.full_like(img, 255)

        for i in range(1, len(self.coordinates.x_coordinates)):
            x1 = self.coordinates.x_coordinates[i-1] - self.coordinates.xmin
            y1 = self.coordinates.y_coordinates[i-1] - self.coordinates.ymin

            x2 = self.coordinates.x_coordinates[i] - self.coordinates.xmin
            y2 = self.coordinates.y_coordinates[i] - self.coordinates.ymin

            cv.line(img, (x1, y1), (x2, y2), color=(0, 0, 0), thickness=7, lineType=cv.FILLED)

        cv.namedWindow("image")
        print("Press any key to close the image window")
        cv.imshow("image", img)
        cv.waitKey()
        cv.destroyAllWindows()