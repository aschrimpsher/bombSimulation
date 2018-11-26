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
        width = randrange(16, 25)
        height = randrange(16, 25)
        bomb_x = randrange(0, width)
        bomb_y = randrange(0, height)
        robots = []
        grid = Grid(width, height)
        grid.init_bomb(bomb_x, bomb_y, 10)
        for i in range(0, 2):
            temp = Robot(i, grid, [0, int(i*height/2)], False)
            robots.append(temp)
        controller = RobotController(grid, robots, True, True)
        temp = controller.go()
        steps.append(temp)

        robotsSlow = []
        gridSlow = Grid(width, height)
        gridSlow .init_bomb(bomb_x, bomb_y, 10)
        for j in range(0, 2):
            temp = Robot(j, grid, [0, int(j * height / 2)], True)
            robotsSlow .append(temp)
        controllerSlow  = RobotController(gridSlow, robotsSlow, True, True)
        tempSlow  = controllerSlow .go()
        stepsSlow.append(tempSlow )

    x_bar = steps[0]
    # sigma = stdev(steps, x_bar)
    print('Phylogenetic Algorithm')
    print('----------------------')
    print('Mean Steps: ', x_bar)
    # print('Std Dev Steps: ', sigma)

    x_barSlow = stepsSlow[0]
    # sigmaSlow = stdev(stepsSlow, x_barSlow)
    print()
    print('Brute Force')
    print('----------------------')
    print('Mean Steps: ', x_barSlow)
    # print('Std Dev Steps: ', sigmaSlow)

    print(x_barSlow /x_bar, 'Increase')

if __name__ == "__main__":
    # execute only if run as a script
    main()


