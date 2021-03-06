from bomb_simulation.grid import Grid
from bomb_simulation.estimate_generator import EstimateGenerator
from bomb_simulation.graphics import Graphics
from bomb_simulation.distance import euclidean_distance


class RobotController:
    def __init__(self, grid, robots, ui=True, asci=True, guess=True):
        self.id = id
        self.grid = grid
        self.MAX_STEPS = grid.width * grid.height
        self.heat_map = Grid(grid.width, grid.height)
        self.estimate_generator = EstimateGenerator(self.heat_map, self.grid.bomb_location)
        self.robots = robots
        self.steps = 0
        self.interval_steps = 0
        self.ui = ui
        self.ascii = asci
        self.done = False
        self.estimates = []
        self.diff = 0
        self.print_grid = False
        self.print_all_estimates = False
        self.guess = guess
        self.best_z = []
        self.last_z = []
        # self.interval = max([int((grid.width * grid.height) / 250), 3])
        self.interval = 3
        if self.ui:
            self.graphics = Graphics(self.heat_map, self.robots)

    def move_robots(self):
        closestRobot = -1
        if self.estimate_generator.found_bomb():
            print(self.estimate_generator.found_bomb(),
                  self.estimate_generator.best_z)
            distance = []
            for robot in self.robots:
                temp = euclidean_distance(robot.current_location[0],
                                          robot.current_location[1],
                                          self.estimate_generator.best_z[0],
                                          self.estimate_generator.best_z[1])
                distance.append(temp)
            closestRobot = distance.index(min(distance))
        all_robots_done = True
        for robot in self.robots:
            x = robot.current_location[0]
            y = robot.current_location[1]
            self.heat_map.cells[x][y] = robot.measure()
            if self.estimate_generator.found_bomb():
                if closestRobot == robot.id:
                    robot.manual_drive(self.estimate_generator.best_z[0], self.estimate_generator.best_z[1])
            robot.go()
            if robot.bomb_found is True:
                if self.ascii is True:
                    print('Robot', robot.id, 'Found the Bomb, the City is Saved')
                self.done = True
            elif robot.done is False:
                all_robots_done = False
            if self.steps % 3 == 0:
                robot.share(self.robots)
        return all_robots_done

    def go(self):
        if self.ascii and self.print_grid is True:
            print(self.grid)
        if self.ui is True:
            self.graphics.draw_grid()
        while not self.done and self.steps < self.MAX_STEPS:
            all_robots_done = self.move_robots()
            self.steps += 1
            self.interval_steps += 1
            if self.interval_steps % self.interval == 0:
                if self.guess and not self.done:
                    if self.ascii is True:
                        print('Updating Estimate', self.interval_steps,
                              self.interval)
                    self.estimate_generator.estimate(self.heat_map, self.robots, self.steps)
                    if self.estimate_generator.is_valid() and \
                            self.estimate_generator.do_prediction_grid and \
                            len(self.estimate_generator.prediction_grid) > 0:
                        self.interval = 3
                        self.interval_steps = 0
                if self.ascii is True:
                    print(self)
            if self.ui is True:
                self.graphics.update_grid(self.heat_map)
            if all_robots_done is True:
                self.done = True
        if self.ascii is True:
            print(self)
        return [self.steps,
                self.done,
                self.estimate_generator.best_z,
                self.estimate_generator.last_z]

    def __str__(self):
        grid_string = 'Heat Map: ' + str(self.steps) + ' steps\n'
        if self.guess:
            grid_string += self.estimate_generator.__str__()
        for robot in self.robots:
            grid_string += robot.__str__()
        if self.print_grid:
            for y in range(self.heat_map.height):
                for x in range(self.heat_map.width):
                    is_robot = False
                    for robot in self.robots:
                        if is_robot is False and x == robot.current_location[0] and y ==robot.current_location[1]:
                            is_robot = True
                            grid_string += '[' + 'R' + str(robot.id) + ']'
                    if not is_robot and self.heat_map.cells[x][y] > 0:
                        grid_string += '[' + str("%2d" % self.heat_map.cells[x][y]) + ']'
                    elif not is_robot:
                        grid_string += '[' + '  ' + ']'
                grid_string += '\n'
        return grid_string
