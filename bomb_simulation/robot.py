

class Robot:
    def __init__(self, id, grid, starting_point, boundry):
        self.id = id
        self.grid = grid
        self.starting_point = starting_point
        self.current_location = starting_point
        self.boundry = boundry
        self.direction = 1
        self.done = False
        self.bomb_found = False
        self.last_reading = 0

    def __str__(self):
        grid_string = 'Robot ' + str(self.id) + '\n'
        grid_string += '(' + str(self.current_location[0]) + ',' + str(self.current_location[1]) + ')\n'
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if x == self.current_location[0] and y == self.current_location[1]:
                    grid_string += ' |' + 'RR' + '| '
                else:
                    grid_string += ' |' + str("%2d" % self.grid.cells[x][y]) + '| '
            grid_string += '\n'
        return grid_string

    def measure(self):
        return self.grid.cells[self.current_location[0]][self.current_location[1]]

    def go(self):
        if self.done is not True and self.bomb_found is not True:
            if self.measure() == 10:
                self.bomb_found = True
                self.done = True
            elif self.measure() < self.last_reading:
                print("Turning Around")
                self.last_reading = self.measure()
                self.current_location[1] += 1
                self.direction = -1 * self.direction
            else:
                if (self.current_location[0] + self.direction) == self.grid.width:
                    self.last_reading = self.measure()
                    self.current_location[1] += 1
                    self.direction = -1 * self.direction
                elif (self.current_location[0] + self.direction) == 0:
                    self.last_reading = self.measure()
                    self.current_location[1] += 1
                    self.direction = -1 * self.direction
                else:
                    self.last_reading = self.measure()
                    self.current_location[0] += self.direction

                if self.current_location[1] == self.grid.height:
                    self.current_location[1] = self.grid.height - 1
                    self.done = True

