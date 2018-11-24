from bomb_simulation.kriging import Kriging
from bomb_simulation.grid import Grid


class EstimateGenerator:
    def __init__(self, heat_map):
        self.kriging = Kriging(heat_map)
        self.prediction_points = []
        self.min = 5
        self.error_limit = 10
        self.valid = True

    def is_valid(self):
        return self.valid

    def update_heat_map(self, new_heat_map):
        self.kriging = Kriging(new_heat_map)
        self.prediction_points = []
        if self.kriging.setup():
            self.valid = True
        else:
            self.valid = False

    def add_estimates(self, x, y):
        found = False
        for estimate in self.prediction_points:
            if x == estimate[0] and y == estimate[1]:
                found = True
        if not found:
            self.prediction_points.append([x, y])

    def get_points_to_predict(self):
        if self.valid:
            for x in range(self.kriging.heat_map.height):
                for y in range(self.kriging.heat_map.width):
                    if self.kriging.heat_map.cells[x][y] <= 0:
                        self.prediction_points.append([x, y])

    def estimate(self):
        if self.valid:
            for points in self.prediction_points:
                temp = self.kriging.get_estimate(points[0], points[1])
                points.extend(temp)

    def clean_up(self):
        if self.valid:
            temp = []
            for points in self.prediction_points:
                if len(points) == 4 and points[2] > self.min and points[3] < self.error_limit:
                    temp.append(points)
            self.prediction_points = temp

    def target_guess(self):
        if self.valid:
            guess = []
            max_estimate = 5
            for points in self.prediction_points:
                if points[2] > max_estimate or points[3] > 10:
                    max_estimate = points[2]
                    guess.append(points)
            return guess
        else:
            return []


if __name__ == "__main__":
    heat_map = Grid(32, 32)
    heat_map.init_bomb(8, 8)
    heat_map.cells[8][8] = 0
    e = EstimateGenerator(heat_map)
    e.update_heat_map(heat_map)
    e.get_points_to_predict()
    e.estimate()
    e.clean_up()
    print(e.target_guess())