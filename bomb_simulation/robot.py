class Robot:
    def __init__(self, id, grid, starting_point, heat_map, true_starting_point, slow=False):
        self.id = id
        self.grid = grid
        self.true_starting_point = true_starting_point
        self.starting_point = starting_point
        self.current_location = starting_point
        self.heat_map = heat_map
        self.done = False
        self.bomb_found = False
        self.last_reading = 0
        self.fast = True
        self.max = 0
        self.max_location = [0,0]
        self.row_direction = 1
        self.x_direction = 1
        self.y_direction = 0
        if slow:
            self.fast = False

    def __str__(self):
        grid_string = 'Robot ' + str(self.id) + '\n'
        grid_string += '(' + str(self.current_location[0]) + ',' + str(self.current_location[1]) + ')\n'
        return grid_string

    def measure(self):
        return self.grid.cells[self.current_location[0]][self.current_location[1]]

    def share(self, robot):
        robot.add_max_to_heat_map(self.max, self.max_location)

    def add_max_to_heat_map(self, other_max, max_location):
        self.heat_map.cells[max_location[0]][max_location[1]] = other_max

    def go(self):
        if self.done is not True and self.bomb_found is not True:
            if self.measure() > self.max:
                self.max = self.measure()
                self.max_location[0] = self.current_location[0]
                self.max_location[1] = self.current_location[1]
                self.heat_map.cells[self.max_location[0]][self.max_location[1]] = self.max
                print(str(self.max_location[0]) + ' ' + str(self.max_location[1]))
                print(self.heat_map)

            if self.measure() == 10:
                self.bomb_found = True
                self.done = True
            else:
                if self.fast and self.measure() - self.max <= -2:
                    if self.current_location[1] - 2 < 0:
                        self.y_direction = 0
                        self.x_direction = 0
                    else:
                        self.y_direction = -2
                        self.x_direction = 0
                        self.row_direction = self.row_direction * 1
                        self.max = self.measure()
                elif self.fast and self.measure() < self.last_reading:
                        if self.current_location[1] + 1 == self.grid.height:
                            self.done = True
                            self.y_direction = 0
                            self.x_direction = 0
                        else:
                            self.y_direction = 1
                            self.x_direction = 0
                            self.row_direction = self.row_direction * -1
                else:
                    if (self.current_location[0] + self.x_direction) == self.grid.width:
                        self.y_direction = 1
                        self.x_direction = 0
                        self.row_direction = self.row_direction * -1
                    elif (self.current_location[0] + self.x_direction) == -1:
                        self.y_direction = 1
                        self.x_direction = 0
                        self.row_direction = self.row_direction * -1
                    else:
                        self.y_direction = 0
                        self.x_direction = self.row_direction
                self.last_reading = self.measure()
                self.current_location[0] += self.x_direction
                self.current_location[1] += self.y_direction

