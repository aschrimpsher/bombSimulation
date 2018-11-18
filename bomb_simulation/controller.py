from bomb_simulation.grid import Grid
from bomb_simulation.robot import Robot
from random import randrange
from turtle import *


class RobotController:
    def __init__(self, id, gw, gh, r2x, r2y):
        self.id = id
        self.grid = Grid(gw, gh)
        self.r2x = r2x
        self.r2y = r2y
        self.grid.init_bomb(randrange(0, gw), randrange(0, gh), 10)
        self.heat_map = Grid(gw, gh)
        self.heat_map1 = Grid(gw, gh)
        self.heat_map2 = Grid(gw, gh)
        self.r1_boundary = self.grid.split_grid(0, 0, 16, 16)
        self.r2_boundary = self.grid.split_grid(self.r2x, self.r2y, (gw - self.r2x), (gh - self.r2y))
        self.robot = Robot(1, self.r1_boundary, [0, 0], self.heat_map1, [0,0], False)
        self.r2Star = 7
        self.robot2 = Robot(2, self.r2_boundary, [0, self.r2Star], self.heat_map2, [self.r2x, self.r2y+self.r2Star], False)
        self.steps = 0
        self.scale_x = 800 / gw
        self.scale_y = 800 / gh
        self.draw_heat_map()
        self.robot_stamps1 = None
        self.robot_stamps2 = None

    def go(self):
        print(self.grid)
        print(self.r1_boundary)
        print(self.r2_boundary)
        x = self.robot.current_location[0]
        y = self.robot.current_location[1]
        self.heat_map.cells[x][y] = self.robot.measure()
        x = self.robot2.current_location[0] + self.r2x
        y = self.robot2.current_location[1] + self.r2y
        self.heat_map.cells[x][y] = self.robot2.measure()
        while not self.robot.done or not self.robot2.done:
            self.robot.go()
            self.robot2.go()
            x = self.robot.current_location[0]
            y = self.robot.current_location[1]
            self.heat_map.cells[x][y] = self.robot.measure()
            x = self.robot2.current_location[0] + self.r2x
            y = self.robot2.current_location[1] + self.r2y
            self.heat_map.cells[x][y] = self.robot2.measure()
            if self.robot.bomb_found is True:
                print('Robot 1 Found the Bomb, the City is Saved')
                self.robot2.done = True
            elif self.robot2.bomb_found is True:
                print('Robot 2 Found the Bomb, the City is Saved')
                self.robot.done = True
            else:
                print(self)
                self.update_heat_map()
            if self.steps % 3 == 0:
                self.robot.share(self.robot2)
                self.robot2.share(self.robot)
            self.steps += 1
        print(self.robot.heat_map)
        print(self.robot2.heat_map)

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
                if self.robot.current_location[0] == x and self.robot.current_location[1] == y:
                    if self.robot_stamps1 is not None:
                        clearstamp(self.robot_stamps1)
                    penup()
                    setposition(x*int(self.scale_x) - 400, -y*int(self.scale_y)+400)
                    pendown()
                    color('green')
                    self.robot_stamps1 = stamp()
                if self.robot2.current_location[0] == x and self.robot2.current_location[1] == y:
                    if self.robot_stamps2 is not None:
                        clearstamp(self.robot_stamps2)
                    penup()
                    setposition(x*int(self.scale_x) - 400, -y*int(self.scale_y)+400)
                    pendown()
                    color('orange')
                    self.robot_stamps2 = stamp()


    def __str__(self):
        grid_string = 'Heat Map: ' + str(self.steps) + ' steps\n'
        grid_string += self.robot.__str__()
        grid_string += self.robot2.__str__()
        for y in range(self.heat_map.height):
            for x in range(self.heat_map.width):
                if x == self.robot.current_location[0] and y == self.robot.current_location[1]:
                    grid_string += ' |' + 'R1' + '| '
                elif x == self.robot2.current_location[0] + self.r2x and y == self.robot2.current_location[1]+self.r2y:
                    grid_string += ' |' + 'R2' + '| '
                elif self.heat_map.cells[x][y] > 0:
                    grid_string += ' |' + str("%2d" % self.heat_map.cells[x][y]) + '| '
                else:
                    grid_string += ' |' + '  ' + '| '
            grid_string += '\n'
        return grid_string



c = RobotController(1, 16, 16, 0, 0)
c.go()
done()