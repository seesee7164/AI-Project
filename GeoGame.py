import random

airtime = 3
jumpchance = .3
pathlength = 10

class avatar:
    lives = 3
    Alive = True
    length = 0
    InAir = False
    TurnsAirbound = 0
    jumpLoc = []
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
        if self.InAir and obstacles[1]:  #checking if the object and the obstacle are both in the air
            self.hit()
        if not self.InAir and obstacles[0]:  #checking if the object and the obstacle are both on the ground
            self.hit()
        print(self.InAir,self.lives)
        if not self.InAir and random.random() < jumpchance:    #jumping function
            self.jump()
            flag = 1
        elif self.InAir:
            self.falling()
        self.length += 1
        self.jumpLoc.append(flag)


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



def RunTrial(path,tests):
    length = len(path)
    trials = []
    for i in range(tests):
        obj = avatar()
        trials.append(obj)
    for i in range(length):
        for j in trials:
            if j.Alive:
                j.PassTurn(path[i])
    for j in trials:
        print(j.length)
        print(j.jumpLoc)
p = GeneratePath()
print(p)
RunTrial(p, 1)