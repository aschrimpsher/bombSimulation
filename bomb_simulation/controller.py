from bomb_simulation.grid import Grid
from bomb_simulation.robot import Robot


class RobotController:
    def __init__(self, id):
        self.id = id
        self.grid = Grid(9, 9)
        self.grid.init_bomb(4, 4, 10)
        self.robot = Robot(1, self.grid, [0, 0], [])
        self.robot2 = Robot(1, self.grid, [5, 5], [])
        self.heat_map = Grid(9, 9)

    def go(self):
        while not self.robot.done or not self.robot2.done:
            self.robot.go()
            self.robot2.go()
            x = self.robot.current_location[0]
            y = self.robot.current_location[1]
            self.heat_map.cells[x][y] = self.robot.measure()
            x = self.robot2.current_location[0]
            y = self.robot2.current_location[1]
            self.heat_map.cells[x][y] = self.robot2.measure()
            if self.robot.bomb_found is True:
                print('Robot 1 Found the Bomb, the City is Saved')
                self.robot2.done = True
            elif self.robot2.bomb_found is True:
                print('Robot 2 Found the Bomb, the City is Saved')
                self.robot.done = True
            else:
                print(self)

    def __str__(self):
        grid_string = 'Heat Map ' + '\n'
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if x == self.robot.current_location[0] and y == self.robot.current_location[1]:
                    grid_string += ' |' + 'R1' + '| '
                elif  x == self.robot2.current_location[0] and y == self.robot2.current_location[1]:
                    grid_string += ' |' + 'R2' + '| '
                elif self.heat_map.cells[x][y] > 0:
                    grid_string += ' |' + str("%2d" % self.heat_map.cells[x][y]) + '| '
                else:
                    grid_string += ' |' + '  ' + '| '
            grid_string += '\n'
        return grid_string

c = RobotController(1)
c.go()

