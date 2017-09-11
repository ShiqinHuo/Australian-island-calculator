####################################################### Level 1
def level1(path, y, x, h):
    '''Calculate the land area and its proportion of whole land area in given
       region that above a particular sea level height.

       Parameters: file name,
                   mean vertical spacing (km),
                   mean horizontal spacing (km),
                   sea level height (m)'''
    fileobj = open(path, 'r')

    count_land = 0
    count_above_h = 0
    for line in fileobj:
        h_str = line.split()[2]
        h_float = float(h_str)

        if h_float > 0.0:
            count_land += 1

            if h_float >= h:
                count_above_h += 1

    fileobj.close()
    land_above = int(y * x * count_above_h)
    land_above_percentage = round(count_above_h / count_land, 4) * 100
    print(land_above, 'km^2,', round(land_above_percentage, 2), end = '')
    print('%', 'of current land above water')

# level1('sydney250m.txt', 0.278, 0.231, 2)

####################################################### Level 2
import matplotlib.pyplot as mpl
import numpy as np

compare_dict = {}

def level2(path, y, x, step):
    '''List the information of different sea levels according to the given
       step of the maximum elevation in the given region, and plot sea level
       increase against area above water. 1 must be divisible by step.

       Parameters: file path,
                   mean vertical spacing (km),
                   mean horizontal spacing (km),
                   step in percentage (< 1)'''
    fileobj = open(path, 'r')
    count_land = 0
    z_list = []
    for line in fileobj:     # first traversal, find the maximum sea level
        line_list = [float(line.split()[0]), float(line.split()[1]), float(line.split()[2])]
        if line_list[2] > 0.0:
            count_land += 1

        z_list.append(line_list[2])

    z_max = max(z_list)
    step_m = step * z_max
    fileobj.close()


    fileobj = open(path, 'r')
    group_dict = {}
    for i in range(round(1 / step)):
        group_dict[i] = 0

    global compare_dict
    compare_dict = {}  # initialising the global "compare_dict", i.e., remove data inherited from the last calling

    for line in fileobj:   # second traversal, do more interesting stuff...
        line_list = [float(line.split()[0]), float(line.split()[1]), float(line.split()[2])]
        if line_list[2] <= 0.0:         # in files like 'au10k.txt', there are some Z with minors value
            continue
        lower_bound = z_max
        while lower_bound - step_m > line_list[2]:
            lower_bound -= step_m
        lower_bound -= step_m
        try:##raise key error
            group_dict[round(lower_bound / step_m)] += 1
        except KeyError:
            raise_keyerror()

    y_plot = []
    print('Data of land area (no sea counted in) above or equal to a certain sea level:')
    for i in range(len(group_dict)):
        print('at sea level +', end = '')
        print(round(i * step_m, 2), end = '')
        output_count = 0
        for j in range(len(group_dict)):
            if j >= i:
                output_count += group_dict[j]

        output_percentage = output_count / count_land

        print(':', round(output_count * y * x, 2), 'km^2 (', end = '')
        print(round(output_percentage * 100, 2), end = '')
        print('%)')

        compare_dict[round(i * step_m, 2)] = [round(output_count * y * x, 2)]  # 1st item in the value list
        compare_dict[round(i * step_m, 2)] += [round(output_percentage * 100, 2)] # 2nd item

        y_plot.append(round(output_count * y * x, 2))

    print('at sea level +', end = '')
    print(round(z_max, 2), ': 0.0 km^2 (0.0%)')

    x_plot = list(np.linspace(0.0, 1.0, 1 / step) * z_max)

    mpl.figure(1)
    mpl.plot(x_plot, y_plot)
    mpl.title('Plot of sea level increase vs. area above water based on approximation 1')
    mpl.xlabel('sea level increase (m)')
    mpl.ylabel('area above water (km^2)')
    mpl.show()

    fileobj.close()

# level2('sydney250m.txt', 0.278, 0.231, 0.01)
# level2('au10k.txt', 11.1, 9.82, 0.01)

####################################################### Level 3
def compare_function(compare_dict, step_m, z_max):
    print('elevation         approximation 1               approximation 2     number_of_islands')
    print('-------------------------------------------------------------------------------------')
    for i in range(len(compare_dict)):
        str1 = (7 - len(str(round(i * step_m, 2)))) * ' '   # 5 strings: to align the columns
        str2 = (10 - len(str(compare_dict[round(i * step_m, 2)][0]))) * ' '
        str3 = (5 - len(str(compare_dict[round(i * step_m, 2)][1]))) * ' '
        str4 = (10 - len(str(compare_dict[round(i * step_m, 2)][2]))) * ' '
        str5 = (5 - len(str(compare_dict[round(i * step_m, 2)][3]))) * ' '
        # str6 = (3-len(str(compare_dict[round(i * step_m, 2)][4]))) * ' '
        print(round(i * step_m, 2), str1, '    ', end = '')
        print(compare_dict[round(i * step_m, 2)][0], end = '')
        print('km^2', str2, '(', end='')
        print(compare_dict[round(i * step_m, 2)][1], end = '')
        print('%)   ', str3, end='')
        print(compare_dict[round(i * step_m, 2)][2], end = '')
        print('km^2', str4,'(', end='')
        if i == 0:         # because of rounding mistake, sometimes there will be percentage slightly above 100.00%
            print('100.0', end = '')
        else:
            print(compare_dict[round(i * step_m, 2)][3], end = '')
        print('%)   ', str5, end='')
        print(compare_dict[round(i * step_m, 2)][4])
        # print('%)   ', str5, end='')


    str_last = (7 - len(str(round(z_max, 2)))) * ' '   # the last line, which is not in compare_dict
    print(round(z_max, 2), str_last, '    ', end = '')
    print('0.0km^2         (0.0%)      0.0km^2         (0.0%)      0')
    print('-------------------------------------------------------------------------------------')

import math

def approximation(path):
    '''Read a file path, return the mean vertical and horizontal spacing of approximation 1 and horizontal spacings of approximation 2.
Note that x_list is not rounded to ensure high accuracy.'''
    fileobj = open(path, 'r')

    y_count = 0
    x_count = 0

    line_sample = fileobj.readline()
    y_last = float(line_sample.split()[0])
    y_start = float(line_sample.split()[0])
    x_start = float(line_sample.split()[1])
    x_list = []

    fileobj.close()

    fileobj = open(path, 'r')
    for line in fileobj:
        line_list = [float(line.split()[0]), float(line.split()[1]), float(line.split()[2])]
        if line_list[0] == y_last:
            x_count += 1
            x_end = line_list[1]
        else:
            y_count += 1

            x_list.append(abs(40075 / 360 * math.cos(y_last * math.pi / 180) * (x_end - x_start) / x_count))
            x_count = 0
            x_start = line_list[1]

            y_last = line_list[0]

    x_list.append(abs(40075 / 360 * math.cos(y_last * math.pi / 180) * (x_end - x_start) / x_count))    # the last y is not included in the loop above, manually add it in

    y = round(40007 / 360 * abs(y_last - y_start) / y_count, 3)
    x = round(sum(x_list) / len(x_list), 3)

    fileobj.close()

    return y, x, x_list

def level3_1(path, h):
    '''Do function level 1 with both the two approximations'''
    y, x, x_list = approximation(path)

    print('=========Below is function level 1 with approximation 1=========')
    level1(path, y, x, h)

    print('\n=========Below is function level 1 with approximation 2=========')
    fileobj = open(path, 'r')

    line_sample = fileobj.readline()
    y_last = float(line_sample.split()[0])

    fileobj.close()

    fileobj = open(path, 'r')

    land_above_area = 0
    total_land_area = 0
    i = 0
    for line in fileobj:
        line_list = [float(line.split()[0]), float(line.split()[1]), float(line.split()[2])]
        if line_list[0] == y_last:
            if line_list[2] > 0.0:
                total_land_area += x_list[i] * y
                if line_list[2] >= h:
                    land_above_area += x_list[i] * y

        else:
            y_last = line_list[0]
            i += 1
            if line_list[2] > 0.0:
                total_land_area += x_list[i] * y
                if line_list[2] >= h:
                    land_above_area += x_list[i] * y

    fileobj.close()

    land_above_area_percentage = round(land_above_area / total_land_area, 4) * 100

    print(round(land_above_area), 'km^2,', land_above_area_percentage, end = '')
    print('%', 'of current land above water')

# level3_1('sydney250m.txt', 2)

def level3_2(path, step):
    '''Do function level 2 with both the two approximations.
Note that the first plot must be closed to continue programme running.'''
    y, x, x_list = approximation(path)
    print('Note: manually close the figure to continue programme running.\n')
    print('=========Below is function level 2 with approximation 1=========')
    level2(path, y, x, step)

    print('\n=========Below is function level 2 with approximation 2=========')
    fileobj = open(path, 'r')
    line_sample = fileobj.readline()
    y_first = float(line_sample.split()[0])
    y_last = float(line_sample.split()[0])
    fileobj.close()


    fileobj = open(path, 'r')
    z_list = []
    total_land_area = 0
    i = 0
    for line in fileobj:     # first traversal, find the maximum sea level (m) and calculate total land area (km^2)
        line_list = [float(line.split()[0]), float(line.split()[1]), float(line.split()[2])]
        if line_list[0] == y_last:
            if line_list[2] > 0.0:
                total_land_area += x_list[i] * y
        else:
            y_last = line_list[0]
            i += 1
            if line_list[2] > 0.0:
                total_land_area += x_list[i] * y

        z_list.append(line_list[2])
    z_max = max(z_list)
    step_m = step * z_max
    fileobj.close()


    fileobj = open(path, 'r')
    area_group_dict = {}
    for i in range(round(1 / step)):
        area_group_dict[i] = 0
    y_last = y_first  # y_last refers to the previous y value read, not the bottom value
    i = 0
    for line in fileobj:   # second traversal
        line_list = [float(line.split()[0]), float(line.split()[1]), float(line.split()[2])]
        if line_list[2] <= 0.0:
            continue
        lower_bound = z_max
        while lower_bound - step_m > line_list[2]:
            lower_bound -= step_m

        lower_bound -= step_m
        if line_list[0] == y_last:
            area_group_dict[round(lower_bound / step_m)] += x_list[i] * y
        else:
            y_last = line_list[0]
            i += 1
            area_group_dict[round(lower_bound / step_m)] += x_list[i] * y
    fileobj.close()

    global compare_dict
    y_plot = []
    print('Data of land area (no sea counted in) above or equal to a certain sea level:')
    for i in range(len(area_group_dict)):
        print('at sea level +', end = '')
        print(round(i * step_m, 2), end = '')
        output_area = 0
        for j in range(len(area_group_dict)):
            if j >= i:
                output_area += area_group_dict[j]
        output_percentage = output_area / total_land_area

        print(':', round(output_area, 2), 'km^2 (', end = '')
        if i == 0:       # because of rounding mistake, sometimes there will be percentage slightly above 100.00%
            print('100.00', end = '')
        else:
            print(round(output_percentage * 100, 2), end = '')
        print('%)')

        compare_dict[round(i * step_m, 2)] += [round(output_area, 2)]    # 3rd item
        compare_dict[round(i * step_m, 2)] += [round(output_percentage * 100, 2)]    # 4th item
        h=round(i * step_m, 2) #
        level4(path, h)      #
        y_plot.append(round(output_area, 2))

    print('at sea level +', end = '')
    print(round(z_max, 2), ': 0.0 km^2 (0.00%)')
    x_plot = list(np.linspace(0.0, 1.0, 1 / step) * z_max)
    mpl.figure(2)
    mpl.plot(x_plot, y_plot)
    mpl.title('Plot of sea level increase vs. area above water based on approximation 2')
    mpl.xlabel('sea level increase (m)')
    mpl.ylabel('area above water (km^2)')
    mpl.show()

    print('\n=================Compare the results and the chart is shown below:==================')
    compare_function(compare_dict, step_m, z_max)

# level3_2('au10k.txt', 0.01)

####################################################### Level 4
# def level4plot(path, h):
#     '''Visualise the map with a sea level rising h(m)'''
#     fileobj = open(path, 'r')
#     line_sample = fileobj.readline()
#     y_start = float(line_sample.split()[0])
#     y_last = float(line_sample.split()[0])
#     fileobj.close()

#     z_list = []
#     y_count = 1    # first y is not counted in loop
#     x_count = 0

#     fileobj = open(path, 'r')
#     for line in fileobj:
#         line_list = [float(line.split()[0]), float(line.split()[1]), float(line.split()[2])]
#         z_list.append(line_list[2])
#         if line_list[0] == y_start:
#             x_count += 1
#         if line_list[0] != y_last:
#             y_count += 1
#             y_last = line_list[0]
#     fileobj.close()

#     z_array = np.array(z_list).reshape(y_count, x_count)
#     mpl.figure(1)
#     mpl.imshow(z_array > h, interpolation = 'none')
#     mpl.show()

# level4plot('sydney250m.txt', 0)

class Point:
    '''Define a class Point to contains information in YXZ, together with a boolean attribute to show if it has been visited.'''

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.visited = False

point_array = None

def check_around(p, h):
    '''Return the points around point p that above h, by building a list which contains position information.

    position diagram:        0 1 2
                             3 p 4
                             5 6 7     '''
    valid_list = []

    global point_array
    if p.x == 0:
        if p.y == 0:
            if point_array[0][1].z > h and point_array[0][1].visited == False:
                valid_list.append(4)
            if point_array[1][0].z > h and point_array[1][0].visited == False:
                valid_list.append(6)
            if point_array[1][1].z > h and point_array[1][1].visited == False:
                valid_list.append(7)

        elif p.y == len(point_array) - 1:
            if point_array[p.y - 1][0].z > h and point_array[p.y - 1][0].visited == False:
                valid_list.append(1)
            if point_array[p.y - 1][1].z > h and point_array[p.y - 1][1].visited == False:
                valid_list.append(2)
            if point_array[p.y][1].z > h and point_array[p.y][1].visited == False:
                valid_list.append(4)

        else:
            if point_array[p.y - 1][0].z > h and point_array[p.y - 1][0].visited == False:
                valid_list.append(1)
            if point_array[p.y - 1][1].z > h and point_array[p.y - 1][1].visited == False:
                valid_list.append(2)
            if point_array[p.y][1].z > h and point_array[p.y][1].visited == False:
                valid_list.append(4)
            if point_array[p.y + 1][0].z > h and point_array[p.y + 1][0].visited == False:
                valid_list.append(6)
            if point_array[p.y + 1][1].z > h and point_array[p.y + 1][1].visited == False:
                valid_list.append(7)

    elif p.x == len(point_array[0]) - 1:
        if p.y == 0:
            if point_array[0][p.x - 1].z > h and point_array[0][p.x - 1].visited == False:
                valid_list.append(3)
            if point_array[1][p.x - 1].z > h and point_array[1][p.x - 1].visited == False:
                valid_list.append(5)
            if point_array[1][p.x].z > h and point_array[1][p.x].visited == False:
                valid_list.append(6)

        elif p.y == len(point_array) - 1:
            if point_array[p.y - 1][p.x - 1].z > h and point_array[p.y - 1][p.x - 1].visited == False:
                valid_list.append(0)
            if point_array[p.y - 1][p.x].z > h and point_array[p.y - 1][p.x].visited == False:
                valid_list.append(1)
            if point_array[p.y][p.x - 1].z > h and point_array[p.y][p.x - 1].visited == False:
                valid_list.append(3)

        else:
            if point_array[p.y - 1][p.x - 1].z > h and point_array[p.y - 1][p.x - 1].visited == False:
                valid_list.append(0)
            if point_array[p.y - 1][p.x].z > h and point_array[p.y - 1][p.x].visited == False:
                valid_list.append(1)
            if point_array[p.y][p.x - 1].z > h and point_array[p.y][p.x - 1].visited == False:
                valid_list.append(3)
            if point_array[p.y + 1][p.x - 1].z > h and point_array[p.y + 1][p.x - 1].visited == False:
                valid_list.append(5)
            if point_array[p.y + 1][p.x].z > h and point_array[p.y + 1][p.x].visited == False:
                valid_list.append(6)

    else:
        if p.y == 0:
            if point_array[0][p.x - 1].z > h and point_array[0][p.x - 1].visited == False:
                valid_list.append(3)
            if point_array[0][p.x + 1].z > h and point_array[0][p.x + 1].visited == False:
                valid_list.append(4)
            if point_array[1][p.x - 1].z > h and point_array[1][p.x - 1].visited == False:
                valid_list.append(5)
            if point_array[1][p.x].z > h and point_array[1][p.x].visited == False:
                valid_list.append(6)
            if point_array[1][p.x + 1].z > h and point_array[1][p.x + 1].visited == False:
                valid_list.append(7)

        elif p.y == len(point_array) - 1:
            if point_array[p.y - 1][p.x - 1].z > h and point_array[p.y - 1][p.x - 1].visited == False:
                valid_list.append(0)
            if point_array[p.y - 1][p.x].z > h and point_array[p.y - 1][p.x].visited == False:
                valid_list.append(1)
            if point_array[p.y - 1][p.x + 1].z > h and point_array[p.y - 1][p.x + 1].visited == False:
                valid_list.append(2)
            if point_array[p.y][p.x - 1].z > h and point_array[p.y][p.x - 1].visited == False:
                valid_list.append(3)
            if point_array[p.y][p.x + 1].z > h and point_array[p.y][p.x + 1].visited == False:
                valid_list.append(4)

        else:
            if point_array[p.y - 1][p.x - 1].z > h and point_array[p.y - 1][p.x - 1].visited == False:
                valid_list.append(0)
            if point_array[p.y - 1][p.x].z > h and point_array[p.y - 1][p.x].visited == False:
                valid_list.append(1)
            if point_array[p.y - 1][p.x + 1].z > h and point_array[p.y - 1][p.x + 1].visited == False:
                valid_list.append(2)
            if point_array[p.y][p.x - 1].z > h and point_array[p.y][p.x - 1].visited == False:
                valid_list.append(3)
            if point_array[p.y][p.x + 1].z > h and point_array[p.y][p.x + 1].visited == False:
                valid_list.append(4)
            if point_array[p.y + 1][p.x - 1].z > h and point_array[p.y + 1][p.x - 1].visited == False:
                valid_list.append(5)
            if point_array[p.y + 1][p.x].z > h and point_array[p.y + 1][p.x].visited == False:
                valid_list.append(6)
            if point_array[p.y + 1][p.x + 1].z > h and point_array[p.y + 1][p.x + 1].visited == False:
                valid_list.append(7)

    return valid_list

def get_around(p, h):
    '''Return a set of points whose z(m) is above given h(m) that around a certain point'''
    global point_array
    points = set()
    points.add(p)
    for direction in check_around(p, h):
        if direction == 0:
            points.add(point_array[p.y - 1][p.x - 1])
        elif direction == 1:
            points.add(point_array[p.y - 1][p.x])
        elif direction == 2:
            points.add(point_array[p.y - 1][p.x + 1])
        elif direction == 3:
            points.add(point_array[p.y][p.x - 1])
        elif direction == 4:
            points.add(point_array[p.y][p.x + 1])
        elif direction == 5:
            points.add(point_array[p.y + 1][p.x - 1])
        elif direction == 6:
            points.add(point_array[p.y + 1][p.x])
        elif direction == 7:
            points.add(point_array[p.y + 1][p.x + 1])
        else:
            pass

    return points

def mark_an_island(p, h):
    '''Taking in one point, and mark all points in the island as visited, with a certain sea level h(m).'''
    fringe = []
    visited_set = set()
    fringe.append(p)
    while fringe:
        x = fringe.pop()
        x.visited = True
        visited_set.add(x)
        for point_around in get_around(x, h):
            if point_around in visited_set:
                continue
            fringe.append(point_around)


def level4(path, h):
    '''Return the number of "connected areas" with a sea level rise h(m)'''
##    h=round(i * step_m, 2)  ## each step_m marked as h
    fileobj = open(path, 'r')
    line_sample = fileobj.readline()
    y_start = float(line_sample.split()[0])
    y_last = float(line_sample.split()[0])
    fileobj.close()

    z_list = []
    y_count = 1    # first y is not counted in loop
    x_count = 0

    fileobj = open(path, 'r')
    for line in fileobj:
        line_list = [float(line.split()[0]), float(line.split()[1]), float(line.split()[2])]
        z_list.append(line_list[2])
        if line_list[0] == y_start:
            x_count += 1
        if line_list[0] != y_last:
            y_count += 1
            y_last = line_list[0]
    fileobj.close()

    z_array = np.array(z_list).reshape(y_count, x_count) # transfer all z into a 2d array, from ← to →, then from ↑ to ↓
    # print(z_array[0][0])
    # print(z_array[0][1])  # the first two z in the file

    point_list = []
    for y in range(len(z_array)):
        for x in range(len(z_array[0])):
            point_list.append(Point(x, y, z_array[y][x]))  # obtain a 1d list of Point with correct x, y attributes and all visit == False

    global point_array
    point_array = np.array(point_list).reshape(y_count, x_count)

    count = 0
    for y in range(len(z_array)):
        for x in range(len(z_array[0])):
            if point_array[y][x].visited == False and point_array[y][x].z > h:
                mark_an_island(point_array[y][x], h)
                count += 1
    compare_dict[h] += [count] # 5th item
    return count
