
####################################################### Level 4
def level4plot(fname, h):
    '''Visualise the map with a sea level rising h(m)'''
    fileobj = open(fname, 'r')
    line_sample = fileobj.readline()
    y_start = float(line_sample.split()[0])
    y_last = float(line_sample.split()[0])
    fileobj.close()

    z_list = []
    y_count = 1    # first y is not counted in loop
    x_count = 0

    fileobj = open(fname, 'r')
    for line in fileobj:
        line_list = [float(line.split()[0]), float(line.split()[1]), float(line.split()[2])]
        z_list.append(line_list[2])
        if line_list[0] == y_start:
            x_count += 1
        if line_list[0] != y_last:
            y_count += 1
            y_last = line_list[0]
    fileobj.close()

    z_array = np.array(z_list).reshape(y_count, x_count)
    mpl.figure(1)
    mpl.imshow(z_array > h, interpolation = 'none')
    mpl.show()

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


def level4(fname, round(i * step_m, 2)):
    '''Return the number of "connected areas" with a sea level rise h(m)'''
    h=round(i * step_m, 2)  ## each step_m marked as h
    fileobj = open(fname, 'r')
    line_sample = fileobj.readline()
    y_start = float(line_sample.split()[0])
    y_last = float(line_sample.split()[0])
    fileobj.close()

    step

    z_list = []
    y_count = 1    # first y is not counted in loop
    x_count = 0

    fileobj = open(fname, 'r')
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
    compare_dict[round(i * step_m, 2)] += count ## 5th items
    return count
