import sys, random, tkinter as tk

def generateEvent(spacing, variability):
    return random.randint(spacing-variability, spacing+variability)

class Level:
    def __init__(self, width=100, spacing=6, variability=1):
        self.level = []
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

    def __str__(self):
        top = ""
        bottom = ""
        for tile in self.level:
            top += str(tile[1])
            bottom += str(tile[0])
        return f"{top}\n{bottom}"

def main():
    LEVELWIDTH = 100
    SQUARESIZE = 15
    l = Level(width=LEVELWIDTH, variability=3)
    
    top = tk.Tk()
    w = tk.Canvas(top, width=LEVELWIDTH*SQUARESIZE, height=SQUARESIZE*2)
    w.pack()

    for i in range(len(l.level)):
        bottomColor = "white"
        skyColor = "white"

        if l.level[i][0] == 1: bottomColor = "black"
        if l.level[i][1] == 1: skyColor = "black"

        x1 = SQUARESIZE * i
        y1 = 0

        x2 = x1 + SQUARESIZE
        y2 = y1 + SQUARESIZE

        x3 = x1
        y3 = SQUARESIZE

        x4 = x3 + SQUARESIZE
        y4 = y3 + SQUARESIZE

        # drawing floor square
        w.create_rectangle(x1, y1, x2, y2, fill=bottomColor)

        # drawing sky square
        w.create_rectangle(x3, y3, x4, y4, fill=skyColor)

    tk.mainloop()

if __name__ == "__main__":
    main()