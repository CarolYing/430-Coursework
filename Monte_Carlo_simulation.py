#YouTube: https://youtu.be/58L1M2aBbLk

#--------------------------prng class-----------------------
#open and read the file
with open('war-and-peace.txt') as infile:
        content = infile.read()

bound = len(content)  

#create a class
class WarAndPeacePseudoRandomNumberGenerator():
        '''This class generates pseudo random numbers'''

        def __init__(self, seed =1000, cursor = 0):
                ''''initializes seed and cursor''' 
                self.seed = seed
                self.cursor = cursor

        def random(self): #start =0
                '''this function returns a pseudo random number [0,1)'''
                # set up the step
                self.step = 100

                # get 64 letters(symbols) from the text in a list, each two adjacent are not the same 
                self.lst = []
                i = self.cursor  #0
                self.count = 0
                while self.count < 32:
                        try:
                                first = content[self.seed+self.step*i]
                        except: # if it runs to the end of the text, start off from the beginning
                                preIndex = (self.seed+self.step*(i-1)) 
                                diff = bound-preIndex 
                                first = content[self.step-diff]
                                self.seed = self.step-diff
                                i = 0
                        try:
                                second = content[self.seed+self.step*(i+1)]
                        except: # if it runs to the end of the text, start off from the beginning
                                preIndex = (self.seed+self.step*(i)) 
                                diff = bound-preIndex 
                                second = content[self.step-diff]
                                self.seed = self.step-diff
                                i = -1  # i should be the previous one
                                
                        if first != second:
                                  self.lst.append(first)
                                  self.lst.append(second)
                                  self.count += 1
                                  i += 2  
                        
                        else:
                                 i += 1

                #compare two letters(symbols) adjacent
                self.res = ''
                j = 0
                while j < 64:
                        if self.lst[j] > self.lst[j+1]:
                                self.res += '1'
                        else:
                                self.res += '0'
                        j+=2

                #calculate the number
                self.ans = 0
                for k in range(len(self.res)):
                        self.ans+= float(self.res[k])*((1/2)**(k+1))

                self.cursor = i # the new i is the next cursor, reset the cursor
                return self.ans #a number [0,1)


#---------------------------Point class----------------------------

class Point:
        '''This class generates a point'''

        def __init__(self, xcoord=0, ycoord=0):
                self.x = xcoord
                self.y = ycoord

        def __repr__(self):
                return f'Point ({self.x}, {self.y})'

        def getX(self):
                return self.x

        def getY(self):
                return self.y


#--------------------------Ellipse class---------------------------

class Ellipse():
        '''This class generates an ellipse'''

        def __init__(self, p1=Point(), p2=Point(), width=0):
                self.p1 = p1
                self.p2 = p2
                self.width = width

        def __repr__(self):
                return f'ellipse (focal point 1 is {self.p1}, focal point 2 is {self.p2}, width is {self.width})'

        def getP1(self):
                return self.p1

        def getP2(self):
                return self.p2

        def getWidth(self):
                return self.width



#-----------------------------some functions------------------------------
def borders(e1, e2):
        '''This function detects the four borders'''
        # get the points (four focal points, each point has a xcoord and ycoord)
        x = [e1.getP1().getX(), e1.getP2().getX(), e2.getP1().getX(), e2.getP2().getX()]
        y = [e1.getP1().getY(), e1.getP2().getY(), e2.getP1().getY(), e2.getP2().getY()]
        
        minX = min(x)
        maxX = max(x)
        minY = min(y)
        maxY = max(y)
        
        #get the bigger width
        width = [e1.getWidth(), e2.getWidth()]
        wid = max(width)

        #get the four borders
        left = minX - wid
        right = maxX + wid
        top = maxY + wid
        bottom = minY - wid

        return left, right, top, bottom
        

def getArea(left, right, top, bottom):
        '''calculates the area of the box'''
        area = abs(left - right) * abs(top - bottom)
        return area


prng = WarAndPeacePseudoRandomNumberGenerator()
def randomPoint(left, right, top, bottom):
        '''generates a random number in this box and returns the xcoord and ycoord'''
        #scale the range
        randomX = (right - left) * prng.random() + left
        randomY = (top - bottom) * prng.random() + bottom
        return randomX, randomY


import math
def hitEllipse(x, y, e):
        '''checks if this random point darts in the ellipes or not'''
        focalP1_x = e.getP1().getX()
        focalP1_y = e.getP1().getY()
        focalP2_x = e.getP2().getX()
        focalP2_y = e.getP2().getY()

        a = math.sqrt((focalP1_x - x)**2 + (focalP1_y - y)**2)
        b = math.sqrt((focalP2_x - x)**2 + (focalP2_y - y)**2)
        w = e.getWidth()

        if a+b<=w:
                return True
        else:
                return False
                
        
#--------------------------------overlap Ellipses---------------------------------
class computeOverlapOfEllipses():
        '''return the area of two ellipses overlap'''

        def __init__(self, e1, e2):
                '''takes two ellipses'''
                self.e1 = e1
                self.e2 = e2
                

        def overlap(self):
                '''This function returns the overlap area of two ellipses'''
                left, right, top, bottom = borders(self.e1, self.e2)
                area = getArea(left, right, top, bottom)
                ans = 0
                for i in range(20000):
                        x, y = randomPoint(left, right, top, bottom)
                        
                        if hitEllipse(x, y, self.e1) and hitEllipse(x, y, self.e2):
                                ans += 1
                        else:
                                pass
                

                res = (ans / 20000)*area
                print (f'The overlap area is {res}.')



#-------------------------Test-------------------------
if __name__ == '__main__':
        print ('start')
        p1 = Point(1, 1)
        p2 = Point(3, 3)
        p3 = Point(-1, 1)
        p4 = Point(3, 1)
        e1 = Ellipse(p1, p2, 5)
        e2 = Ellipse(p3, p4, 6)
        overlapArea = computeOverlapOfEllipses(e1, e2)
        overlapArea.overlap()
        
        
