import os

FILENAME = "new.csv"
f = open(FILENAME, "a")
for pk in range(10, 25, 5): #percent of population to keep
    for mc in (1, 5): #mutation chance
        for ps in range(1, 20, 5): #population size
            list = []
            for _ in range(10): #retry just for good measure...
                command = "python3 GeoGame.py -g -pk "+str(0.01 * pk)+" -mc "+str(0.001 * mc)+" -ps "+str(ps)
                output = os.popen(command).read()
                if output != '':
                  list += [int(output)]
            #back outside of loopy
            list.sort()
            median = list[int(len(list)/2)]
            output = str(pk)+","+str(mc)+","+str(ps)+","+str(median)
            f.write(output)
            os.system(command)
f.close()
