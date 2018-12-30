from bomb_simulation.kriging import Kriging
from bomb_simulation.distance import euclidean_distance


class EstimateGenerator:
    def __init__(self, heat_map, bomb_location):
        self.heat_map = heat_map
        self.bomb_location = bomb_location
        self.kriging = Kriging(heat_map)
        self.prediction_points = []
        self.do_prediction_grid = True
        self.min = 5
        self.error_limit = 50
        self.hard_error_limit = 10
        self.bomb_estimate_min = 8
        self.min_points = 20
        self.valid = True
        self.all = True
        self.prediction_grid = []
        self.best_z = []
        self.last_z = []
        self.print_all_estimates = False
        self.bomb_flag = False
        self.new_bomb_estimate = False

    def is_valid(self):
        return self.valid

    def found_bomb(self):
        if self.new_bomb_estimate and self.bomb_flag and len(self.best_z) >= 2:
            return True
        else:
            return False

    def update_heat_map(self, new_heat_map):
        self.heat_map = new_heat_map
        number_points = 0
        for y in range(self.heat_map.height):
            for x in range(self.heat_map.width):
                if self.heat_map.cells[x][y] >= 1:
                    number_points += 1
        if number_points < self.min_points:
            self.valid = False
        else:
            self.kriging = Kriging(new_heat_map)
            self.prediction_points = []
            if len(self.best_z) >= 2 and \
                    self.heat_map.cells[self.best_z[0]][self.best_z[1]] >= 1:
                self.best_z = []
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

    def get_points_to_predict(self, robots):
        if self.valid:
            if self.do_prediction_grid and len(self.prediction_grid) > 0:
                for y in range(self.prediction_grid[0][1], self.prediction_grid[1][1]+1):
                    for x in range(self.prediction_grid[0][0], self.prediction_grid[1][0]+1):
                        if self.kriging.heat_map.cells[x][y] <= 0:
                            self.add_estimates(x, y)
            elif self.all:
                for y in range(self.kriging.heat_map.height):
                    for x in range(self.kriging.heat_map.width):
                        if self.kriging.heat_map.cells[x][y] <= 0:
                            self.prediction_points.append([x, y])
            else:
                for robot1 in robots:
                    for robot2 in robots:
                        if robot1.id is not robot2.id and robot1.max > 0 and robot2.max > 0:
                            temp_x = int((robot1.max_location[0] + robot2.max_location[0]) / 2)
                            temp_y = int((robot1.max_location[1] + robot2.max_location[1]) / 2)
                            self.add_estimates(temp_x, temp_y)

    def estimate_points(self):
        if self.valid:
            for points in self.prediction_points:
                temp = self.kriging.get_estimate(points[0], points[1])
                points.extend(temp)

    def clean_up(self):
        if self.valid:
            self.bomb_flag = False
            self.new_bomb_estimate = False
            temp = []
            for points in self.prediction_points:
                if len(points) == 4 and points[2] > self.min and \
                        abs(points[3]) < self.error_limit and \
                        points[3] is not 0.0:
                    temp.append(points)
            self.prediction_points = temp

    def estimate(self, new_heat_map, robots, step):
        self.update_heat_map(new_heat_map)
        if self.is_valid():
            self.get_points_to_predict(robots)
            # print("Points to Estimate: ", len(self.prediction_points))
            self.estimate_points()
            self.clean_up()
            if len(self.prediction_points) > 0 and len(self.prediction_points[0]) == 4:
                min_x = self.heat_map.width
                min_y = self.heat_map.height
                max_x = 0
                max_y = 0
                max_z = 0
                min_err = 1000
                best_z = []
                best_e = []
                for estimate in self.prediction_points:
                    if estimate[0] < min_x:
                        min_x = estimate[0]
                    if estimate[0] > max_x:
                        max_x = estimate[0]
                    if estimate[1] < min_y:
                        min_y = estimate[1]
                    if estimate[1] > max_y:
                        max_y = estimate[1]
                    if estimate[2] > max_z and abs(estimate[3]) < self.hard_error_limit:
                        max_z = estimate[2]
                        best_z = estimate
                    if estimate[3] < min_err:
                        min_err = estimate[3]
                        best_e = estimate
                    if len(self.best_z) > 2 and \
                            estimate[0] == self.best_z[0] and \
                            estimate[1] == self.best_z[1]:
                        temp = self.best_z[4]
                        self.best_z = estimate
                        self.best_z.append(temp)
                if len(best_z) == 4 and best_z[2] >= self.min:
                    self.last_z = best_z
                    self.new_bomb_estimate = True
                    if len(self.best_z) == 0:
                        self.best_z = best_z
                        self.best_z.append(step)
                    elif best_z[0] == self.best_z[0] and \
                            best_z[1] == self.best_z[1]:
                        self.best_z = best_z
                        self.best_z.append(step)
                        self.new_bomb_estimate = False
                    elif best_z[2] >= self.best_z[2]:
                        self.best_z = best_z
                        self.best_z.append(step)
                    if self.best_z[2] > self.bomb_estimate_min and \
                            self.best_z[3] < self.hard_error_limit:
                        self.bomb_flag = True
                if max_x > 0 or max_y > 0:
                    self.prediction_grid = [[min_x, min_y], [max_x, max_y]]

    def __str__(self):
        estimate_string = ''
        if len(self.prediction_points) > 0 and len(self.prediction_points[0]) == 4:
            if self.print_all_estimates:
                for estimate in self.prediction_points:
                    estimate_string += 'Bomb Estimate ' + str("(%2d,%2d)" % (estimate[0], estimate[1]))
                    estimate_string += str(" *(%2d, %2d)" % (self.bomb_location[0], self.bomb_location[1])) + '\n'
                    estimate_string += 'Estimate= ' + str("%.1f %.1f" % (estimate[2], estimate[3]))
            if self.do_prediction_grid and len(self.prediction_grid) == 2:
                min_x = self.prediction_grid[0][0]
                min_y = self.prediction_grid[0][1]
                max_x = self.prediction_grid[1][0]
                max_y = self.prediction_grid[1][1]
                estimate_string += "Estimate Bomb is within "
                estimate_string += str("(%2d, %2d) and (%2d, %2d)" % (min_x, min_y, max_x, max_y)) + '\n'
            estimate_string += str("%2d estimates" % len(self.prediction_points)) + '\n'
            if len(self.best_z) == 5:
                estimate_string += 'Best Z '
                estimate_string += str("(%2d,%2d Z=%2.1f Error=%2.1f Step=%d)" % (self.best_z[0], self.best_z[1],
                                                                                  self.best_z[2], self.best_z[3],
                                                                                  self.best_z[4])) + '\n'
            if len(self.last_z) == 4:
                estimate_string += 'Latest Z '
                estimate_string += str("(%2d,%2d Z=%2.1f Error=%2.1f)" % (self.last_z[0], self.last_z[1],
                                                                          self.last_z[2], self.last_z[3])) + '\n'
        return estimate_string
