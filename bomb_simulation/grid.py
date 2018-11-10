class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bomb_location = None
        self.cells = [[0 for i in range(self.height)] for j in range(self.width)]

    def init_bomb(self, x, y, strength):
        self.bomb_location = [x, y]
        current_strength = strength
        offset = 0
        while current_strength > 0:
            for x_offset in range(-offset, offset + 1):
                for y_offset in range(-offset, offset + 1):
                    if (self.bomb_location[0] + x_offset >= 0) and (self.bomb_location[1] + y_offset >= 0) and (
                            self.bomb_location[0] + x_offset < self.width) and (
                            self.bomb_location[1] + y_offset < self.height):
                        if (self.cells[self.bomb_location[0] + x_offset][self.bomb_location[1] + y_offset]) < current_strength:
                            self.cells[self.bomb_location[0] + x_offset][
                                self.bomb_location[1] + y_offset] = current_strength
                                # print('Setting ' + str(self.bomb_location[0] + x_offset) + ', ' +  str(self.bomb_location[1]+y_offset) +')' + 'to ' + str(current_strength))
            offset = offset + 1
            current_strength = current_strength - 1

    def __str__(self):
        grid_string = 'Grid\n'
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[x][y]>  0:
                    grid_string += ' |' + str("%2d" % self.cells[x][y]) + '| '
                else:
                    grid_string += ' |' + '  ' + '| '
            grid_string += '\n'
        return grid_string
