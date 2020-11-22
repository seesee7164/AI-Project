import os

FILENAME = "output.csv"
f = open(FILENAME, "a")
for d in range(3, 9): #moves to delete off of solutions
    for pk in range(1, 50, 1): #percent of population to keep
        for mc in (1, 11): #mutation chance
            for ps in range(1, 121, 5): #population size
                for _ in range(100): #retry just for good measure...
                    command = "printf "+str(d)+","+str(pk)+","+str(mc)+","+str(ps)+", >> "+FILENAME
                    ret = os.system(command)
                    if ret!=0:
                        print("OOPS: ",ret)
                    command = "python3 GeoGame.py -g -d "+str(d)+" -pk "+str(0.01 * pk)+" -mc "+str(0.001 * mc)+" -ps "+str(ps)+" >> "+FILENAME
                    ret = os.system(command)
                    if ret!=0:
                        print("OOPS: ",ret)
                    # Python program should be outputting our newline, will cause problems if we want more things in the .csv
