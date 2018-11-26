from bomb_simulation.controller import RobotController
from bomb_simulation.robot import Robot
from bomb_simulation.grid import Grid
from random import randrange, seed
from statistics import mean, stdev
import csv

def single():
    """
    Single runs a single run with no graphics.
    You can configure each parameter with the menu system
    :return: None
    """
    choice = input('Brute Force (1) or Phylogenetic(2): ')
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
    choice = input('Print Grid 1 Yes 2 No: ')
    temp = int(choice)
    print_grid = False
    if temp == 1:
        print_grid = True
    robots = []

    grid = Grid(width, height)
    grid.init_bomb(bomb_x, bomb_y, 10)

    for i in range(0, num_robots):
        starting_x = 0
        direction = 1
        if i % 2 == 1:
            starting_x = width-1
            direction = -1
        temp = Robot(i, grid, [starting_x, int(i * height / num_robots)], slow)
        temp.row_direction = direction
        temp.x_direction = direction
        robots.append(temp)

    controller = RobotController(grid, robots, False, True, guess)
    controller.print_grid = print_grid
    controller.go()


def single_with_graphics():
    """
    Runs a single run with graphics.
    You can configure each parameter with the menu system
    :return: None
    """
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
        starting_x = 0
        direction = 1
        if i % 2 == 1:
            starting_x = width - 1
            direction = -1
        temp = Robot(i, grid, [starting_x, int(i * height / num_robots)], slow)
        temp.row_direction = direction
        temp.x_direction = direction
        robots.append(temp)

    controller = RobotController(grid, robots, True, True)
    controller.print_grid = False
    controller.go()

def mc():
    """
    Runs a number of iterations of each of the 4 algorithm
    combinations. No graphics and no output.
    You can configure each parameter with the menu system
    :return: Writes out a CSV File of results for each run
    """
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

    choice = input('File To Save Results (default is results.csv): ')
    filename = choice
    if filename == '':
        filename = 'results.csv'

    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        header = ['Algorithm', 'Kriging', 'Grid Width', 'Grid Height',
                  'Bomb X Location', 'Bomb Y Location', 'Number of Robots',
                  'Steps', 'Best Bomb Guess X', 'Best Bomb Guess Y', 'Guess at Step',
                  'Last Bomb Guess X', 'Last Bomb Guess Y',]
        csvwriter.writerow(header)
        seed()
        for iteration in range(iterations):
            width = randrange(min_width, max_width)
            height = randrange(min_height, max_height)
            if vary_bomb:
                bomb_x = randrange(0, width)
                bomb_y = randrange(0, height)
            grid = Grid(width, height)
            grid.init_bomb(bomb_x, bomb_y, 10)

            robots_bf = []
            for i in range(0, num_robots):
                starting_x = 0
                direction = 1
                if i % 2 == 1:
                    starting_x = width - 1
                    direction = -1
                temp = Robot(i, grid, [starting_x, int(i * height / num_robots)], True)
                temp.row_direction = direction
                temp.x_direction = direction
                robots_bf.append(temp)
            controller = RobotController(grid, robots_bf, False, False, False)
            temp = controller.go()
            steps_bf.append(temp[0])
            print('BF Iteration', iteration)
            list = ['BF', 'No', width, height, bomb_x, bomb_y, num_robots, temp[0], '', '', '', '', '']
            csvwriter.writerow(list)

            robots_bf_k = []
            for i in range(0, num_robots):
                starting_x = 0
                direction = 1
                if i % 2 == 1:
                    starting_x = width - 1
                    direction = -1
                temp = Robot(i, grid, [starting_x, int(i * height / num_robots)], True)
                temp.row_direction = direction
                temp.x_direction = direction
                robots_bf_k.append(temp)
            controller = RobotController(grid, robots_bf_k, False, False, True)
            temp = controller.go()
            steps_bf_k.append(temp[0])
            print('BFK Iteration', iteration)
            list = []
            if len(temp[1]) > 0:
                list = ['BFK', 'Yes', width, height, bomb_x, bomb_y, num_robots, temp[0], temp[1][0], temp[1][1],
                        temp[1][4], temp[2][0], temp[2][1]]
            else:
                list = ['BFK', 'Yes', width, height, bomb_x, bomb_y, num_robots, temp[0], '', '', '', '', '']
            csvwriter.writerow(list)

            robots_ph = []
            for i in range(0, num_robots):
                starting_x = 0
                direction = 1
                if i % 2 == 1:
                    starting_x = width - 1
                    direction = -1
                temp = Robot(i, grid, [starting_x, int(i * height / num_robots)], False)
                temp.row_direction = direction
                temp.x_direction = direction
                robots_ph.append(temp)
            controller = RobotController(grid, robots_ph, False, False, False)
            temp = controller.go()
            steps_ph.append(temp[0])
            print('PH Iteration', iteration)
            list = ['PH', 'No', width, height, bomb_x, bomb_y, num_robots, temp[0], '', '', '', '', '']
            csvwriter.writerow(list)

            robots_ph_k = []
            for i in range(0, num_robots):
                starting_x = 0
                direction = 1
                if i % 2 == 1:
                    starting_x = width - 1
                    direction = -1
                temp = Robot(i, grid, [starting_x, int(i * height / num_robots)], False)
                temp.row_direction = direction
                temp.x_direction = direction
                robots_ph_k.append(temp)
            controller = RobotController(grid, robots_ph_k, False, False, True)
            temp = controller.go()
            steps_ph_k.append(temp[0])
            print('PHK Iteration', iteration)
            list = []
            if len(temp[1]) > 0:
                list = ['PHK', 'Yes', width, height, bomb_x, bomb_y, num_robots, temp[0], temp[1][0], temp[1][1],
                        temp[1][4], temp[2][0], temp[2][1]]
            else:
                list = ['PHK', 'Yes', width, height, bomb_x, bomb_y, num_robots, temp[0], '', '', '', '', '']
            csvwriter.writerow(list)

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


def mc_no_kriging():
    """
    Runs a number of iterations of each of the 4 algorithm
    combinations. No graphics and no output.
    You can configure each parameter with the menu system
    :return: Writes out a CSV File of results for each run
    """
    min_width = 0
    min_height = 0
    max_width = 0
    max_height = 0
    steps_bf = []
    steps_bf_k = []
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

    choice = input('File To Save Results (default is results.csv): ')
    filename = choice
    if filename == '':
        filename = 'results.csv'

    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        header = ['Algorithm', 'Kriging', 'Grid Width', 'Grid Height',
                  'Bomb X Location', 'Bomb Y Location', 'Number of Robots', 'Steps']
        csvwriter.writerow(header)
        seed()
        for iteration in range(iterations):
            width = randrange(min_width, max_width)
            height = randrange(min_height, max_height)
            # width = min_width + iteration
            # height = min_width + iteration
            if vary_bomb:
                bomb_x = randrange(0, width)
                bomb_y = randrange(0, height)
            grid = Grid(width, height)
            grid.init_bomb(bomb_x, bomb_y, 10)

            robots_bf = []
            for i in range(0, num_robots):
                temp = Robot(i, grid, [0, int(i * height / num_robots)], True)
                robots_bf.append(temp)
            controller = RobotController(grid, robots_bf, False, False, False)
            temp = controller.go()
            steps_bf.append(temp[0])
            print('BF Iteration', iteration)
            list = ['BF', 'No', width, height, bomb_x, bomb_y, num_robots, temp]
            csvwriter.writerow(list)

            robots_ph = []
            for i in range(0, num_robots):
                temp = Robot(i, grid, [0, int(i * height / num_robots)], False)
                robots_ph.append(temp)
            controller = RobotController(grid, robots_ph, False, False, False)
            temp = controller.go()
            steps_ph.append(temp[0])
            print('PH Iteration', iteration)
            list = ['PH', 'No', width, height, bomb_x, bomb_y, num_robots, temp]
            csvwriter.writerow(list)


    x_bar_bf = mean(steps_bf)
    sigma_bf = stdev(steps_bf, x_bar_bf)
    print()
    print('Brute Force')
    print('----------------------')
    print('Mean Steps: ', x_bar_bf)
    print('Std Dev Steps: ', sigma_bf)

    x_bar_ph = mean(steps_ph)
    sigma_ph = stdev(steps_ph, x_bar_ph)
    print()
    print('Phylogenetic')
    print('----------------------')
    print('Mean Steps: ', x_bar_ph)
    print('Std Dev Steps: ', sigma_ph)


def main():
    """
    Main runs a menu system for the Bomb Simulator.
    It can be run in a single session, a single session
    with graphics or a monte carlo session
    :return: None
    """
    print(30 * '-')
    print("   M A I N - M E N U")
    print(30 * '-')
    print("1. Single Run")
    print("2. Single Run with Graphics")
    print("3. Monte Carlo Run")
    print("4. Monte Carlo Run Without Kriging")
    print(30 * '-')
    choice = input('Enter your choice [1-4] : ')
    choice = int(choice)

    if choice == 1:
        single()
    elif choice == 2:
        single_with_graphics()
    elif choice == 3:
        mc()
    elif choice == 4:
        mc_no_kriging()
    else:  ## default ##
        print("Invalid number. Try again...")


if __name__ == "__main__":
    # execute only if run as a script
    main()