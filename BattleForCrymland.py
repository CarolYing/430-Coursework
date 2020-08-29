#YouTube: https://youtu.be/oD9HHkczhFo

import random

#-----------------------------create classes-------------------------------------
class Thief:
        '''this is a thief'''
        def __init__(self,num, n_testimony):
                '''initilize some features of a thief'''
                self.thieves = []
                self.num = num #the number of thieves the thief can recruite
                self.wealth = 0
                self.jailed = False
                self.reporter = None
                self.weekearning = 0
                self.n_testimony = n_testimony

        def recruite_thieves(self):
                '''this function simulates the action of recruiting thieves'''
                for i in range(self.num):
                        t = Thief(self.num, self.n_testimony)
                        t.reporter = self
                        self.thieves.append(t) #append to list self.thieves

        def isarrest(self):
                '''this function simulates the action how a thief is arrested'''
                num = 0
                for t in self.thieves:
                        if t.jailed:
                                num+=1
                if num >= self.n_testimony:
                        self.jailed=True

                return self.jailed

        def assignvalue(self,v): # v: value of one heist
                '''this function simulates the action of assigning values''' #half keep, half up
                self.wealth += v/2
                v = v/2
                lieu = self.reporter
                while lieu.reporter != None:
                        lieu.wealth += v/2
                        v = v/2
                        lieu = lieu.reporter
                lieu.wealth += v
                lieu.weekearning += v

        def promoted_to_lieutenant(self):
                '''this function simulates the action of how a thief is promoted to a lieutenant.''' # when wealth >=1000000
                if self.wealth <= 1000000:
                        return False
                else:
                        self.recruite_thieves() #can recruite thieves
                        return True

        def intojail(self, summary): #summary is a dictionary tracking the number of total thieves, jailed thieves, and the amount of bribe money
                '''this function simulates the change of data after putting a thief into jail'''
                self.jailed=True
                #if someone is in jail, summary changed
                summary['total'] -= 1
                summary['jailed'] += 1
                lieu=self.reporter

                if lieu == None:
                        pass 
                else:
                        num = 0
                        for t in lieu.thieves:
                                if t.jailed:
                                        num += 1

                        if num >= self.n_testimony and not lieu.jailed:
                                lieu.intojail(summary)

class Bigg(Thief):
        '''this is Mr. Bigg'''
        #override
        def assignvalue(self,v): # v: value of one heist
                '''this function simulates the action of assigning values''' #all keep
                self.wealth += v/2

        def promoted_to_lieutenant(self):
                pass
        			
		
class Detective:
        '''this class is a detective'''
        def __init__(self,solve_init,solve_cap):
                '''initilize some features of a detective'''
                self.solve_cap = solve_cap 
                self.solve_ability = solve_init  
                self.isbribed = False
                self.discovered = -1 #set as -1
                self.seized = 0
                self.bribnum= 0 

        def bribe(self,discovered,bribe_amount):
                '''this function returns the result if the detective is bribed or not'''
                prob=random.random()
                self.bribnum+=1
                if bribe_amount<=10000 and prob<=0.05:
                        self.isbribed=True
                elif bribe_amount<=100000 and prob<=0.1:
                        self.isbribed=True
                elif bribe_amount<=1000000 and prob<=0.25:
                        self.isbribed=True
                elif prob<=0.5:
                        self.isbribed=True
                else:
                        self.isbribed=False
                        
                # if a detective is bribed, there would be a possibility to be discovered 
                if self.isbribed:
                        self.discovered=discovered #parameter, initial 10%

                return self.isbribed


        def discoveredincrease(self):
                '''this function simulates the increasing probability of a detective to be discovered'''
                if self.isbribed:
                        x = random.randint(1,20)
                        self.discovered = self.discovered * (1+0.01*x)
                        if self.discovered > 1:
                                self.discovered = 1

        def isdiscovered(self):
                '''this function return the result if the detective is discovered (be bribed) or not'''
                prob = random.random()

                if prob <= self.discovered:
                        return True
                else:
                        return False

        def solved(self):
                '''this function returns if the detective solved a heist or not, and increases the solve ability if yes'''
                res = True
                prob=random.random()

                if prob<=self.solve_ability: #25%
                        x = random.randint(1,10)
                        self.solve_ability=self.solve_ability+x*0.01 
                        if self.solve_ability>=self.solve_cap:
                                self.solve_ability = self.solve_cap
                else:
                        res=False

                return res


#-----------------------------some functions-------------------------------------				
def readparameter(parafile):
        '''this fucntion used to read the paramater.txt file and stores the parameters into a dictionary'''
        with open(parafile) as infile:
                content = infile.readlines()
                para={} #create an empty dictionary
                for line in content:
                        line=line.strip().split('=')
                        key=line[0].strip()
                        val=line[1].strip()
                        para[key]=val

                return para # return a dictionary
        

def createBigg(para):
        '''this function creates Mr. Bigg'''
        thieves = []
        n_thieves = int(para['n_thieves'])
        n_testimony = int(para['n_testimony'])
        bigg = Bigg(n_thieves, n_testimony)
        bigg.recruite_thieves()

        return bigg

	
def createDetectives(para):
        '''this function creates a list of detectives'''
        n_detectives = int(para['n_detectives'])
        detectivelist=[]
        solve_init = float(para['solve_init'])
        solve_cap = float(para['solve_cap'])
        for i in range(n_detectives):
                d = Detective(solve_init, solve_cap)
                detectivelist.append(d)

        return detectivelist
	
def createOneDetective(para):
        '''this function creates one detective (in case any detective is discovered)'''
        solve_init = float(para['solve_init'])
        solve_cap = float(para['solve_cap'])
        d=Detective(solve_init, solve_cap)

        return d

def assign_detective(n_heist,n_detective):
        '''this function simulates the action of assigning each detective a heist'''
        res=[-1 for i in range(n_detective)] #list comprehension: [-1, -1, -1] if n_detective = 3
        num = 0
        while num < n_heist:
                for i in range(n_detective):
                        if res[i] != -1:
                                continue

                        a = random.randint(0, n_heist-1)
                        if a not in res:
                                res[i]=a
                                num+=1

                        if num>=n_heist:
                                break
                        
                if num >= n_detective:
                        break

        return res
	

	
def oneweek(para, Bigg, thievelist, detectivelist, summary, week, outfile):
        '''this function simulates all the interactions in one week'''
        print('--------------------------------------------------------')
        print(f'week {week}')

        outfile.write('--------------------------------------------------------\n')
        outfile.write(f'week {week}' + '\n')

        n_heist = len(thievelist) # number of heists
        n_detective=int(para['n_detectives']) # number of detectives
        discovered = float(para['discovered']) #the probability of a bribe is discovered
        #print(n_heist,n_detective) #for testing
        assign = assign_detective(n_heist,n_detective) #a list
        print('The detectives are assigned the following heists')
        print(assign)
        newthievelist=[]
        removethieveindex=[]
        for i in range(n_heist):
                d = random.randint(1,20)
                v = 1000*(d**2)
                # if the thief is not caught, he/she commits a heist
                if i not in assign:
                        thievelist[i].assignvalue(v)

                # if the thief is caught, check the detective
                else:
                        index = assign.index(i)
                        if detectivelist[index].isbribed: #if the detective is bribed, he/she will purposely fail to solve it
                                thievelist[i].assignvalue(v)
                                if detectivelist[index].isdiscovered():
                                        detectivelist[index]=createOneDetective(para)
                                else:
                                        detectivelist[index].discoveredincrease()
                        else:
                                if detectivelist[index].solved():
                                        print('The seized amount is '+str(v))
                                        detectivelist[index].seized += v
                                        print('The total seized amount is '+str(detectivelist[index].seized))
                                        thievelist[i].intojail(summary)
                                        removethieveindex.append(i)
                                else:
                                        thievelist[i].assignvalue(v)

                # if the thief is promoted to lieutenant
                if thievelist[i].promoted_to_lieutenant():
                        removethieveindex.append(i)
                        newthievelist.extend(thievelist[i].thieves)
                        summary['total']+=len(thievelist[i].thieves)

        # if the detective is bribed, calculate the bribe amount
        bribe_threshold = int(para['bribe_threshold'])
        bribe_percent = float(para['bribe_percent'])
        for i in range(len(detectivelist)):
                if detectivelist[i].isbribed:
                        continue

                #will be bribed every bribe_threshhold every after
                if detectivelist[i].seized >= (detectivelist[i].bribnum+1)*bribe_threshold:
                        print(f'Mr. Bigg\'s weekearning is {str(Bigg.weekearning)}')
                        if detectivelist[i].bribe(discovered, bribe_percent*Bigg.weekearning): #10%*earning
                                summary['bribe_amount']+=bribe_percent*Bigg.weekearning

        #re-orginze the list of thieves, exclude those who are in jail and promoted to lieutenant
        for i in range(len(thievelist)):
                if i not in removethieveindex:
                        newthievelist.append(thievelist[i])
        
        thievelist.clear()
        thievelist.extend(newthievelist)

        print("The total number of actors in Mr. Bigg’s criminal syndicate, excluding those jailed: " + str(summary['total']))
        print("the total number of thieves/lieutenants jailed " + str(summary['jailed']))
        print("the personal wealth of Mr. Bigg is " + str(Bigg.wealth))
        print("the total amount of bribes accepted by detectives " + str(summary['bribe_amount']))
        print(f'------------------Here is the summary for week {week}-------------')
        print(summary)

        outfile.write("The total number of actors in Mr. Bigg’s criminal syndicate, excluding those jailed: " + str(summary['total']) + '\n')
        outfile.write("the total number of thieves/lieutenants jailed " + str(summary['jailed']) + '\n')
        outfile.write("the personal wealth of Mr. Bigg is "+str(Bigg.wealth)+'\n')
        outfile.write("the total amount of bribes accepted by detectives "+str(summary['bribe_amount']) + '\n')

        #clear the week earning
        Bigg.weekearning=0

        if Bigg.jailed:
                print('Bigg is jailed')
                print('--------------------------------------------------------')
                return True
        print('--------------------------------------------------------')

        outfile.write('--------------------------------------------------------\n')
        return False



#-----------------------------Main Function-------------------------------------
def simulation(parafile): #parafile: parameter file name
        '''this is the main function simulates the whole interactions between
        Mr. Bigg, the thieves, the lieutenants, and detectives in 500 weeks or Mr. Bigg is arrested'''

        para = readparameter(parafile)
        Bigg = createBigg(para)
        thievelist = [t for t in Bigg.thieves]
        print('start')
        detectivelist=createDetectives(para)

        outfile = open('Result.txt', 'w')

        weeks = int(para['weeks'])
        summary={}
        summary['total']=len(thievelist)+1
        summary['jailed']=0
        summary['Mr. Bigg personal wealth']=0
        summary['bribe_amount']=0

        for week in range(1, (weeks+1)):
                if oneweek(para, Bigg, thievelist, detectivelist, summary, week, outfile):

                        print('The Bigg is jailed, game over')
                        break
		

#------------------------run the main function-----------------------
if __name__ == '__main__':
        simulation("parameter.txt")
