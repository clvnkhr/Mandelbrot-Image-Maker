maxIter = 1000
maxDist = 1000 #maximum distance z_n can get from 0
gridWidth = 450 #number of pixels per row (before h2w stretching)
gridHeight = 450 #number of rows of pixels
reRange = 3.0  
imRange = 3.0
startPt = -2 -2j
 
h2w = 2.5 #height:width ratio, mainly useful in poorMansPrint as chars are not square
#for poormansPrint, good results come with h2w = 2 and ~120x120 size.
 
#the Mandelbrot set is the set of c such that z_1 := 0 and z_(n+1) = z_n^2 + c
def insideMandel(c):
    counter,z = 0,c
    while (abs(z) < maxDist) and (counter < maxIter):
        z = z*z + c
        counter = counter + 1
    return counter #if counter == maxIter, then c is 'inside'; else counter can be used to color the pixel based on iteration distance
 
def mandelGrid():
    #get grid of counters
    return [[ insideMandel(startPt + i*reRange/(int(h2w*gridWidth))
        + ii*1j*imRange/gridHeight) for i in range(int(h2w*gridWidth))]
        for ii in range(gridHeight)]
 
def poorMansPrint(grid):
    #for proper scaling, measure your char's h2w. My computer's is 2
    screen = ''
    for row in grid:
        for pt in row:
            if pt == maxIter:
                screen += 'X'
            elif maxIter/50<pt<maxIter:
                screen += 'x'
            elif maxIter/100<pt<maxIter/10:
                screen += '.'
            else:
                screen += ' '
        screen += '\n'
    print(screen)
   
poorMansPrint(mandelGrid())