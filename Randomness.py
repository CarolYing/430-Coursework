#YouTube: https://youtu.be/59Uq06_Tp0g


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


#-------------------------Test-------------------------
if __name__ == '__main__':
        lst = []
        prng = WarAndPeacePseudoRandomNumberGenerator(1000) #the seed can be changed
        for i in range(10000):
                r = prng.random()
                lst.append(r)

        minNum = min(lst)
        maxNum = max(lst)
        mean = sum(lst)/len(lst)
        print (f'The min is {minNum}')
        print ('----------------------------')
        print (f'The max is {maxNum}')
        print ('----------------------------')
        print (f'The mean is {mean}')
        print ('----------------------------')
                



