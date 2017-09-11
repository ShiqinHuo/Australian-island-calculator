import func_lib

path = ''         

def enter_file_path():
    global path
    path = input("Please type in the directory of your file (without quote marks): ")

    try:
        fileobj_test = open(path, 'r')
    except FileNotFoundError:
        print("File not found. Try again please.")
        enter_file_path()

    print('\nVerifying whether it is a YXZ file, it may take several minutes...')
    for line in fileobj_test:
        try:
            line_list = [float(line.split()[0]), float(line.split()[1]), float(line.split()[2])]
        except ValueError:
            print('This is not a YXZ file. Try again please.')
            enter_file_path()
            break
    print('\nVerification passed.')

    fileobj_test.close()

enter_file_path()

print('\n===========================================================')
print('Introduction to each function level:\n')
print('Level 1: Calculate the land area and its proportion of whole land area in given region that above a particular sea level height.\n')
print('Level 2: List the information of different sea levels according to the given step of the maximum elevation in the given region, and plot sea level increase against area above water.\n')
print('''Level 3: Do both function level 1 and 2 with both approxiation 1 and 2 (don't need to input spacings). Then compare all the results in a table, in which numbers of 'islands' are also included.''')
print('===========================================================\n')

level = 0
def choose_level():
    global level

    try:
        level = int(input('\nNow type in the level of function you need: '))
    except ValueError:
        print('That is not a valid number. Try again please.')
        choose_level()

    if level < 1 or level > 3:
        print('Input out of range. Try again please.')
        choose_level()

choose_level()

if level == 1:
    y = float(input('\nInput mean vertical spacing y(km): '))
    x = float(input('Input mean horizontal spacing x(km): '))
    h = float(input('Input the desired sea level height h(m): '))
    print('')
    func_lib.level1(path, y, x, h)
elif level == 2:
    y = float(input('\nInput mean vertical spacing y(km): '))
    x = float(input('Input mean horizontal spacing x(km): '))
    step = float(input('Input the desired step(1 must be divisible by step, e.g., 0.01): '))
    print('')
    func_lib.level2(path, y, x, step)
elif level == 3:
    print('\nFirstly, do function level1 with both 2 approximations.')
    h = float(input('Input the desired sea level height h(m): '))
    print('')
    func_lib.level3_1(path, h)

    print('\nThen, do function level2 with both 2 approximations.')
    step = float(input('Input the desired step(1 must be divisible by step, e.g., 0.01): '))
    print('')
    func_lib.level3_2(path, step)
else:
    print('\nLevel should be among 1, 2, 3.')
