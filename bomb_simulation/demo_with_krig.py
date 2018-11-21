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
        width = 16
        height = 16
        bomb_x = 7
        bomb_y = 7
        robots = []
        grid = Grid(width, height)
        grid.init_bomb(bomb_x, bomb_y, 10)
        for i in range(0, 2):
            temp = Robot(i, grid, [0, int(i*height/2)], False)
            robots.append(temp)
        controller = RobotController(grid, robots, False, True)
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


