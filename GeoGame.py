import random
import Solution

airtime = Solution.hangtime
jumpchance = .3 #   % chance that it will jump at any given tick
pathlength = 100 #  Length of path
trials = 25 #       Population size

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
        #print(self.InAir,self.lives)
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
        #print(self.InAir,self.lives)
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

def GenerateEasyPath():
    path = [[0,0]]
    c = 3
    count = 0
    for i in range(pathlength - 1):
        a = 0
        b = 0
        if (count > 0):
            count -= 1
        elif random.randint(1,3) == 1:
            a = 1
            count = airtime
        elif random.randint(1,3) == 1:
            b = 1
            count = airtime
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
        #print(trials[j].length)
        #print(jumpLoc[j])
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
        #print(trials[j].length)
        #print(jumpLoc[j])
        Pass = PassOn(trials[j].length, jumpLoc[j])
        prevGen.append(Pass)


# Convert from form 0 = stay, 1 = jump, and insert hangtime after jumps
def convertBinary(jumps):
    moves = []
    i = 0
    while i<len(jumps):
        if jumps[i] == 0:
            moves += ['stay']
        else:
            moves += ['jump']
            for j in range(airtime):
                moves += ['hang']
                i += 1
        i += 1
    ret = Solution.Solution
    ret.moves = moves
    return ret

# Convert to form 0=stay, 1=jump, and hangtime doesn't matter
def makeToBinary(moves):
    ret = []
    for i in range(len(moves)):
        if moves[i] == 'jump':
            ret += [1]
        elif moves[i] == 'stay':
            ret += [0]
        else:
            if random.random()<jumpchance:
                ret += [1]
            else:
                ret += [0]
    return ret

def doRun():
    global prevGen
    jumpLoc.clear()
    solutions = []
    average = 0
    longest = 0
    for i in range(trials): #make list of Solutions and get average score
        solution = convertBinary(prevGen[i].pattern)
        if len(solution.moves) >= pathlength:
            print("FOUND AN OPTIMAL PATH:")
            print(prevGen[i].pattern)
            return True
        elif len(solution.moves) > longest:
            longest = len(solution.moves)
        average += len(solution.moves)
        solutions += [solution]
    average = average/trials
    print(longest)

    #print("SOLUTIONS:")
    newSolutions = solutions
    for i in range(len(solutions)-1,0,-1): #purge em
        if len(solutions[i].moves) < average:
            del solutions[i]

    prevGen.clear()

    for i in range(trials): #randomly select and breed parents
        parent1 = solutions[random.randint(0,len(solutions)-1)]
        parent2 = solutions[random.randint(0,len(solutions)-1)]
        thisChild = Solution.Solution(parent1,parent2)
        binaryMoves = makeToBinary(thisChild.moves)
        prevGen += [PassOn(len(binaryMoves),binaryMoves)]

    RunNextTrial(p,trials,prevGen)
    return False

p = GenerateEasyPath()
print(p)
print("RUNNING")
RunFirstTrial(p, trials)

for i in range(100):
    if doRun() == True:
        break
print(p)

f = open("path.txt",'w')
for i in range(len(p)):
    stringyboi = str(p[i][0]) + str(p[i][1]) + ' '
    f.write(stringyboi)
f.write("\n00000")
f.close()