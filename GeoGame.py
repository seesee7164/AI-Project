import random
import Solution
import matplotlib.pyplot as plt
import Graphics
import sys

'''
FLAGS:
-na         no animation
-np         no plotting
-g          print nothing but number of generations
-d <n>      delete n moves
-ps <n>     population size set to n
-pk <f>     percentKeep set to float f
-mc <f>     mutationChance in Solution.py set to float f
'''

def getFlagVal(flag):
    for i, arg in enumerate(sys.argv):
        if arg == flag:
            try: return sys.argv[i+1]
            except: 
                print("Error in fetching flag value.")
                sys.exit(1)

airtime = Solution.hangtime  # Ticks the agent is in the air for
jumpchance = Solution.jumpChance  # % chance that it will jump at any given tick
pathlength = 150
populationSize = 100
# Generations to try before giving up (not all levels are possible with x lives)
maxGenerations = 250
gamerLives = 1  # Number of lives each agentGets (hit obstacle = lose 1 life)
levelDifficulty = 3  # Minimum number of spaces between obstacles, lower = harder
percentKeep = 0.05 # How much of the population to keep or purge

if "-ps" in sys.argv: populationSize = int(getFlagVal("-ps"))
if "-pk" in sys.argv: percentKeep = float(getFlagVal("-pk"))

prevGen = []
jumpLoc = []
longestSolutions = []  # Longest solution length for each generation
averageSolutions = []  # Average solution length for each generation
# Will be filled with longest Solution found (the path itself, not the length)
longestOverallSolution = []

#This class will create the avatar tracks aspects of the character
#as it moves through the game and performs the functions needed to
#make the game work
class avatar:
    lives = gamerLives
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
        # checking if the object and the obstacle are both in the air
        if self.InAir and obstacles[1]:
            self.hit()
        # checking if the object and the obstacle are both on the ground
        if not self.InAir and obstacles[0]:
            self.hit()
        if not self.InAir and flag == 1:  # jumping function
            self.jump()
        elif self.InAir:
            self.falling()
        self.length += 1
        # self.jumpLoc.append(flag)
        return flag

    def RepeatTurn(self, obstacles, jumps):
        flag = jumps
        # checking if the object and the obstacle are both in the air
        if self.InAir and obstacles[1]:
            self.hit()
        # checking if the object and the obstacle are both on the ground
        if not self.InAir and obstacles[0]:
            self.hit()
        if not self.InAir and flag == 1:  # jumping function
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
    path = [[0, 0]]
    for i in range(pathlength - 1):
        a = 0
        b = 0
        if random.randint(1, 3) == 1:
            a = 1
        elif random.randint(1, 3) == 1:
            b = 1
        path.append([a, b])
    return path


def GenerateEasyPath(c=3):
    path = [[0, 0]]
    count = 0
    for i in range(pathlength - 2):
        a = 0
        b = 0
        if (count > 0):
            count -= 1
        elif random.randint(1, 3) == 1:
            a = 1
            count = c
        elif random.randint(1, 3) == 1:
            b = 1
            count = c
        path.append([a, b])
    path.append([0,0])
    return path


def RunFirstTrial(path, tests):
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
        Pass = PassOn(trials[j].length, jumpLoc[j])
        prevGen.append(Pass)


def RunNextTrial(path, tests, initialized):
    length = len(path)
    trials = []
    for i in range(tests):
        obj = avatar()
        #obj.lives += 1 #this part is included for testing purposes
        trials.append(obj)
        jumpLoc.append([])
    for i in range(length):
        for j in range(tests):
            if trials[j].Alive:
                if i >= initialized[j].length:
                    f = trials[j].PassTurn(path[i])
                    jumpLoc[j].append(f)
                else:
                    f = trials[j].RepeatTurn(
                        path[i], initialized[j].pattern[i])
                    jumpLoc[j].append(f)
    prevGen.clear()
    for j in range(tests):
        Pass = PassOn(trials[j].length, jumpLoc[j])
        prevGen.append(Pass)


# Convert from form 0 = stay, 1 = jump, and insert hangtime after jumps
def convertBinary(jumps):
    moves = []
    i = 0
    while i < len(jumps):
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
            if random.random() < jumpchance:
                ret += [1]
            else:
                ret += [0]
    return ret


def runGeneration():
    global prevGen
    global longestSolutions
    global averageSolutions
    global longestOverallSolution

    jumpLoc.clear()
    solutions = []
    average = 0
    longest = []  # Longest solution found in this generation
    for i in range(populationSize):  # make list of Solutions and get average score
        solution = convertBinary(prevGen[i].pattern)
        if len(solution.moves) > len(longest):
            longest = solution.moves
        average += len(solution.moves)
        solutions += [solution]
    average = average/populationSize
    longestSolutions += [len(longest)]
    averageSolutions += [average]
    if len(longest) >= pathlength:
        return [True, longest]
    if len(longest) > len(longestOverallSolution):
        longestOverallSolution = longest

    # Purge anything but the best
    solutions.sort(key=lambda x: x.moves)
    solutions = solutions[int(len(solutions)*(1-percentKeep)):]

    prevGen.clear()

    for i in range(populationSize):  # randomly select and breed parents
        parent1 = solutions[random.randint(0, len(solutions)-1)]
        parent2 = solutions[random.randint(0, len(solutions)-1)]
        thisChild = Solution.Solution(parent1, parent2, sys.argv)
        binaryMoves = makeToBinary(thisChild.moves)
        prevGen += [PassOn(len(binaryMoves), binaryMoves)]

    RunNextTrial(p, populationSize, prevGen)
    return [False, []]

# Setup path
if "-g" not in sys.argv: print("Creating path")
p = GenerateEasyPath(levelDifficulty)
RunFirstTrial(p, populationSize)

# Keep running until solution is found
if "-g" not in sys.argv: print("Trying to find a solution...")
runResult = None
for i in range(maxGenerations):
    runResult = runGeneration()
    if runResult[0] == True:
        if "-g" not in sys.argv: print("Found one in ", len(longestSolutions), " generations!")
        break
if runResult[0] == False:
    if "-g" not in sys.argv: print("Couldn't find one :(")
    runResult[1] = longestOverallSolution

# Put into file to view graphics at any time, then display it running
f = open("data.txt", 'w')
for i in range(len(p)):
    pathString = str(p[i][0]) + str(p[i][1]) + ' '
    f.write(pathString)
runString = "\n"
for i in range(len(runResult[1])):
    if runResult[1][i] == "jump" or runResult[1][i] == "stay":
        runString += "0"
    else:
        runString += "1"
f.write(runString)
f.close()

if "-na" not in sys.argv and "-g" not in sys.argv:
    if "-g" not in sys.argv: print("Displaying best solution")
    Graphics.main()
else:
    if "-g" not in sys.argv: print("Skipping animation.")

# Plot the longest solutions
if "-np" not in sys.argv and "-g" not in sys.argv:
    if "-g" not in sys.argv: print("Plotting solution lengths")
    axes = plt.gca()
    axes.set_xlim([0, len(longestSolutions)])
    axes.set_ylim([0, pathlength])
    xaxis = []
    for i in range(len(longestSolutions)):
        xaxis += [i]
    plt.title("Solution Length over Time")
    plt.xlabel("Generation")
    plt.ylabel("Longest Solution")
    plt.plot(xaxis, averageSolutions,
            label="Average Solution Length", ls='--', color='grey')
    plt.plot(xaxis, longestSolutions, label="Longest Solution", color='blue')
    plt.legend()
    plt.show()
else:
    if "-g" not in sys.argv: print("Skipping plot")