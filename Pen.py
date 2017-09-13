import pygame


class Pen:
    __vert_lines = []
    __horiz_lines = []
    __grid_points = None
    __max_x = None
    __max_y = None
    __screen = None
    __is_down = False
    __penx = None
    __peny = None
    __penr = 180
    __drawn_lines = []

    # Ex: To create a 5,5 grid with a starting point at 1,1 = Pen((5,5), (1,1))
    def __init__(self, grid_size: tuple, init_pen_pos):
        pygame.init()
        self.__screen = pygame.display.set_mode((640, 480))

        self.__max_x = grid_size[0]
        self.__max_y = grid_size[1]

        width, height = pygame.display.get_surface().get_size()
        vertPos = width / grid_size[0]
        horizPos = height / grid_size[1]
        for x in range(1, grid_size[0]):
            self.__vert_lines.append([(x*vertPos, 0), (x*vertPos, height)])
        for y in range(1, grid_size[1]):
            self.__horiz_lines.append([(0, y*horizPos), (width, y*horizPos)])

        def line_intersection(line1, line2):
            xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
            ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

            def det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            div = det(xdiff, ydiff)
            if div == 0:
                print("Lines don't intersect")

            d = (det(*line1), det(*line2))
            return int(det(d, xdiff) / div), int(det(d, ydiff) / div)

        self.__grid_points = [[0 for x in range(grid_size[0]-1)] for y in range(grid_size[1]-1)]
        x, y = (0, 0)
        for vline in self.__vert_lines:

            vlinex = vline[0]
            vliney = vline[1]
            for hline in self.__horiz_lines:
                hlinex = hline[0]
                hliney = hline[1]
                if x >= grid_size[0]-1:
                    x = 0
                if y >= grid_size[0]-1:
                    y = 0
                self.__grid_points[x][y] = line_intersection((vlinex, vliney), (hlinex, hliney))
                y += 1
            x += 1

        self.__penx = init_pen_pos[0]-1
        self.__peny = init_pen_pos[1]-1

    def __draw_pen(self):
        def get_matrix_pos():
            return self.__grid_points[self.__penx][self.__peny]

        def get_triangle_points():
            x, y = get_matrix_pos()
            front = (x, y)
            back1 = None
            back2 = None
            if self.__penr == 0 or self.__penr == 360:
                back1 = (x + 15, y - 10)
                back2 = (x + 15, y + 10)
            elif self.__penr == 90:
                back1 = (x - 10, y - 15)
                back2 = (x + 10, y - 15)
            elif self.__penr == 180:
                back1 = (x - 15, y - 10)
                back2 = (x - 15, y + 10)
            elif self.__penr == 270:
                back1 = (x - 10, y + 15)
                back2 = (x + 10, y + 15)

            return [front, back1, back2]
        pygame.draw.polygon(pygame.display.get_surface(), (255, 0, 0), get_triangle_points())

    def __draw_grid(self):
        for line in self.__vert_lines:
            pygame.draw.lines(pygame.display.get_surface(), (255, 255, 255), False, line, 2)
        for line in self.__horiz_lines:
            pygame.draw.lines(pygame.display.get_surface(), (255, 255, 255), False, line, 2)

    # Must be called last. Draws results from pen movements
    def draw(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()

            self.__screen.fill((0, 0, 0))
            self.__draw_grid()
            for line in self.__drawn_lines:
                line_x1, line_y1 = line[0][0], line[0][1]
                line_x2, line_y2 = line[1][0], line[1][1]
                pygame.draw.lines(pygame.display.get_surface(), (255, 0, 0), False,
                                  [self.__grid_points[line_x1][line_y1],
                                   self.__grid_points[line_x2][line_y2]], 4)
            self.__draw_pen()
            pygame.display.update()

    # Pick up pen
    def pu(self):
        self.__is_down = False

    # Place down pen
    def pd(self):
        self.__is_down = True

    # Move pen forward (v can be negative value)
    def fd(self, v):
        last_x, last_y = (self.__penx, self.__peny)

        temp_x, temp_y = (self.__penx, self.__peny)

        if self.__penr == 0 or self.__penr == 360:
            temp_x -= v
        elif self.__penr == 90:
            temp_y += v
        elif self.__penr == 180:
            temp_x += v
        elif self.__penr == 270:
            temp_y -= v

        if temp_x > self.__max_x or temp_x < 0 or temp_y > self.__max_y or temp_y < 0:
            print("Cursor went out of bounds")
        else:
            self.__penx = temp_x
            self.__peny = temp_y

            curr_x, curr_y = (self.__penx, self.__peny)
            if self.__is_down:
                self.__drawn_lines.append([(last_x, last_y), (curr_x, curr_y)])

    def __rot_check(self):
        if self.__penr < 0:
            self.__penr = 360 + self.__penr
        if self.__penr > 360:
            while self.__penr > 360:
                self.__penr = self.__penr - 360

    # Rotate pen clockwise
    def lt(self, r):
        if r % 90 == 0:
            self.__penr += r
            self.__rot_check()
        else:
            print("Rotation must be in multiples of 90")

    # Rotate pen counter-clockwise
    def rt(self, r):
        if r % 90 == 0:
            self.__penr += -r
            self.__rot_check()
        else:
            print("Rotation must be in multiples of 90")
