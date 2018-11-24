from bomb_simulation.controller import RobotController
from bomb_simulation.robot import Robot
from bomb_simulation.grid import Grid
from random import randrange, seed
from statistics import mean, stdev


def single():
    choice = input('Brute Force (1) or Phylogenic(2): ')
    temp = int(choice)
    slow = False
    if temp == 1:
        slow = True
    choice = input('Enter the Grid Width : ')
    width = int(choice)
    choice = input('Grid Height : ')
    height = int(choice)
    choice = input('Enter the Bomb Location in X: ')
    bomb_x = int(choice)
    choice = input('in Y: ')
    bomb_y = int(choice)
    choice = input('Enter the number of robots: ')
    num_robots = int(choice)
    choice = input('Use Kriging to Guess 1 Yes 2 No: ')
    temp = int(choice)
    guess = True
    if temp == 2:
        guess = False
    robots = []

    grid = Grid(width, height)
    grid.init_bomb(bomb_x, bomb_y, 10)

    for i in range(0, num_robots):
        temp = Robot(i, grid, [0, int(i * height / num_robots)], slow)
        robots.append(temp)

    controller = RobotController(grid, robots, False, True, guess)
    controller.print_grid = False
    controller.go()


def single_with_graphics():
    choice = input('Brute Force (1) or Phylogenic(2): ')
    temp = int(choice)
    slow = False
    if temp == 1:
        slow = True
    choice = input('Enter the Grid Width : ')
    width = int(choice)
    choice = input('Grid Height : ')
    height = int(choice)
    choice = input('Enter the Bomb Location in X: ')
    bomb_x = int(choice)
    choice = input('in Y: ')
    bomb_y = int(choice)
    choice = input('Enter the number of robots: ')
    num_robots = int(choice)
    robots = []

    grid = Grid(width, height)
    grid.init_bomb(bomb_x, bomb_y, 10)

    for i in range(0, num_robots):
        temp = Robot(i, grid, [0, int(i * height / num_robots)], slow)
        robots.append(temp)

    controller = RobotController(grid, robots, True, True)
    controller.print_grid = False
    controller.go()

def mc():
    #Vary Grid Size?
    #Vary Bomb Location?
    #Number of Robots


    min_width = 0
    min_height = 0
    max_width = 0
    max_height = 0
    steps_bf = []
    steps_bf_k= []
    steps_ph = []
    steps_ph_k = []
    choice = input('Do you want to Vary Grid Size (Y/N): ')
    if choice == 'Y' or choice == 'y':
        choice = input('Minimum Grid Width : ')
        min_width = int(choice)
        choice = input('Maximum Grid Width : ')
        max_width = int(choice)
        choice = input('Minimum Grid Height : ')
        min_height = int(choice)
        choice = input('Maximum Grid Height : ')
        max_height = int(choice)
    else:
        choice = input('Grid Width : ')
        min_width = int(choice)
        max_width = min_width + 1
        choice = input('Grid Height : ')
        min_height = int(choice)
        max_height = min_height + 1

    vary_bomb = False
    bomb_x = 0
    bomb_y = 0
    choice = input('Do you want to Vary Bomb Location (Y/N): ')
    if choice == 'Y' or choice == 'y':
        vary_bomb = True
    else:
        vary_bomb = False
        choice = input('Enter the Bomb Location in X: ')
        bomb_x = int(choice)
        choice = input('in Y: ')
        bomb_y = int(choice)


    choice = input('Enter the number of robots: ')
    num_robots = int(choice)
    robots = []

    choice = input('Number of Iterations: ')
    iterations = int(choice)

    seed()
    for i in range(iterations):
        width = randrange(min_width, max_width)
        height = randrange(min_height, max_height)
        if vary_bomb:
            bomb_x = randrange(0, width)
            bomb_y = randrange(0, height)
        grid = Grid(width, height)
        grid.init_bomb(bomb_x, bomb_y, 10)

        robots_bf = []
        for i in range(0, num_robots):
            temp = Robot(i, grid, [0, int(i*height/num_robots)], True)
            robots_bf.append(temp)
        controller = RobotController(grid, robots_bf, False, False, False)
        temp = controller.go()
        steps_bf.append(temp)

        robots_bf_k = []
        for i in range(0, num_robots):
            temp = Robot(i, grid, [0, int(i * height / num_robots)], True)
            robots_bf_k.append(temp)
        controller = RobotController(grid, robots_bf_k, False, False, True)
        temp = controller.go()
        steps_bf_k.append(temp)

        robots_ph = []
        for i in range(0, num_robots):
            temp = Robot(i, grid, [0, int(i * height / num_robots)], False)
            robots_ph.append(temp)
        controller = RobotController(grid, robots_ph, False, False, False)
        temp = controller.go()
        steps_ph.append(temp)

        robots_ph_k = []
        for i in range(0, num_robots):
            temp = Robot(i, grid, [0, int(i * height / num_robots)], False)
            robots_ph_k.append(temp)
        controller = RobotController(grid, robots_ph_k, False, False, True)
        temp = controller.go()
        steps_ph_k.append(temp)

    x_bar_bf = mean(steps_bf)
    sigma_bf = stdev(steps_bf, x_bar_bf)
    print()
    print('Brute Force')
    print('----------------------')
    print('Mean Steps: ', x_bar_bf)
    print('Std Dev Steps: ', sigma_bf)
    
    x_bar_bf_k = mean(steps_bf_k)
    sigma_bf_k = stdev(steps_bf_k, x_bar_bf_k)
    print()
    print('Brute Force + Kriging')
    print('----------------------')
    print('Mean Steps: ', x_bar_bf_k)
    print('Std Dev Steps: ', sigma_bf_k)

    x_bar_ph = mean(steps_ph)
    sigma_ph = stdev(steps_ph, x_bar_ph)
    print()
    print('Phylogenetic')
    print('----------------------')
    print('Mean Steps: ', x_bar_ph)
    print('Std Dev Steps: ', sigma_ph)

    x_bar_ph_k = mean(steps_ph_k)
    sigma_ph_k = stdev(steps_ph_k, x_bar_ph_k)
    print()
    print('Phylogenetic + Kriging')
    print('----------------------')
    print('Mean Steps: ', x_bar_ph_k)
    print('Std Dev Steps: ', sigma_ph_k)


def main():
    ## Show menu ##
    print(30 * '-')
    print("   M A I N - M E N U")
    print(30 * '-')
    print("1. Single Run")
    print("2. Single Run with Graphics")
    print("3. Monte Carlo Run")
    print("4. Quit")
    print(30 * '-')
    choice = input('Enter your choice [1-3] : ')
    choice = int(choice)

    if choice == 1:
        single()
    elif choice == 2:
        single_with_graphics()
    elif choice == 3:
        mc()
    elif choice == 4:
        exit(0)
    else:  ## default ##
        print("Invalid number. Try again...")

if __name__ == "__main__":
    # execute only if run as a script
    main()