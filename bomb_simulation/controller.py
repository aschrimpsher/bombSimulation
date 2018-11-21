from bomb_simulation.grid import Grid
from bomb_simulation.kriging import Kriging
from turtle import *


class RobotController:
    def __init__(self, grid, robots, ui=True, asci=True):
        self.id = id
        self.grid = grid
        self.heat_map = Grid(grid.width, grid.height)
        self.heat_map1 = Grid(grid.width, grid.height)
        self.heat_map2 = Grid(grid.width, grid.height)
        self.robots = robots
        self.steps = 0
        self.scale_x = 800 / grid.width
        self.scale_y = 800 / grid.height
        self.ui = ui
        self.asci = asci
        self.robot_stamps = []
        self.done = False
        self.estimate = -1
        self.estimateX = -1
        self.estimateY = -1
        self.diff = 0
        for index in range(len(self.robots)):
            self.robot_stamps.append(None)

    def go(self):
        if self.asci is True:
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
                    if self.asci is True:
                        print('Robot 1 Found the Bomb, the City is Saved')
                    self.done = True
                elif robot.done is False:
                    all_robots_done = False
                if self.ui is True:
                        self.update_heat_map()
                if self.steps % 3 == 0:
                    robot.share(self.robots)
            self.steps += 1
            if self.steps % 5 == 0:
                if self.robots[0].max > 0 and self.robots[1].max > 0:
                    k = Kriging(self.heat_map)
                    k.setup()
                    tempX= int((self.robots[0].max_location[0] + self.robots[1].max_location[0]) / 2)
                    tempY = int((self.robots[0].max_location[1] + self.robots[1].max_location[1]) / 2)
                    if self.estimateX == -1:
                        self.estimateX = tempX
                        self.estimateY = tempY
                    tempEstimate1 = round(k.get_estimate(tempX, tempY), 1)
                    tempEstimatePrevious = round(k.get_estimate(self.estimateX, self.estimateY), 1)
                    if self.asci is True:
                        print('Previous ', tempEstimatePrevious, ' New ', tempEstimate1)
                    if tempEstimate1 > 11 or tempEstimate1 < 0:
                        self.estimate = tempEstimatePrevious
                    elif tempEstimatePrevious > 11 or tempEstimatePrevious < 0:
                        self.estimate = tempEstimate1
                        self.estimateX = tempX
                        self.estimateY = tempY
                    elif tempEstimate1 > tempEstimatePrevious:
                        self.estimate = tempEstimate1
                        self.estimateX = tempX
                        self.estimateY = tempY
                    else:
                        self.estimate = tempEstimatePrevious
                    self.diff = abs(self.estimate - self.grid.cells[self.estimateX][self.estimateY])
                if self.asci is True:
                    print(self)

            if all_robots_done is True:
                self.done = True
        if self.asci is True:
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
        if self.estimateX != -1:
            grid_string += 'Bomb Estimate ' + str("(%2d,%2d)" % (self.estimateX, self.estimateY))
            grid_string += str(" *(%d, %d)" % (self.grid.bomb_location[0], self.grid.bomb_location[1])) + '\n'
            grid_string += 'Estimate= ' + str("%.1f" % self.estimate) + str(" *%d" % self.grid.cells[self.estimateX][self.estimateY]) + '\n'
            grid_string += 'Error= ' + str("%.1f" % self.diff) + '\n'
        for robot in self.robots:
            grid_string += robot.__str__()
        for y in range(self.heat_map.height):
            for x in range(self.heat_map.width):
                is_robot = False
                for robot in self.robots:
                    if is_robot is False and x == robot.current_location[0] and y ==robot.current_location[1]:
                        is_robot = True
                        grid_string += '[' + 'R' + str(robot.id) + ']'

                if not is_robot and x is self.estimateX and y is self.estimateY:
                    grid_string += '[' + '**' + ']'
                elif not is_robot and self.heat_map.cells[x][y] > 0:
                    grid_string += '[' + str("%2d" % self.heat_map.cells[x][y]) + ']'
                elif not is_robot:
                    grid_string += '[' + '  ' + ']'
            grid_string += '\n'
        return grid_string


if __name__ == "__main__":
    c = RobotController(1, 16, 16, 0, 0)
    c.go()
    done()