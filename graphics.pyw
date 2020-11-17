import random, time, tkinter as tk
from tkinter import Variable

def generateEvent(spacing, variability):
    return random.randint(spacing-variability, spacing+variability)

# generally, this class operates under the assumtion that tiles are something like
# [floor, sky].
# so something like [0, 1] would mean there's NO tile on the floor, but IS one in the sky.
class Level:
    def __init__(self, width=100, spacing=6, variability=1, readIn=""):
        # this implies that data.txt is structured as follows:
        # one line is the map, with pairs of numbers as each tile
        # for example, 00 00 01 00 10 is then
        # 0 0 1 0 0
        # 0 0 0 0 1
        # the next line is movements taken by the winner

        self.level = []
        self.movements = []

        if readIn != "":
            f = open(readIn, 'r')
            data = []
            for line in f:
                data.append(line.split())

            for tile in data[0]:
                self.level.append([int(tile[0]), int(tile[1])])

            for move in data[1][0]:
                self.movements.append(int(move))

            f.close()

        else: 
            event = generateEvent(spacing, variability)
            for i in range(width):
                if event > 0:
                    self.level.append([0, 0])
                    event -= 1
                else:
                    isInSky = random.randint(0, 1) % 2 == 0
                    if isInSky: self.level.append([0, 1])
                    else: self.level.append([1, 0])
                    event = generateEvent(spacing, variability)

    def drawLevel(self, w):
        for i in range(len(self.level)):
            bottomColor = "white"
            skyColor = "white"

            if self.level[i][0] == 1: bottomColor = "black"
            if self.level[i][1] == 1: skyColor = "black"

            x1 = SQUARESIZE * i
            y1 = 0
            x2 = x1 + SQUARESIZE
            y2 = y1 + SQUARESIZE
            x3 = x1
            y3 = SQUARESIZE
            x4 = x3 + SQUARESIZE
            y4 = y3 + SQUARESIZE

            # drawing floor square
            w.create_rectangle(x3, y3, x4, y4, fill=bottomColor)

            # drawing sky square
            w.create_rectangle(x1, y1, x2, y2, fill=skyColor)

    def partialDrawLevel(self, w, i):
        bottomColor = "white"
        skyColor = "white"

        if self.level[i][0] == 1: bottomColor = "black"
        if self.level[i][1] == 1: skyColor = "black"

        x1 = SQUARESIZE * i
        y1 = 0
        x2 = x1 + SQUARESIZE
        y2 = y1 + SQUARESIZE
        x3 = x1
        y3 = SQUARESIZE
        x4 = x3 + SQUARESIZE
        y4 = y3 + SQUARESIZE

        # drawing floor square
        w.create_rectangle(x3, y3, x4, y4, fill=bottomColor)

        # drawing sky square
        w.create_rectangle(x1, y1, x2, y2, fill=skyColor)

    def animate(self, top, w, leaveTrail, frameSpeed, i=0):
        if i >= len(self.level): 
            if not leaveTrail: self.partialDrawLevel(w, i-1)
            return
        else:
            x1 = SQUARESIZE * i
            y1 = 0
            x2 = x1 + SQUARESIZE
            y2 = y1 + SQUARESIZE
            x3 = x1
            y3 = SQUARESIZE
            x4 = x3 + SQUARESIZE
            y4 = y3 + SQUARESIZE

            # hero stays on ground
            if self.movements[i] == 0:
                w.create_rectangle(x3, y3, x4, y4, fill="green")
            else:
                w.create_rectangle(x1, y1, x2, y2, fill="green")

            if not leaveTrail and i > 0: self.partialDrawLevel(w, i-1)

            top.after(frameSpeed, lambda: self.animate(top, w, leaveTrail, frameSpeed, i+1))

    def getLevelWidth(self):
        return len(self.level)

    def __str__(self):
        top = ""
        bottom = ""
        for tile in self.level:
            top += str(tile[1])
            bottom += str(tile[0])
        return f"{top}\n{bottom}"

def main():
    global SQUARESIZE # squares will be SQUARESIZE by SQUARESIZE pixels in area
    SQUARESIZE = 15 # yes we need two lines here

    l = Level(variability=3, readIn="data.txt")
    
    top = tk.Tk()
    top.title("GamerBot 9000")

    try: top.iconbitmap("joystick.ico")
    except tk.TclError: pass

    windowWidth = max((l.getLevelWidth()*SQUARESIZE), SQUARESIZE*15) # we want the window to be at least 15 tiles in width for good display purposes
    w = tk.Canvas(top, width=windowWidth, height=SQUARESIZE*2)
    w.pack()

    l.drawLevel(w)

    isTicked = tk.IntVar()
    buttonDiv = tk.Canvas(top)

    msTextLabel = tk.Label(buttonDiv, text="Frame speed (ms): ")
    msTextLabel.pack(side=tk.LEFT)

    msVal = tk.StringVar()
    msVal.set("50")
    msEntry = tk.Entry(buttonDiv, width=5, textvariable=msVal)
    msEntry.pack(side=tk.LEFT)

    msSpacer = tk.Label(buttonDiv, text=" ")
    msSpacer.pack(side=tk.LEFT)

    buttonDiv.pack()
    animateButton = tk.Button(buttonDiv, text="Animate!", width=10, command=lambda: l.animate(top, w, isTicked.get(), int(msVal.get())))
    animateButton.pack(side=tk.LEFT)
    
    trailCheckbox = tk.Checkbutton(buttonDiv, variable=isTicked, text="Leave trail?", onvalue=1, offvalue=0)
    trailCheckbox.pack(side=tk.RIGHT)

    resetButton = tk.Button(buttonDiv, text="Reset", width=10, command=lambda: l.drawLevel(w))
    resetButton.pack(side=tk.RIGHT)

    tk.mainloop()

if __name__ == "__main__":
    main()