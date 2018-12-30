from statistics import stdev, mean, variance
from bomb_simulation.distance import euclidean_distance
from bomb_simulation.grid import Grid


class EmGrid(Grid):
    def __init__(self, width, height):
        super().__init__(width, height)

    def init_bomb(self, x, y, strength=10):
        self.bomb_location = [x, y]
        # Usess the Inverse Sq Law str = strength / distance^2
        current_strength = strength
        offset = 0
        while current_strength > 0.1:
            for x_offset in range(-offset, offset + 1):
                for y_offset in range(-offset, offset + 1):
                    if (self.bomb_location[0] + x_offset >= 0) and (
                            self.bomb_location[1] + y_offset >= 0) and (
                            self.bomb_location[0] + x_offset < self.width) and (
                            self.bomb_location[1] + y_offset < self.height):
                        if (self.cells[self.bomb_location[0] + x_offset][self.bomb_location[1] + y_offset]) \
                                < current_strength:
                            self.cells[self.bomb_location[0] + x_offset][
                                self.bomb_location[1] + y_offset] = current_strength
            offset = offset + 1
            current_strength = strength / pow(offset, 2)
            print(current_strength)

