import random

airtime = 3
jumpchance = .3
pathlength = 20
prevGen = []
jumpLoc =[]
class avatar:
    lives = 3
    Alive = True
    length = 0
    InAir = False
    TurnsAirbound = 0
    def falling(self):
        self.TurnsAirbound -= 1
        if self.TurnsAirbound == 0:
            self.InAir = False
    def hit(self):
        self.lives -= 1
        if self.lives == 0:
            self.Alive = False
    def jump(self):
        self.InAir = True
        self.TurnsAirbound = airtime
    def PassTurn(self, obstacles):
        flag = 0
        if random.random() < jumpchance:
            flag = 1
        if self.InAir and obstacles[1]:  #checking if the object and the obstacle are both in the air
            self.hit()
        if not self.InAir and obstacles[0]:  #checking if the object and the obstacle are both on the ground
            self.hit()
        print(self.InAir,self.lives)
        if not self.InAir and flag == 1:    #jumping function
            self.jump()
        elif self.InAir:
            self.falling()
        self.length += 1
        # self.jumpLoc.append(flag)
        return flag
    def RepeatTurn(self, obstacles,jumps):
        flag = jumps
        if self.InAir and obstacles[1]:  #checking if the object and the obstacle are both in the air
            self.hit()
        if not self.InAir and obstacles[0]:  #checking if the object and the obstacle are both on the ground
            self.hit()
        print(self.InAir,self.lives)
        if not self.InAir and flag == 1:    #jumping function
            self.jump()
        elif self.InAir:
            self.falling()
        self.length += 1
        # self.jumpLoc.append(flag)
        return flag
class PassOn:
    def __init__(self, l, jumps):
        self.length = l
        self.pattern = jumps

def GeneratePath():
    path = [[0,0]]
    for i in range(pathlength - 1):
        a = 0
        b = 0
        if random.randint(1,3) == 1:
            a = 1
        elif random.randint(1,3) == 1:
            b = 1
        path.append([a,b])
    return path



def RunFirstTrial(path,tests):
    length = len(path)
    trials = []
    for i in range(tests):
        obj = avatar()
        trials.append(obj)
        jumpLoc.append([])
    for i in range(length):
        for j in range(tests):
            if trials[j].Alive:
                f = trials[j].PassTurn(path[i])
                jumpLoc[j].append(f)
    prevGen.clear()
    for j in range(tests):
        print(trials[j].length)
        print(jumpLoc[j])
        Pass = PassOn(trials[j].length, jumpLoc[j])
        prevGen.append(Pass)

def RunNextTrial(path, tests, initialized):
    length = len(path)
    trials = []
    for i in range(tests):
        obj = avatar()
        obj.lives += 1 #this part is included for testing purposes
        trials.append(obj)
        jumpLoc.append([])
    for i in range(length):
        for j in range(tests):
            if trials[j].Alive:
                # print(trials[j].jumpLoc[j])
                if i >= initialized[j].length:
                    f = trials[j].PassTurn(path[i])
                    jumpLoc[j].append(f)
                else:
                    f = trials[j].RepeatTurn(path[i],initialized[j].pattern[i])
                    jumpLoc[j].append(f)
    prevGen.clear()
    for j in range(tests):
        print(trials[j].length)
        print(jumpLoc[j])
        Pass = PassOn(trials[j].length, jumpLoc[j])
        prevGen.append(Pass)
p = GeneratePath()
print(p)
trials = 1
RunFirstTrial(p, trials)
jumpLoc.clear()
# for i in prevGen:
#     print(i.length)
RunNextTrial(p,trials,prevGen)