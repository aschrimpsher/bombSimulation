from bomb_simulation.grid import Grid
from bomb_simulation.estimate_generator import EstimateGenerator
from turtle import *


class RobotController:
    def __init__(self, grid, robots, ui=True, asci=True, guess=True):
        self.id = id
        self.grid = grid
        self.heat_map = Grid(grid.width, grid.height)
        self.heat_map1 = Grid(grid.width, grid.height)
        self.heat_map2 = Grid(grid.width, grid.height)
        self.estimate_generator = EstimateGenerator(self.heat_map)
        self.robots = robots
        self.steps = 0
        self.scale_x = 800 / grid.width
        self.scale_y = 800 / grid.height
        self.ui = ui
        self.ascii = asci
        self.robot_stamps = []
        self.done = False
        self.estimates = []
        self.diff = 0
        self.print_grid = False
        self.print_all_estimates = False
        self.guess = guess
        for index in range(len(self.robots)):
            self.robot_stamps.append(None)

    def go(self):
        if self.print_grid is True:
            print(self.grid)
        if self.ui is True:
            self.draw_heat_map()
        while not self.done:
            all_robots_done = True
            for robot in self.robots:
                x = robot.current_location[0]
                y = robot.current_location[1]
                self.heat_map.cells[x][y] = robot.measure()
                robot.go()
                if robot.bomb_found is True:
                    if self.ascii is True:
                        print('Robot 1 Found the Bomb, the City is Saved')
                    self.done = True
                elif robot.done is False:
                    all_robots_done = False
                if self.ui is True:
                        self.update_heat_map()
            self.steps += 1
            if self.steps % 1 == 0 and not self.done:
                robot.share(self.robots)
                self.estimate_generator.update_heat_map(self.heat_map)
                if self.estimate_generator.is_valid():
                    # for robot1 in self.robots:
                    #     for robot2 in self.robots:
                    #         if robot1.id is not robot2.id and robot1.max > 0 and robot2.max > 0:
                    #             temp_x = int((robot1.max_location[0] + robot2.max_location[0]) / 2)
                    #             temp_y = int((robot1.max_location[1] + robot2.max_location[1]) / 2)
                    #             self.estimate_generator.add_estimates(temp_x, temp_y)
                    self.estimate_generator.get_points_to_predict()
                    self.estimate_generator.estimate()
                    self.estimate_generator.clean_up()
                    self.estimates = self.estimate_generator.target_guess()
                else:
                    print('No Estimate')
            if all_robots_done is True:
                self.done = True
            if self.ascii is True:
                print(self)
        return self.steps

    def draw_heat_map(self):
        hideturtle()
        turtlesize(2, 2, 1)
        penup()
        setposition(-400, 400)
        pendown()
        forward(self.heat_map.width * int(self.scale_x))
        right(90)
        forward(self.heat_map.height * int(self.scale_y))
        right(90)
        forward(self.heat_map.width * int(self.scale_x))
        right(90)
        forward(self.heat_map.height * int(self.scale_y))
        right(90)


    def update_heat_map(self):
        for y in range(self.heat_map.height):
            for x in range(self.heat_map.width):
                if self.heat_map.cells[x][y] > 0 and self.heat_map.drawn[x][y] is False:
                    penup()
                    setposition(x*int(self.scale_x) - 400, -y*int(self.scale_y)+400)
                    pendown()
                    if self.heat_map.cells[x][y] == 1:
                        dot(self.scale_x/2, '#660099')
                    elif self.heat_map.cells[x][y] == 2:
                        dot(self.scale_x/2,'#770088')
                    elif self.heat_map.cells[x][y] == 3:
                        dot(self.scale_x/2,'#880077')
                    elif self.heat_map.cells[x][y] == 4:
                        dot(self.scale_x/2,'#990066')
                    elif self.heat_map.cells[x][y] == 5:
                        dot(self.scale_x/2,'#AA0055')
                    elif self.heat_map.cells[x][y] == 6:
                        dot(self.scale_x/2,'#BB0044')
                    elif self.heat_map.cells[x][y] == 7:
                        dot(self.scale_x/2,'#CC0033')
                    elif self.heat_map.cells[x][y] == 8:
                        dot(self.scale_x/2,'#DD0022')
                    elif self.heat_map.cells[x][y] == 9:
                        dot(self.scale_x/2,'#EE0011')
                    elif self.heat_map.cells[x][y] == 10:
                        dot(self.scale_x/2,'#FF0000')
                    self.heat_map.drawn[x][y] = True
        for robot in self.robots:
            if self.robot_stamps[robot.id] is not None:
                clearstamp(self.robot_stamps[robot.id])
            penup()
            x = robot.current_location[0]
            y = robot.current_location[1]
            setposition(x*int(self.scale_x) - 400, -y*int(self.scale_y)+400)
            pendown()
            color('green')
            self.robot_stamps[robot.id] = stamp()


    def __str__(self):
        grid_string = 'Heat Map: ' + str(self.steps) + ' steps\n'
        if len(self.estimates) > 0 and len(self.estimates[0]) == 4:
            if self.print_all_estimates:
                for estimate in self.estimates:
                    grid_string += 'Bomb Estimate ' + str("(%2d,%2d)" % (estimate[0], estimate[1]))
                    grid_string += str(" *(%d, %d)" % (self.grid.bomb_location[0], self.grid.bomb_location[1])) + '\n'
                    grid_string += 'Estimate= ' + str("%.1f %.1f" % (estimate[2], estimate[3])) + str(" *%d" % self.grid.cells[estimate[0]][estimate[1]]) + '\n'
                    grid_string += 'Error= ' + str("%.1f" % (estimate[2] - self.grid.cells[estimate[0]][estimate[1]])) + '\n'
            minx = self.grid.width
            miny = self.grid.height
            maxx = 0
            maxy = 0
            maxz = 0
            minerr = 1000
            bestZ = []
            bestE = []
            for estimate in self.estimates:
                if estimate[0] < minx:
                    minx = estimate[0]
                if estimate[0] > maxx:
                    maxx = estimate[0]
                if estimate[1] < miny:
                    miny = estimate[1]
                if estimate[1] > maxy:
                    maxy = estimate[1]
                if estimate[2] > maxz:
                    maxz = estimate[2]
                    bestZ = estimate
                if estimate[3] < minerr:
                    minerr = estimate[3]
                    bestE = estimate
            grid_string += "Estimate Bomb is within " + str("(%2d, %2d) and (%2d, %2d)" % (minx, miny, maxx, maxy)) + '\n'
            grid_string += str("%2d estimates" % len(self.estimates)) + '\n'
            grid_string += 'Best Z ' + str("(%2d,%2d Z=%2.1f Error=%2.1f)" % (bestZ[0], bestZ[1], bestZ[2], bestZ[3])) + '\n'
            grid_string += 'Least Error ' + str("(%2d,%2d Z=%2.1f Error=%2.1f)" % (bestE[0], bestE[1], bestE[2], bestE[3])) + '\n'
            if bestZ == bestE and bestZ[2] > 8 and self.guess:
                grid_string += str("Bomb is at (%2d %2d)" % (bestZ[0], bestZ[1])) + '\n'
                for robot in self.robots:
                    robot.manual_drive(bestZ[0], bestZ[1])
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


if __name__ == "__main__":
    c = RobotController(1, 16, 16, 0, 0)
    c.go()
    done()