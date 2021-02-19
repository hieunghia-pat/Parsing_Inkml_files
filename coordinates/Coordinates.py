class TCoordinate:
    def __init__(self, coordinates):
        self.coordinate_template = coordinates
        self.x_coordinates = []
        self.y_coordinates = []

        self.xmax, self.xmin = 0, 0
        self.ymax, self.ymin = 0, 0

    def parsing_coordinates(self):
        x_y_temps = self.coordinate_template.split(",")
        while "" in x_y_temps:
            x_y_temps.remove("")
        for x_y_temp in x_y_temps:
            temp = x_y_temp.strip().split(" ")
            x, y = temp[0], temp[1]
            self.x_coordinates.append(int(x))
            self.y_coordinates.append(int(y))

        self.xmax = max(self.x_coordinates)
        self.xmin = min(self.x_coordinates)
        
        self.ymax = max(self.y_coordinates)
        self.ymin = min(self.y_coordinates)