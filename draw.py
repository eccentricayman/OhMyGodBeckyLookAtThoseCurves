from display import *
from matrix import *


def add_circle( points, cx, cy, cz, r, step ):
    ctr = step;
    oldX = None
    oldY = None
    oldZ = None
    while (ctr <= 1.0000000000000000000001):
        angl = 2 * math.pi * ctr;
        if (oldX == None or oldY == None or oldZ == None):
            oldX = r * math.cos(angl) + cx
            oldY = r * math.sin(angl)
            prevZ = cz
        else:
            newX = r * math.cos(angl) + cx
            newY = r * math.sin(angl) + cy
            newZ = cz
            add_edge(points, oldX, oldY, oldZ, newX, newY, newZ)
            oldX = newX
            oldY = newY
            oldZ = newZ
        ctr += step

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    if curve_type == "hermite":
        xc = generate_curve_coefs(x0, x1, x2, x3, "hermite")[0]
        yc = generate_curve_coefs(y0, y1, y2, y3, "hermite")[0]
    else:
        xc = generate_curve_coefs(x0, x1, x2, x3, "bezizer")[0]
        yc = generate_curve_coefs(y0, y1, y2, y3, "bezier")[0]

    add_point(points, xc[3], yc[3])
    ctr = first = 1 / step
    while ctr < 1:
        x = xc[0] * (ctr ** 3) + xc[1] * (ctr ** 2) + xc[2] * ctr + xc[3]
        y = yc[0] * (ctr ** 3) + yc[1] * (ctr ** 2) + yc[2] * ctr + yc[3]
        add_point(points, x, y)
        add_point(points, x, y)
        ctr += first
        sumx = 0
        for i in xc:
            sumx += i
        sumy = 0
        for i in yc:
            sumy += i
        add_point(points, xc, yc)
        
def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return
    
    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
