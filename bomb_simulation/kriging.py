import numpy as np
from math import sqrt, exp
from bomb_simulation.grid import Grid


class Kriging:
    def __init__(self, heat_map):
        self.nugget = 0
        self.range = 8 #1/3 of range
        self.sill = 12
        self.sv_matrix = None
        self.lag_matrix = None
        self.heat_map = heat_map
        self.pp = None
        self.ppsv = None
        self.weights = None
        self.points = []
        self.pp_z = 0
        self.z_matrix = None

    def get_points(self):
        for y0 in range(self.heat_map.height):
            for x0 in range(self.heat_map.width):
                if self.heat_map.cells[x0][y0] > 0:
                    self.points.append([x0, y0])

    def calculate_lag_matrix(self):
        self.lag_matrix = np.zeros((len(self.points), len(self.points)), dtype=float)
        row = 0
        column = 0
        for p0 in self.points:
            for p1 in self.points:
                lag = sqrt(pow(p0[0] - p1[0], 2) + pow(p0[1] - p1[1], 2))
                self.lag_matrix[row][column] = lag
                column += 1
            row += 1
            column = 0

    def calculate_sv_matrix(self):
        # sv = lambda t: self.nugget + self.sill*(1 - exp(-t/self.range)) if t < self.range and t != 0 else 0
        sv = lambda t: self.nugget + self.sill*(1 - exp(-t/self.range)) if t != 0 else 0
        self.sv_matrix = np.array([[sv(h) for h in row] for row in self.lag_matrix])

        self.sv_matrix = np.c_[self.sv_matrix, np.zeros(len(self.points))]
        self.sv_matrix = np.c_[self.sv_matrix, np.zeros(len(self.points))]
        self.sv_matrix = np.c_[self.sv_matrix, np.zeros(len(self.points))]
        self.sv_matrix = np.r_[self.sv_matrix, [np.zeros(len(self.points)+3)]]
        self.sv_matrix = np.r_[self.sv_matrix, [np.zeros(len(self.points)+3)]]
        self.sv_matrix = np.r_[self.sv_matrix, [np.zeros(len(self.points)+3)]]

        num_rows = len(self.points) +3
        num_colmuns = len(self.points) + 3
        count = 0
        for point in self.points:
            self.sv_matrix[num_rows-1][count] = point[1]
            self.sv_matrix[num_rows-2][count] = point[0]
            self.sv_matrix[num_rows-3][count] = 1
            self.sv_matrix[count][num_colmuns-1] = point[1]
            self.sv_matrix[count][num_colmuns-2] = point[0]
            self.sv_matrix[count][num_colmuns-3] = 1
            count += 1
        #print(self.sv_matrix)

    def calculate_prediction_point(self, pX, pY):
        pp_lag = lambda t: sqrt(pow(t[0] - pX, 2) + pow(t[1] - pY, 2))
        self.pp = np.array([pp_lag(row) for row in self.points])

    def calculate_sv_pp(self):
        # ppsv = lambda t: self.sill*(1 - exp(-t/self.range)) if t < self.range and t != 0 else 0
        ppsv = lambda t: self.nugget + self.sill*(1 - exp(-t/self.range)) if t != 0 else 0
        self.ppsv = np.array([ppsv(h) for h in self.pp])
        self.ppsv = np.r_[self.ppsv, np.ones(3)]

    def calculate_weights(self):
        temp = np.linalg.inv(self.sv_matrix)
        self.weights = np.dot(temp, self.ppsv)
        self.weights = np.delete(self.weights, -1, 0)
        self.weights = np.delete(self.weights, -1, 0)
        self.weights = np.delete(self.weights, -1, 0)

    def calculate_z(self):
        z = lambda t: self.heat_map.cells[t[0]][t[1]]
        self.z_matrix = np.array([z(p) for p in self.points])
        self.pp_z = np.inner(self.z_matrix, self.weights)
        # sum = 0
        # for i in range(len(self.z_matrix)):
        #     sum += self.z_matrix[i] * self.weights[i]
        # self.pp_z = sum

    def setup(self):
        self.get_points()
        if len(self.points) < 3:
            print(len(self.points), 'is not enough points')
            return False
        else:
            print(len(self.points), 'is enough points')
            self.calculate_lag_matrix()
            self.calculate_sv_matrix()
            return True

    def get_estimate(self, x, y):
        self.calculate_prediction_point(x, y)
        self.calculate_sv_pp()
        self.calculate_weights()
        self.calculate_z()
        return self.pp_z


if __name__ == "__main__":
    np.set_printoptions(linewidth=300, precision=3)
    heat_map = Grid(16, 16)
    heat_map.init_bomb(3, 3, 10)
    # heat_map.cells[0][0] = 1
    # heat_map.cells[1][0] = 2
    # heat_map.cells[2][0] = 4
    # heat_map.cells[0][1] = 5
    # heat_map.cells[0][2] = 6
    # heat_map.cells[2][2] = 27


    k = Kriging(heat_map)
    k.setup()
    #print('\nLag')
    #print(k.lag_matrix)

    #print('\nSV')
    #print(k.sv_matrix)



    #print('\nPP')
    #print(k.pp)
    #print('\nPP SV')
    #print(k.ppsv)

    #print('\nWeights')
    #print(k.weights)
    #print('\nZ')
    #print(k.pp_z)


    for x in range(16):
        for y in range(16):
            result = k.get_estimate(x, y)
            print("Estimate for (%2d,%2d)" % (x, y), str("%4.1f" % result), heat_map.cells[x][y], ' Error ' + str("%.1f" % (result - heat_map.cells[x][y])))
