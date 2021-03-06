from random import randrange, seed
from bomb_simulation.controller import RobotController
from bomb_simulation.grid import Grid
from bomb_simulation.robot import Robot
from statistics import mean, stdev

def main():
    seed()
    steps = []
    stepsSlow = []
    for i in range(1):
        width = randrange(33, 33+1)
        height = randrange(33, 33+1)
        bomb_x = randrange(0, width)
        bomb_y = randrange(0, height)
        robots = []
        grid = Grid(width, height)
        grid.init_bomb(bomb_x, bomb_y, 10)
        for i in range(0, 3):
            temp = Robot(i, grid, [0, int(i*height/3)], False)
            robots.append(temp)
        controller = RobotController(grid, robots, False, True)
        controller.print_grid = False
        temp = controller.go()
        steps.append(temp)


    x_bar = steps[0]
    # sigma = stdev(steps, x_bar)
    print('Phylogenetic Algorithm')
    print('----------------------')
    print('Mean Steps: ', x_bar)
    # print('Std Dev Steps: ', sigma)



if __name__ == "__main__":
    # execute only if run as a script
    main()


