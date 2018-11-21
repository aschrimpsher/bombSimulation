import numpy as np
from math import sqrt, exp
from bomb_simulation.grid import Grid


class Kriging:
    def __init__(self, heat_map):
        self.nugget = 0
        self.range = 10
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
        sv = lambda t: self.sill*(1 - exp(-3*t**2/self.range**2)) if t < self.range else 0
        self.sv_matrix = np.array([[sv(h) for h in row] for row in self.lag_matrix])
        self.sv_matrix = np.c_[self.sv_matrix, np.ones(len(self.points))]
        self.sv_matrix = np.r_[self.sv_matrix, [np.ones(len(self.points)+1)]]
        self.sv_matrix[-1, -1] = 0

    def calculate_prediction_point(self, pX, pY):
        pp_lag = lambda t: sqrt(pow(t[0] - pX, 2) + pow(t[1] - pY, 2))
        self.pp = np.array([pp_lag(row) for row in self.points])

    def calculate_sv_pp(self):
        ppsv = lambda t: self.sill*(1 - exp(-3*t**2/self.range**2)) if t < self.range else 0
        self.ppsv = np.array([ppsv(h) for h in self.pp])
        self.ppsv = np.r_[self.ppsv, np.ones(1)]


    def calculate_weights(self):
        temp = np.linalg.inv(self.sv_matrix)
        self.weights = np.dot(temp, self.ppsv)
        self.weights = np.delete(self.weights, -1, 0)

    def calculate_z(self):
        z = lambda t: self.heat_map.cells[t[0]][t[1]]
        self.z_matrix = np.array([z(p) for p in self.points])
        self.pp_z = np.inner(self.weights, self.z_matrix)
        if self.pp_z > 10:
            self.pp_z = 10
        elif self.pp_z < 0:
            self.pp_z = 0

    def setup(self):
        self.get_points()
        self.calculate_lag_matrix()
        self.calculate_sv_matrix()

    def get_estimate(self, x, y):
        self.calculate_prediction_point(15, 15)
        self.calculate_sv_pp()
        self.calculate_weights()
        self.calculate_z()
        return self.pp_z


if __name__ == "__main__":
    np.set_printoptions(linewidth=300, precision=3)
    heat_map = Grid(100, 100)
    heat_map.init_bomb(3, 3, 10)
    # heat_map.cells[10][0] = 5
    # heat_map.cells[7][1] = 6
    # heat_map.cells[13][1] = 6
    # heat_map.cells[9][3] = 8
    # heat_map.cells[13][2] = 7
    # heat_map.cells[4][0] = 4
    # heat_map.cells[8][8] = 8
    # heat_map.cells[12][8] = 8
    # heat_map.cells[10][9] = 7

    k = Kriging(heat_map)
    k.get_points()
    #print('Points')
    #print(k.points)
    k.calculate_lag_matrix()
    print('Lag')
    print(k.lag_matrix)
    k.calculate_sv_matrix()
    #print('SV')
    #print(k.sv_matrix)
    k.calculate_prediction_point(15,15)
    #print('Prediction Lag')
    #print(k.pp)
    k.calculate_sv_pp()
    #print('Prediction SV')
    #print(k.ppsv)
    k.calculate_weights()
    #print('Weights')
    #print(k.weights)
    k.calculate_z()
    #print('Z Matrix')
    #print(k.z_matrix)
    print('Estaimate for 15,15')
    print(k.pp_z)
    print(heat_map.cells[15][15])
    #print(np.sum(k.weights))

    k.calculate_prediction_point(3, 3)
    #print('Prediction Lag')
    #print(k.pp)
    k.calculate_sv_pp()
    #print('Prediction SV')
    #print(k.ppsv)
    k.calculate_weights()
    #print('Weights')
    #print(k.weights)
    k.calculate_z()
    #print('Z Matrix')
    #print(k.z_matrix)
    print('Estaimate for 3, 3')
    print(k.pp_z)
    print(heat_map.cells[3][3])
    #print(np.sum(k.weights))


    k.calculate_prediction_point(7,7)
    #print('Prediction Lag')
    #print(k.pp)
    k.calculate_sv_pp()
    #print('Prediction SV')
    #print(k.ppsv)
    k.calculate_weights()
    #print('Weights')
    #print(k.weights)
    k.calculate_z()
    #print('Z Matrix')
    #print(k.z_matrix)
    print('Estaimate for 7, 7')
    print(k.pp_z)
    print(heat_map.cells[7][7])
    #print(np.sum(k.weights))