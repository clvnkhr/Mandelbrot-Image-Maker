from PIL import Image
import math as m #just for log. hm lol

maxIter = 20
maxDist = 2 #maximum distance z_n can get from 0
gridWidth = 500 #number of pixels per row (before h2w stretching)
gridHeight = 500 #number of rows of pixels
reRange = 3.0   
imRange = 3.0
startPt = -2 + 1.5j

h2w = 1 #height:width ratio, only useful in poorMansPrint as chars are not square
#for poormansPrint, good results come with h2w = 2 and ~120x120 size.

#the Mandelbrot set is the set of c such that z_1 := 0 and z_(n+1) = z_n^2 + c
def insideMandel(c):
    counter,z = 0,c
    while (abs(z) < maxDist) and (counter < maxIter):
        z = z*z + c
        counter = counter + 1
    #the following is a naive counter, below is a smooth renormalised version obtained via renormalisation
    #for info see http://linas.org/art-gallery/escape/math.html
    #return counter #if counter == maxIter, then c is 'inside'; else counter can be used to color the pixel based on iteration distance

    if counter == maxIter:
        return maxIter
    else:
        return counter + 1 - m.log( m.log(abs(z)) ) / m.log(2)

def mandelGrid():

    #get grid of counters (list of rows)
    return [[ insideMandel(startPt + i*reRange/(int(h2w*gridWidth))
        - ii*1j*imRange/gridHeight) for i in range(int(h2w*gridWidth))] 
        for ii in range(gridHeight)]

def mandelValue(c,n = maxIter): #to make pictures like http://commons.wikimedia.org/wiki/File:Mandelbrot_Creation_Animation_(800x600).gif
    z = c
    for _ in range(n):
        z = z*z + c
    return z

def mandelValueGrid():
    return [[abs(mandelValue(startPt + i*reRange/(int(h2w*gridWidth))
        - ii*1j*imRange/gridHeight)) for i in range(int(h2w*gridWidth))] 
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
    print(screen) #usage: poorMansPrint(mandelGrid())

def colourPath(point, n=0, b=255.0): #want a path that starts at (255,255,255) and ends at (0,0,0)
    if 0 == n:
        #nice sunny colours
        x = point/maxIter
        scale = 200
        if x < scale/(5*maxIter):
            t = 5*x*maxIter/scale
            return (int(b*(1-(2*t**10 + t)/3)) , int(b*(1-t)) , 0 )
        else:
            return colourPath(point-scale/5,0,b/1.2)
    elif 1 == n:
        #attempt a blue/white glow
        x = 180*point/maxIter
        return (int(20*abs((1-x)*m.sin(2*m.pi*x**2))) + int(50*abs(x*m.sin(2*m.pi*(x**2 + x)))), int(100*abs(x**2*(1-x)*m.sin(2*m.pi*x**2))), int(255*abs(x*m.sin(2*m.pi*(x**2 + x)))))
            
def showImage(grid,colourChoice = 0):
    img = Image.new( 'RGB', (gridWidth,gridHeight), "black") # create a new black image
    pixels = img.load() # create the pixel map

    for i in range(img.size[0]):    # for every pixel:
        for ii in range(img.size[1]):
            pixels[i,ii] = colourPath(grid[ii][i],colourChoice)# set the colour accordingly

    img.show()
    img.save('mandelbrot.png', 'PNG')

def showColourPalette(colourChoice = 0): #just for debugging the colors
    img = Image.new( 'RGB', (255,100), "black") # create a new black image
    pixels = img.load() # create the pixel map

    for t in range(img.size[0]):
        for _ in range(img.size[1]):
            pixels[t,_] = colourPath(t,colourChoice)# set the colour accordingly

    img.show()

showImage(mandelValueGrid(),1)
showColourPalette(1)