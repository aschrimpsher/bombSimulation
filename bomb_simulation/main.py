from bomb_simulation.controller import RobotController
from bomb_simulation.robot import Robot
from bomb_simulation.grid import Grid

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
        temp = Robot(i, grid, [0, int(i * height / num_robots)], False)
        robots.append(temp)

    controller = RobotController(grid, robots, False, False)
    controller.print_grid = False
    controller.go()

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