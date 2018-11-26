import numpy as np
from math import sqrt, exp
from bomb_simulation.grid import Grid


class EasyKriging:
    def __init__(self, heat_map, px, py):
        self.heat_map = heat_map
        self.weights = []
        self.points = []
        self.px = px
        self.py = py
        self.estimate = 0

    def get_points(self):
        for y0 in range(self.heat_map.height):
            for x0 in range(self.heat_map.width):
                if self.heat_map.cells[x0][y0] > 0 and (x0 != self.px or y0 != self.py):
                    self.points.append([x0, y0, self.heat_map.cells[x0][y0], sqrt(pow(x0 - self.px, 2) +
                                                                                  pow(y0 - self.py, 2))])

    def calculate_weights(self):
        total = 0
        inverseDistance = []
        for row in self.points:
            inverse = 1 / row[3]
            inverseDistance.append(inverse)
            total += inverse

        for distance in inverseDistance:
            weight = distance / total
            self.weights.append(weight)

        print(total)


    def calculate_z(self):
        for index in range(len(self.points)):
            temp = self.weights[index] * self.points[index][2]
            # print(self.points[index][2], '->', temp)
            self.estimate += temp
            # print(self.estimate)
            # print(self.weights[index], '->', self.points[index][2])





if __name__ == "__main__":
    np.set_printoptions(linewidth=300, precision=3)
    heat_map = Grid(26,26)
    heat_map.init_bomb(2, 3, 10)
    # heat_map.cells[10][0] = 5
    # heat_map.cells[7][1] = 6
    # heat_map.cells[13][1] = 6
    # heat_map.cells[9][3] = 8
    # heat_map.cells[13][2] = 7
    # heat_map.cells[4][0] = 4
    # heat_map.cells[8][8] = 8
    # heat_map.cells[12][8] = 8
    # heat_map.cells[10][9] = 7

    k = EasyKriging(heat_map, 2, 3)
    k.get_points()
    print(k.points)
    k.calculate_weights()
    print(k.weights)
    k.calculate_z()
    print(k.estimate)
