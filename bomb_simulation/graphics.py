import turtle as g

class Graphics:
    def __init__(self, grid, robots):
        self.grid = grid
        g = g()
        self.robots = robots
        self.scale_x = 800 / grid.width
        self.scale_y = 800 / grid.height
        self.robot_stamps = []
        for index in range(len(self.robots)):
            self.robot_stamps.append(None)

    def draw_grid(self):
        g.hideturtle()
        g.turtlesize(2, 2, 1)
        g.penup()
        g.setposition(-400, 400)
        g.pendown()
        g.forward(self.grid.width * int(self.scale_x))
        g.right(90)
        g.forward(self.grid.height * int(self.scale_y))
        g.right(90)
        g.forward(self.grid.width * int(self.scale_x))
        g.right(90)
        g.forward(self.grid.height * int(self.scale_y))
        g.right(90)

    def update_grid(self, new_grid):
        self.grid = new_grid
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if self.grid.cells[x][y] > 0 and self.grid.drawn[x][y] is False:
                    g.penup()
                    g.setposition(x * int(self.scale_x) - 400, -y * int(self.scale_y) + 400)
                    g.pendown()
                    if self.grid.cells[x][y] == 1:
                        g.dot(self.scale_x / 2, '#660099')
                    elif self.grid.cells[x][y] == 2:
                        g.dot(self.scale_x / 2, '#770088')
                    elif self.grid.cells[x][y] == 3:
                        g.dot(self.scale_x / 2, '#880077')
                    elif self.grid.cells[x][y] == 4:
                        g.dot(self.scale_x / 2, '#990066')
                    elif self.grid.cells[x][y] == 5:
                        g.dot(self.scale_x / 2, '#AA0055')
                    elif self.grid.cells[x][y] == 6:
                        g.dot(self.scale_x / 2, '#BB0044')
                    elif self.grid.cells[x][y] == 7:
                        g.dot(self.scale_x / 2, '#CC0033')
                    elif self.grid.cells[x][y] == 8:
                        g.dot(self.scale_x / 2, '#DD0022')
                    elif self.grid.cells[x][y] == 9:
                        g.dot(self.scale_x / 2, '#EE0011')
                    elif self.grid.cells[x][y] == 10:
                        g.dot(self.scale_x / 2, '#FF0000')
                    self.grid.drawn[x][y] = True
        for robot in self.robots:
            if self.robot_stamps[robot.id] is not None:
                clearstamp(self.robot_stamps[robot.id])
            penup()
            x = robot.current_location[0]
            y = robot.current_location[1]
            setposition(x * int(self.scale_x) - 400, -y * int(self.scale_y) + 400)
            pendown()
            color('green')
            self.robot_stamps[robot.id] = stamp()

