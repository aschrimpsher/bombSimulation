from bomb_simulation.grid import Grid
from bomb_simulation.estimate_generator import EstimateGenerator
from bomb_simulation.graphics import Graphics


class RobotController:
    def __init__(self, grid, robots, ui=True, asci=True, guess=True):
        self.id = id
        self.grid = grid
        self.heat_map = Grid(grid.width, grid.height)
        self.heat_map1 = Grid(grid.width, grid.height)
        self.heat_map2 = Grid(grid.width, grid.height)
        self.estimate_generator = EstimateGenerator(self.heat_map, self.grid.bomb_location)
        self.robots = robots
        self.steps = 0
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
        if self.ui:
            self.graphics = Graphics(self.heat_map, self.robots)

    def move_robots(self):
        all_robots_done = True
        for robot in self.robots:
            x = robot.current_location[0]
            y = robot.current_location[1]
            self.heat_map.cells[x][y] = robot.measure()
            if self.estimate_generator.found_bomb():
                robot.manual_drive(self.estimate_generator.last_z[0],
                                   self.estimate_generator.last_z[1])
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
        while not self.done:
            all_robots_done = self.move_robots()
            self.steps += 1
            if self.guess and self.steps % 3 == 0 and not self.done:
                self.estimate_generator.estimate(self.heat_map, self.robots, self.steps)
            if self.ascii is True:
                print(self)
            if self.ui is True:
                self.graphics.update_grid(self.heat_map)
            if all_robots_done is True:
                self.done = True
        if self.ascii is True:
            print(self)
        return [self.steps, self.estimate_generator.best_z, self.estimate_generator.last_z]

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
