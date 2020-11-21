import subprocess

FILENAME = "output.csv"
f = open(FILENAME, "a")
for d in range(3, 9):
    for pk in range(1, 33, 1):
        for mc in (1, 6):
            for ps in range(1, 101, 5):
                for _ in range(10):
                    subprocess.Popen(f"python3 GeoGame.py -g -d {d} -pk {0.01 * pk} -mc {0.001 * mc} -ps {ps} >> {FILENAME}".split(), stdout=subprocess.PIPE)