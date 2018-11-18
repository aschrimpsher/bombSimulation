from bomb_simulation.grid import Grid
from bomb_simulation.robot import Robot
from random import randrange

class RobotController:
    def __init__(self, id, gw, gh, r2x, r2y):
        self.id = id
        self.grid = Grid(gw, gh)
        self.r2x = r2x
        self.r2y = r2y
        self.grid.init_bomb(9, 5, 10)
        # self.grid.init_bomb(randrange(0, gw), randrange(0, gh), 10)
        self.heat_map = Grid(gw, gh)
        self.heat_map1 = Grid(gw, gh)
        self.heat_map2 = Grid(gw, gh)
        self.r1_boundary = self.grid.split_grid(0, 0, 16, 16)
        self.r2_boundary = self.grid.split_grid(self.r2x, self.r2y, (gw - self.r2x), (gh - self.r2y))
        self.robot = Robot(1, self.r1_boundary, [0, 0], self.heat_map1, [0,0], False)
        self.r2Star = 7
        self.robot2 = Robot(2, self.r2_boundary, [0, self.r2Star], self.heat_map2, [self.r2x, self.r2y+self.r2Star], False)
        self.steps = 0

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
            if self.steps % 3 == 0:
                self.robot.share(self.robot2)
                self.robot2.share(self.robot)
            self.steps += 1
        print(self.robot.heat_map)
        print(self.robot2.heat_map)

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
